import unittest

from sqlalchemy import inspect
from sqlalchemy.orm.scoping import scoped_session

from repository.deprecated_model import Address, Dev, User
from repository.handler import DatabaseManager


class TestDatabase(unittest.TestCase):

    def setUp(self):
        """각 테스트 실행 전에 호출되는 메서드"""
        self.db_manager = DatabaseManager()

    def test_singleton(self):
        """URL 기반 싱글톤 패턴이 올바르게 작동하는지 테스트합니다."""
        db1 = DatabaseManager()
        db2 = DatabaseManager()
        self.assertIs(
            db1, db2, "Same connection parameters should return the same instance"
        )

        db3 = DatabaseManager(database="meme")
        self.assertIsNot(
            db1, db3, "Different database names should return different instances"
        )

        db4 = DatabaseManager(host="localhost")
        db5 = DatabaseManager(host="127.0.0.1")
        self.assertIs(db1, db4, "default host should be equal to localhost")
        self.assertIs(db4, db5, "127.0.0.1 and localhost should be equal")

    def test_create_table(self):
        """테이블이 올바르게 생성되는지 테스트합니다."""
        # 기존 테이블 삭제 후 재생성
        self.db_manager.drop_tables()
        self.db_manager.create_tables()

        inspector = inspect(self.db_manager.engine)
        table_names = inspector.get_table_names()

        self.assertIn("dev", table_names, "Table 'dev' should be created")
        self.assertIn(
            "user_account", table_names, "Table 'user_account' should be created"
        )
        self.assertIn("address", table_names, "Table 'address' should be created")

    def test_insert_and_read(self):
        """레코드 삽입과 읽기가 정상적으로 작동하는지 테스트합니다."""

        def count_records(session: scoped_session):
            return session.query(Dev).filter_by(name="test_name").count()

        with self.db_manager as session:
            initial_count = count_records(session)
            new_dev = Dev(name="test_name")
            session.add(new_dev)

        with self.db_manager as session:
            new_count = count_records(session)
            self.assertEqual(
                new_count, initial_count + 1, "Record count should increase by 1"
            )

    def test_relationships(self):
        """관계 설정이 올바르게 되었는지 테스트합니다."""
        with self.db_manager as session:
            # 사용자 생성
            user = User(name="test_user", fullname="Test User")

            # 주소 추가
            Address(email_address="test1@example.com", user=user)
            Address(email_address="test2@example.com", user=user)

            # 데이터베이스에 저장
            session.add(user)

        # 새 세션에서 관계 확인
        with self.db_manager as session:
            loaded_user = session.query(User).filter_by(name="test_user").first()
            self.assertIsNotNone(loaded_user, "User should be saved")
            self.assertEqual(
                len(loaded_user.addresses), 2, "User should have 2 addresses"
            )

            # 관계의 양방향 확인
            for address in loaded_user.addresses:
                self.assertIs(
                    address.user, loaded_user, "Address should reference back to user"
                )


if __name__ == "__main__":
    unittest.main()
