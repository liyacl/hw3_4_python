from fastapi import APIRouter
from auth.auth import get_user_secure
import logging
from fastapi import FastAPI, Query, Request, Response, Depends, Header
import logging
from db.db_conf import get_db
from sqlalchemy.orm import Session
from models import *
from schemas.request_schemas.links import CreateLink,UpdateLink
from models.short_links import ShortLink
import string
import random
from fastapi.exceptions import HTTPException
from datetime import datetime
import re

from sqlalchemy import or_

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/links",
    tags=["api", 'links'],
    responses={404: {"description": "Not found"}},
)

alphabet = string.ascii_lowercase + string.digits

def short_url_generate():
    return ''.join(random.choices(alphabet, k=8))


logger = logging.getLogger(__name__)

url_pattern = r'^https?:\/\/[a-z0-9]+(?:[-.][a-z0-9]+)*(?::[0-9]{1,5})?(?:\/[^\/\r\n]+)*\.[a-z]{2,5}(?:[?#]\S*)?$'


# @router.post('/')
# def short(db:Session=Depends(get_db)):
#     link = ShortLink(url='123', short_url='321',usage_count=0,creation_date = datetime.now())
#     db.add(link)
#     db.commit()
#     return link

@router.post('/shorten')
def short(request: CreateLink, db:Session=Depends(get_db), user: User=Depends(get_user_secure)):
    logger.info(f"link {request.url}")
    # if not re.fullmatch(url_pattern,request.url):
    #     raise HTTPException(400, 'url is' not valid')
    if not request.custom_alias:
        short_url = short_url_generate()
    else:
        if not db.query(ShortLink).filter(ShortLink.custom_alias==request.custom_alias).first():
            short_url = request.custom_alias
        else:
            raise HTTPException(400, 'alias is already taken')
        
        # already_link = db.query(ShortLink).filter(ShortLink.url==request.url).first()
        # if not request.custom_alias and already_link:
        #     return already_link

    link = ShortLink(url=request.url, short_url=short_url,usage_count=0,creation_date = datetime.now(), custom_alias=request.custom_alias, expires_at=request.expires_at)
    if user:
        link.user_id = user.id
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


def get_shortlink_by_code(db, short_code):
    url: ShortLink = db.query(ShortLink).filter(ShortLink.short_url==short_code).first()
    return url 

@router.get('/{short_code}')
def short(short_code: str, db:Session=Depends(get_db)):
    url: ShortLink = get_shortlink_by_code(db, short_code)
    if not url: 
        return 'no url found' 

    url.usage_count = url.usage_count+1
    url.last_usage_date = datetime.now()
    db.add(url)
    db.commit()
    return url.url


def get_shorlink_by_user_and_code(db, short_code, user_id):
    return db.query(ShortLink).filter(ShortLink.short_url==short_code, ShortLink.user_id==user_id).first()

@router.delete('/{short_code}')
def short(short_code: str, db:Session=Depends(get_db), user: User=Depends(get_user_secure)):
    if not user:
        raise HTTPException(400, 'onlu auth users')

    url: ShortLink = get_shorlink_by_user_and_code(db, short_code, user.id)
    if not url: 
        return 'no url found'
    
    db.delete(url)
    db.commit()
    return True

@router.put('/{short_code}')
def short(short_code: str, request: UpdateLink,user: User=Depends(get_user_secure), db:Session=Depends(get_db)):

    if not user:
        raise HTTPException(400, 'onlu auth users')
    
    print(user.id)

    url: ShortLink = get_shorlink_by_user_and_code(db, short_code, user.id)
    if not url: 
        return 'no url found'
    
    url.url = request.url
    url.expires_at = request.expires_at
    db.add(url)
    db.commit()
    return url



@router.get('/{short_code}/stats')
def short(short_code: str, db:Session=Depends(get_db)):
    link = get_shortlink_by_code(db, short_code)
    # link: ShortLink = db.query(ShortLink).filter(ShortLink.short_url==short_code).first()
    if not link: 
        return 'no url found'
    
    return {'original_utl': link.url, 'creation_date': link.creation_date, 'redirects': link.usage_count, 'last_usage_date': link.last_usage_date }


@router.get('/search/{url}')
def search(url: str, db:Session=Depends(get_db)):
    url = 'string'
    link: ShortLink = db.query(ShortLink).filter(ShortLink.url==url).first()
    if not link: 
        return 'no url found'
    
    return {'original_utl': link.url, 'shorten': link.short_url }



# @router.get('/search?original_url={url}')
# def short(url: str, db:Session=Depends(get_db)):
#     link: ShortLink = db.query(ShortLink).filter(ShortLink.url==url).first()
#     if not link: 
#         return 'no url found'
    
#     return {'original_utl': link.url, 'shorten': link.short_url }





