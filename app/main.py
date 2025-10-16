from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.database import get_session
from app.models import User
from app.schemas import Message, UserList, UserPublic, UserSchema

app = FastAPI(title='Learn FastAPI', version='0.1.0')
database = []


@app.get('/', response_model=Message)
async def read_root():
    return {'message': 'Hello World'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.email == user.email) | (User.username == user.username)
        )
    )

    if db_user:
        if user.email == db_user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Email already exists'
            )
        elif user.username == db_user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Username already exists'
            )

    # Create user in the database
    db_user = User(email=user.email, username=user.username, password=user.password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', response_model=UserList)
def list_users(limit: int = 10, offset: int = 0, session=Depends(get_session)):
    users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': users}


@app.get('/users/{userId}/', response_model=UserPublic)
def get_user(userId: int, session=Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == userId))
    if not user_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    return user_db


@app.put('/users/{userId}/', response_model=UserPublic)
def update_user(userId: int, user: UserSchema, session=Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == userId))
    if not user_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    try:
        user_db.username = user.username
        user_db.email = user.email
        user_db.password = user.password

        session.add(user_db)
        session.commit()
        session.refresh(user_db)

        return user_db
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Username or Email already exists'
        )


@app.delete('/users/{userId}/', response_model=Message)
def delete_user(userId: int, session=Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == userId))
    if not user_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    session.delete(user_db)
    session.commit()

    return {'message': 'User deleted successfully'}


# @app.get('/items/{item_id}')
# async def read_item(item_id: int, q: str = None):
#     return {'item_id': item_id, 'q': q}
