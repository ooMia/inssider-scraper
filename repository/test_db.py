import unittest

from sqlalchemy import inspect

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
        self.assertIs(db1, db2, "Same connection parameters should return the same instance")

        db3 = DatabaseManager(database="meme")
        self.assertIsNot(db1, db3, "Different database names should return different instances")

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

    def test_user_insert_and_relationship(self):
        """User와 UserDetail의 삽입 및 관계 테스트"""

        with self.db_manager as session:
            user = User(
                email="test",
                password="a",
                password_salt="a",
                details=UserDetail(username="닉네임"),
            )
            session.add(user)
            session.commit()

        with self.db_manager as session:
            query_user = session.query(User).filter_by(email="test").first()
            query_detail = session.query(UserDetail).filter_by(username="닉네임").first()

            self.assertIsNotNone(query_user)
            self.assertIsNotNone(query_detail)

            if query_user is None or query_detail is None:
                self.fail("Neither user nor detail should be None")

            self.assertEqual(query_detail.user, query_user.details.user)
            self.assertEqual(query_user.details, query_detail.user.details)


if __name__ == "__main__":
    unittest.main()
