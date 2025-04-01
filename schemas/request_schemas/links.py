from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class CreateLink(BaseModel):
    url: str
    custom_alias: Optional[str]
    expires_at: Optional[datetime]
    # comment: str
    # main_photo: str
    # price: int

class UpdateLink(BaseModel):
    short_code: Optional[str]
    url: Optional[str]
    expires_at: Optional[datetime]


class ModelUser(BaseModel):
    login: str
    password: str


# class LoginUser(BaseModel):
#     login: str
#     password: str

# class UserRegister(BaseModel):
#     login: str
#     password: str
#     email: str


# class UserLogin(BaseModel):
#     login: str
#     password: str
