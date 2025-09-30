from dataclasses import asdict

from sqlalchemy import select

from app.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as mocked_time:
        new_user = User(
            username='john.doe', email='john@example.com', password='secret'
        )
        session.add(new_user)
        session.commit()

        user = session.scalar(select(User).where(User.username == 'john.doe'))

    assert asdict(user) == {
        'id': 1,
        'username': 'john.doe',
        'email': 'john@example.com',
        'password': 'secret',
        'created_at': mocked_time,
        'updated_at': mocked_time,
    }
