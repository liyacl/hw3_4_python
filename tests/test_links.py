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
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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

def override_user_secure():  ## Get user from decoded token 
    return User(email='m@m.ru', password=123, login='123', token='123')


app.dependency_overrides[get_db] = override_get_db

app.dependency_overrides[get_user_secure] = override_user_secure

client = TestClient(app)



    
def test_link_creation():
    link = short_url_generate()
    my_regex = re.compile(r"\b[a-zA-Z0-9]{8}\b")

    assert my_regex.match(link) is not None




def test_create_link(mock_db_session):
    response = client.post(
        "/links/shorten",
        json={"url": "https://example.com"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["url"] == "https://example.com"




def test_get_link(mocker):
    # First create a link

    mocker.patch('api.v1.links.links.get_shortlink_by_code', return_value=ShortLink(url='google.com', usage_count=0,short_url='1234'))
    create_response = client.get(
        f"/links/123",
    )
    link = create_response.json()

    assert link=='google.com'


def test_link_delete(mocker):

    mocker.patch('auth.auth.get_user_secure', return_value=User(email='m@m.ru', password=123, login='123', token='123' ))
    
    mocker.patch('api.v1.links.links.get_shorlink_by_user_and_code', return_value=ShortLink(url='123444', usage_count=0,short_url='1234'))
    create_response = client.delete(
        f"/links/123",
        headers={
             "Authorization": f'Bearer 12344'
        }
    )
    assert create_response.status_code==200
    delete_result = create_response.json()

    assert delete_result==True



def test_link_put(mocker):

    mocker.patch('auth.auth.get_user_secure', return_value=User(email='m@m.ru', password=123, login='123', token='123' ))
    
    mocker.patch('api.v1.links.links.get_shorlink_by_user_and_code', return_value=ShortLink(url='123444', usage_count=0,short_url='1234'))
    create_response = client.put(
        f"/links/123",
        headers={
             "Authorization": f'Bearer 12344'
        },
        json={'short_code': 'code', 'url': 'url'}
    )
    assert create_response.status_code==200
    put_result = create_response.json()

    assert put_result['url'] == 'url'

    # ass
    # assert delete_result==True



def test_link_put(mocker):

    mocker.patch('auth.auth.get_user_secure', return_value=User(email='m@m.ru', password=123, login='123', token='123' ))
    
    mocker.patch('api.v1.links.links.get_shorlink_by_user_and_code', return_value=ShortLink(url='123444', usage_count=0,short_url='1234'))
    create_response = client.put(
        f"/links/123",
        headers={
             "Authorization": f'Bearer 12344'
        },
        json={'short_code': 'code', 'url': 'url'}
    )
    assert create_response.status_code==200
    put_result = create_response.json()

    assert put_result['url'] == 'url'

def test_link_stats(mocker):

    # mocker.patch('auth.auth.get_user_secure', return_value=User(email='m@m.ru', password=123, login='123', token='123' ))
    
    mocker.patch('api.v1.links.links.get_shortlink_by_code', return_value=ShortLink(url='123444', usage_count=100,short_url='1234'))
    create_response = client.get(
        f"/links/123/stats",
    )
    assert create_response.status_code==200
    stats = create_response.json()
    # print(stats)
    assert stats['redirects'] == 100
    assert stats['original_utl'] == '123444'

# @pytest.fixture
# def test_user():
#     # Create a test user in the database
#     db = TestingSessionLocal()
#     Base.metadata.create_all(engine)
#     print(  Base.metadata)
#     user = User(login="testuser", password='123',token='123')

#     db.add(user)
#     db.commit()
#     yield user
#     # Cleanup after test
#     db.delete(user)
#     db.commit()
#     db.close()


# def test_user():
#     # Create a test user in the database
#     db = override_get_db()
#     Base.metadata.create_all(engine)
#     user = User(login="testuser", password='123',token='123')

#     db.add(user)
#     db.commit()
#     assert user.login=='testuser'
#     assert user.id ==1
    


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
    

# def test_secured_route_success(test_user, monkeypatch):
    
#     # Set required environment variables
#     monkeypatch.setenv("TOKEN_KEY", "test_secret")
#     monkeypatch.setenv("TOKEN_ENV", "test")

#     # Obtain token
#     token_response = client.post(
#         "/token",
#         data={"username": "testuser", "password": "any"}
#     )
#     assert token_response.status_code == 200
#     access_token = token_response.json()["access_token"]

#     # Access secured endpoint
#     response = client.get(
#         "/secured",
#         headers={"Authorization": f"Bearer {access_token}"}
#     )
#     assert response.status_code == 200
#     assert response.json() is True