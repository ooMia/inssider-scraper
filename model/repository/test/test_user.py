from datetime import timedelta
from zoneinfo import ZoneInfo

import pytest
from sqlalchemy import text

from model.repository import User
from repository.handler import DatabaseManager


@pytest.fixture(scope="function", autouse=True)
def reset_db():
    DatabaseManager().drop_tables()
    DatabaseManager().create_tables()


@pytest.fixture
def sample_users():
    return [
        User(email="user1@test.com", password="pw1", password_salt="salt1"),
        User(email="user2@test.com", password="pw2", password_salt="salt2"),
        User(email="user3@test.com", password="pw3", password_salt="salt3"),
    ]


def test_create_user(sample_users: list[User]):
    with DatabaseManager() as session:
        session.add(sample_users[0])
        session.commit()

        user = session.query(User).first()
        assert user is not None
        assert user.id == 1
        assert user.email == "user1@test.com"
        assert user.password == "pw1"
        assert user.password_salt == "salt1"
        assert user.details is None
        assert user.following == []

        # check if record is created within the last 5 seconds
        current_time = session.execute(text("SELECT NOW()")).scalar()
        user_created_at = user.created_at.replace(tzinfo=ZoneInfo("UTC"))
        tolerance = timedelta(seconds=5)
        assert (current_time - tolerance) <= user_created_at


def test_create_multiple_users(sample_users: list[User]):
    with DatabaseManager() as session:
        session.add_all(sample_users)
        session.commit()

        users = session.query(User).all()
        assert len(users) == 3


def test_update_user_password(sample_users: list[User]):
    with DatabaseManager() as session:
        user = sample_users[0]
        session.add(user)
        session.commit()

        user.email = "update@test.com"
        user.password = "newpw"
        user.password_salt = "newsalt"
        session.commit()

        updated = session.query(User).filter_by(email="update@test.com").first()
        assert updated is not None
        assert updated.id == user.id
        assert updated.email == "update@test.com"
        assert updated.password == "newpw"
        assert updated.password_salt == "newsalt"


def test_delete_user(sample_users: list[User]):
    with DatabaseManager() as session:
        user = sample_users[0]
        session.add(user)
        session.commit()

        session.delete(user)
        session.commit()

        deleted = session.query(User).first()
        assert deleted is None


def test_error_duplicated_email(sample_users: list[User]):
    from psycopg.errors import UniqueViolation
    from sqlalchemy.exc import IntegrityError

    with pytest.raises(IntegrityError) as exc_info:
        with DatabaseManager() as session:
            user1 = sample_users[0]
            session.add(user1)
            session.commit()

            # Error occurs when trying to add a user with the same email
            user2 = sample_users[1]
            user2.email = user1.email
            session.add(user2)
            session.commit()

    assert isinstance(exc_info.value.orig, UniqueViolation)


def test_error_long_email():
    from psycopg.errors import StringDataRightTruncation
    from sqlalchemy.exc import DataError

    with pytest.raises(DataError) as exc_info:
        with DatabaseManager() as session:
            long_email = "a" * 255 + "@test.com"
            user = User(email=long_email, password="pw", password_salt="salt")
            session.add(user)
            session.commit()

            fetched = session.query(User).first()
            assert fetched is not None
            assert fetched.email == long_email

    assert isinstance(exc_info.value.orig, StringDataRightTruncation)


if __name__ == "__main__":
    import os

    pytest.main([os.path.abspath(__file__)])
