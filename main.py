import logging.config
from typing import List
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Query, Request, Response, Depends, Header
from fastapi.responses import JSONResponse
from fastapi_utils.session import FastAPISessionMaker

from db.db_conf import get_db
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models.user import User
import jwt
from logs.logs_config import LOGGING_CONFIG
import logging
from api.v1.links.links import router as links_router
from auth.auth import get_user_secure
from schemas.response_schemas.secured import SecuredResponse
from fastapi_utils.tasks import repeat_every
import os
from models import ShortLink
from schemas.request_schemas.links import ModelUser
import datetime
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field


load_dotenv()

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

app = FastAPI()
origins = ["*"]

app.include_router(links_router)


database_uri = os.environ.get('DATABASE_URL')

sessionmaker = FastAPISessionMaker(database_uri)

@app.middleware('http')
def catch_exceptions_middleware(request: Request, call_next):
    try:
        return call_next(request)
    except Exception as e:
        logger.exception(e)
        return Response('Internal server error', status_code=500)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/secured')
def secured(user: User=Depends(get_user_secure)):
    print(user)
    return True


@app.on_event("startup")
@repeat_every(seconds=60*60*12)  # 1 hour
def update_everything_task() -> None:
    with sessionmaker.context_session() as db:
        expired = db.query(ShortLink).filter(ShortLink.expires_at<datetime.datetime.now()).all()
        for ex in expired:
            db.delete(ex)
            db.commit()
            

def find_user_login(db, login):
    return db.query(User).filter(User.login==login).first()

@app.post("/register")
def read_main(request: ModelUser,db:Session=Depends(get_db)):
    user = find_user_login(db,request.login)
    print(user)
    # db.query(User).filter(User.login==request.login).first()
    if user:
        return {'error': 'user is already registred'}
    obj: User = db.query(User).order_by(User.id.desc()).first()
    if obj:
        id = obj.id + 1
    else:
        id = 1
    encoded_jwt = jwt.encode({"login": request.login, 'password': request.password, 'user_id': id}, "secret", algorithm="HS256")
    user = User(login=request.login, password=request.password, token=encoded_jwt)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post('/login')
def login(request: ModelUser, db: Session=Depends(get_db)):
    user = db.query(User).filter(User.login==request.login,User.password==request.password).first()
    if not user:
        return {'error': 'No such user'}
    else:
        return user

class Token(BaseModel):
    access_token: str
    token_type: str

@app.post('/token', response_model=Token)
def token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(get_db)):
    user: User = db.query(User).filter(User.login==form_data.username).first()
    print('123')
    if not user:
        return {'error': 'No such user'}
    else:
        encoded = jwt.encode({"login": user.login, 'env': os.environ.get("TOKEN_ENV"), 'user': user.id, 'exp': datetime.datetime.now() + datetime.timedelta(minutes=1440)}, key=str(os.environ.get("TOKEN_KEY")), algorithm="HS256")
    print(user)
    return {'access_token': encoded, 'token_type': 'bearer'}

    
@app.get("/")
async def read_main():
    return {"msg": "Hello World"}

if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8007, reload=True, debug=True)
