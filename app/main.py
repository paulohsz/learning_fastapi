from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from app.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI(title='Learn FastAPI', version='0.1.0')
database = []


@app.get('/', response_model=Message)
async def read_root():
    return {'message': 'Hello World'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    userWithId = UserDB(id=len(database) + 1, **user.model_dump())
    database.append(userWithId)
    return userWithId


@app.get('/users/', response_model=UserList)
def list_users():
    return {'users': database}
    # return {'users': [UserPublic(**user.model_dump()) for user in database]}


@app.get('/users/{userId}/', response_model=UserPublic)
def get_user(userId: int):
    user = None
    for u in database:
        if u.id == userId:
            user = u
            break

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return user


@app.put('/users/{userId}/', response_model=UserPublic)
def update_user(userId: int, user: UserSchema):
    if userId < 0 or userId > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    userWithId = UserDB(id=userId, **user.model_dump())
    database[userId - 1] = userWithId
    return userWithId


@app.delete('/users/{userId}/', response_model=UserPublic)
def delete_user(userId: int):
    user = None
    for u in database:
        if u.id == userId:
            user = u
            break

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    database.remove(user)
    return user


# @app.get('/items/{item_id}')
# async def read_item(item_id: int, q: str = None):
#     return {'item_id': item_id, 'q': q}
