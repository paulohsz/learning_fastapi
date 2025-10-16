from http import HTTPStatus

from app.schemas import UserPublic


def test_read_root(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello World'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'John',
            'email': 'john@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'John',
        'email': 'john@example.com',
    }


def test_create_user_integrity_email_error(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'John',
            'email': 'john.doe@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_create_user_integrity_username_error(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'john.doe',
            'email': 'john@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_list_user_without_user(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_list_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1/',
        json={
            'username': 'John Doe',
            'email': 'john@example.com',
            'password': 'new_secret',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'John Doe',
        'email': 'john@example.com',
    }


def test_get_user(client, user):
    response = client.get('/users/1/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'john.doe',
        'email': 'john.doe@example.com',
    }


def test_get_user_failed(client):
    response = client.get('/users/999/')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user_failed(client):
    response = client.put(
        '/users/-1/',
        json={
            'username': 'John Doe',
            'email': 'john.doe@example.com',
            'password': 'new_secret',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_integrity_error(client, user):
    # Create another user
    client.post(
        '/users/',
        json={
            'username': 'jane.doe',
            'email': 'jane.doe@example.com',
            'password': 'secret',
        },
    )
    # Try to update the first user with the email of the second user
    response = client.put(
        f'/users/{user.id}/',
        json={
            'username': 'jane.doe',
            'email': 'john.doe@example.com',
            'password': 'new_secret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or Email already exists'}


def test_delete_user(client, user):
    response = client.delete('/users/1/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted successfully'}


def test_delete_user_failed(client):
    response = client.delete('/users/999/')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


# def test_read_item():
#     response = client.get("/items/42?q=test")
#     assert response.status_code == 200
#     assert response.json() == {"item_id": 42, "q": "test"}
