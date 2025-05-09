import unittest

from sqlalchemy import inspect
from sqlalchemy.orm.scoping import scoped_session

from model.repository import User, UserDetail
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
        self.db_manager.drop_tables()
        self.db_manager.create_tables()

        inspector = inspect(self.db_manager.engine)
        table_names = inspector.get_table_names()

        self.assertIn("users", table_names)
        self.assertIn("user_details", table_names)
        self.assertIn("follows", table_names)
        self.assertIn("posts", table_names)
        self.assertIn("videos", table_names)

    def test_insert_and_read(self):
        """레코드 삽입과 읽기가 정상적으로 작동하는지 테스트합니다."""

        def count_records(session: scoped_session):
            return session.query(User).filter_by(email="test").count()

        with self.db_manager as session:
            initial_count = count_records(session)
            initial_user = User(email="test", password="a", password_salt="a")
            initial_user.details = UserDetail(username="닉네임")
            session.add(initial_user)

        with self.db_manager as session:
            new_count = count_records(session)
            self.assertEqual(
                new_count, initial_count + 1, "Record count should increase by 1"
            )

    def test_relationships(self):
        """관계 설정이 올바르게 되었는지 테스트합니다."""

        with self.db_manager as session:
            user = User(
                email="a@a.com",
                password="hashed",
                password_salt="salt",
                details=UserDetail(username="닉네임"),
            )
            self.assertEqual(user, user.details.user, "back_populates should work")
            session.add(user)

        # 새 세션에서 관계 확인
        # with self.db_manager as session:
        #     loaded_user = session.query(User).filter_by(name="test_user").first()
        #     self.assertIsNotNone(loaded_user, "User should be saved")
        #     self.assertEqual(
        #         len(loaded_user.addresses), 2, "User should have 2 addresses"
        #     )

        #     # 관계의 양방향 확인
        #     for address in loaded_user.addresses:
        #         self.assertIs(
        #             address.user, loaded_user, "Address should reference back to user"
        #         )


if __name__ == "__main__":
    unittest.main()
