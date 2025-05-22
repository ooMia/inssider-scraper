from datetime import timedelta
from zoneinfo import ZoneInfo

import pytest
from sqlalchemy import text

from model.repository import Account
from repository.handler import DatabaseManager


@pytest.fixture(scope="function", autouse=True)
def reset_db():
    DatabaseManager().drop_tables()
    DatabaseManager().create_tables()


@pytest.fixture
def sample_accounts():
    return [
        Account(email="account1@test.com", password="pw1", password_salt="salt1"),
        Account(email="account2@test.com", password="pw2", password_salt="salt2"),
        Account(email="account3@test.com", password="pw3", password_salt="salt3"),
    ]


def test_create_account(sample_accounts: list[Account]):
    with DatabaseManager() as session:
        session.add(sample_accounts[0])
        session.commit()

        account = session.query(Account).first()
        assert account is not None
        assert account.id == 1
        assert account.email == "account1@test.com"
        assert account.password == "pw1"
        assert account.password_salt == "salt1"
        assert account.details is None
        assert account.following == []

        # check if record is created within the last 5 seconds
        current_time = session.execute(text("SELECT NOW()")).scalar()
        account_created_at = account.created_at.replace(tzinfo=ZoneInfo("UTC"))
        tolerance = timedelta(seconds=5)
        assert (current_time - tolerance) <= account_created_at


def test_create_multiple_accounts(sample_accounts: list[Account]):
    with DatabaseManager() as session:
        session.add_all(sample_accounts)
        session.commit()

        accounts = session.query(Account).all()
        assert len(accounts) == 3


def test_update_account_password(sample_accounts: list[Account]):
    with DatabaseManager() as session:
        account = sample_accounts[0]
        session.add(account)
        session.commit()

        account.email = "update@test.com"
        account.password = "newpw"
        account.password_salt = "newsalt"
        session.commit()

        updated = session.query(Account).filter_by(email="update@test.com").first()
        assert updated is not None
        assert updated.id == account.id
        assert updated.email == "update@test.com"
        assert updated.password == "newpw"
        assert updated.password_salt == "newsalt"


def test_delete_account(sample_accounts: list[Account]):
    with DatabaseManager() as session:
        account = sample_accounts[0]
        session.add(account)
        session.commit()

        session.delete(account)
        session.commit()

        deleted = session.query(Account).first()
        assert deleted is None


def test_error_duplicated_email(sample_accounts: list[Account]):
    from psycopg.errors import UniqueViolation
    from sqlalchemy.exc import IntegrityError

    with pytest.raises(IntegrityError) as exc_info:
        with DatabaseManager() as session:
            account1 = sample_accounts[0]
            session.add(account1)
            session.commit()

            # Error occurs when trying to add a account with the same email
            account2 = sample_accounts[1]
            account2.email = account1.email
            session.add(account2)
            session.commit()

    assert isinstance(exc_info.value.orig, UniqueViolation)


def test_error_long_email():
    from psycopg.errors import StringDataRightTruncation
    from sqlalchemy.exc import DataError

    with pytest.raises(DataError) as exc_info:
        with DatabaseManager() as session:
            long_email = "a" * 255 + "@test.com"
            account = Account(email=long_email, password="pw", password_salt="salt")
            session.add(account)
            session.commit()

            fetched = session.query(Account).first()
            assert fetched is not None
            assert fetched.email == long_email

    assert isinstance(exc_info.value.orig, StringDataRightTruncation)


if __name__ == "__main__":
    import os

    pytest.main([os.path.abspath(__file__)])
