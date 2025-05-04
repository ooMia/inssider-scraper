from sqlalchemy import inspect
from sqlalchemy.orm.scoping import scoped_session

from db.deprecated_model import Address, Dev, User
from db.handler import DatabaseManager


def test_create_table():
    db_manager = DatabaseManager()
    # 기존 테이블 삭제 후 재생성
    db_manager.drop_tables()
    db_manager.create_tables()

    inspector = inspect(db_manager.engine)
    table_names = inspector.get_table_names()

    assert 'dev' in table_names, "Table 'dev' should be created"
    assert 'user_account' in table_names, "Table 'user_account' should be created"
    assert 'address' in table_names, "Table 'address' should be created"


def test_insert_and_read():
    db_manager = DatabaseManager()

    def count_records(session: scoped_session):
        return session.query(Dev).filter_by(name="test_name").count()

    with db_manager as session:
        initial_count = count_records(session)
        new_dev = Dev(name="test_name")
        session.add(new_dev)

    with db_manager as session:
        new_count = count_records(session)
        assert new_count == initial_count + 1, "Record count should increase by 1"


def test_relationships():
    """관계 설정이 올바르게 되었는지 테스트합니다."""
    db_manager = DatabaseManager()

    with db_manager as session:
        # 사용자 생성
        user = User(name="test_user", fullname="Test User")

        # 주소 추가
        Address(email_address="test1@example.com", user=user)
        Address(email_address="test2@example.com", user=user)

        # 데이터베이스에 저장
        session.add(user)

    # 새 세션에서 관계 확인
    with db_manager as session:
        loaded_user = session.query(User).filter_by(name="test_user").first()
        assert loaded_user is not None, "User should be saved"
        assert len(loaded_user.addresses) == 2, "User should have 2 addresses"

        # 관계의 양방향 확인
        for address in loaded_user.addresses:
            assert address.user is loaded_user, "Address should reference back to user"
