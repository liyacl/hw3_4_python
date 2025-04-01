from typing import List
from fastapi import Depends
from logs.logs_config import LOGGING_CONFIG
import logging
from db.db_conf import get_db
from sqlalchemy.orm import Session
from models.user import User
from fastapi.exceptions import HTTPException
import jwt
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv
load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

def secure(token):
    print('token')
    decoded_token = jwt.decode(token, str(os.environ.get("TOKEN_KEY")), algorithms='HS256', verify=False)
    print(decoded_token)
    return decoded_token

def get_user_secure(token: str = Depends(oauth2_scheme), db: Session=Depends(get_db)):  ## Get user from decoded token 
    if not token:
        return None

    try: 
        user_data = secure(token)
        print(user_data)
        user = db.query(User).filter(User.id==user_data['user']).first()
        if user:
            return user
        else:
            print("here?")
            raise HTTPException(status_code=400, detail='invalid_user')
    except Exception as e:
        return None
        print(e)
        return HTTPException(status_code=400, detail='Not valid token')
