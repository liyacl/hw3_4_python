import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.db_conf import Base, get_db
from models.user import User
from main import app  # Ensure this imports your FastAPI app
from sqlalchemy.engine import URL
from api.v1.links.links import short_url_generate
import re
from models.short_links import ShortLink
from typing import List
from fastapi import Depends
from logs.logs_config import LOGGING_CONFIG
import logging
from db.db_conf import get_db
from sqlalchemy.orm import Session
from models.user import User
from fastapi.exceptions import HTTPException
import jwt
from auth.auth import get_user_secure
from unittest.mock import Mock, MagicMock, patch 
from fastapi.security import OAuth2PasswordBearer

mock_session = MagicMock()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        # Base.metadata.create_all(bind=engine)
        # db = TestingSessionLocal()
        yield mock_session
    finally:
        pass
        # db.close()

@pytest.fixture
def mock_db_session():
    return mock_session

# def override_user_secure():  ## Get user from decoded token 
#     return User(email='m@m.ru', password=123, login='123', token='123')


app.dependency_overrides[get_db] = override_get_db

# app.dependency_overrides[get_user_secure] = override_user_secure

client = TestClient(app)



# User(login='google.com', password='123',email='1@1.ru')
def test_create_link(mocker):
    response = client.post(
        "/register",
        json={"email": "w@m.ru", 'login': '321', 'password': '321'}
    )
    mocker.patch('main.find_user_login', return_value='None')

    assert response.status_code == 200
    data = response.json()
    print(data)
    # assert data["url"] == "https://example.com"



# def test_user(monkeypatch):
#     # Create a test user in the database
#     db = TestingSessionLocal()
#     Base.metadata.create_all(engine)
#     user = User(login="testuser", password='123',token='123')

#     db.add(user)
#     db.commit()
#     monkeypatch.setenv("TOKEN_KEY", "test_secret")
#     monkeypatch.setenv("TOKEN_ENV", "test")
#     token_response = client.post(
#         "/token",
#         data={"username": "testuser", "password": "123"}
#     )
#     # print(token_response)
#     assert user.login=='wssqwdewqw'
#     assert user.id ==1
    


    # access_token = token_response.json()["access_token"]

    # Access secured endpoint
    # response = client.get(
    #     "/secured",
    #     headers={"Authorization": f"Bearer {access_token}"}
    # )
    # assert response.status_code == 200
    # assert response.json() is True