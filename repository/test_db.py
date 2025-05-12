import pytest

from repository.handler import DatabaseManager


@pytest.fixture
def db_engine():
    db = DatabaseManager()
    db.drop_tables()
    db.create_tables()
    print("Database tables created")
    return db.engine


def test_singleton():
    db1 = DatabaseManager()
    db2 = DatabaseManager()
    assert db1.engine is db2.engine, "Same connection parameters should return the same engine"

    db3 = DatabaseManager(database="meme")
    assert db1.engine is not db3.engine, "Different database names should return different engines"

    db4 = DatabaseManager(host="localhost")
    db5 = DatabaseManager(host="127.0.0.1")
    assert db1.engine is db4.engine, "default host should be equal to localhost"
    assert db4.engine is db5.engine, "127.0.0.1 and localhost should be equal"


@pytest.mark.usefixtures("db_engine")
def test_create_table(db_engine):
    from sqlalchemy import inspect

    inspector = inspect(db_engine.engine)
    table_names = inspector.get_table_names()

    print("Table names:", table_names)

    assert "users" in table_names
    assert "user_details" in table_names
    assert "follows" in table_names
    assert "posts" in table_names
    assert "videos" in table_names


if __name__ == "__main__":
    pytest.main()
