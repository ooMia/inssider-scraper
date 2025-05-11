import pytest

from model.repository import User
from repository.handler import DatabaseManager


def test_create_user():
    with DatabaseManager() as session:
        user = User(email="a@a.com", password="password", password_salt="salt")
        session.add(user)
        session.commit()

        # 데이터베이스에서 사용자 조회
        user = session.query(User).filter_by(email="a@a.com").first()
        assert user is not None
        assert user.id == 1
        assert user.email == "a@a.com"
        assert user.password == "password"
        assert user.password_salt == "salt"


if __name__ == "__main__":
    pytest.main()
