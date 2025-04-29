import mysql.connector
import pytest

from db import MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, MYSQL_PORT, MYSQL_HOST


@pytest.fixture(scope="module")
def db_connection():
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )
    yield conn
    conn.close()


def test_table_exist(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SHOW TABLES")
    result = cursor.fetchall()
    cursor.close()

    tables = ['company', 'keyword', 'recruit', 'investment']
    for table in tables:
        assert (table,) in result


def test_error_on_non_exist_company(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM company WHERE id = (%s)", ("0",))
    result = cursor.fetchall()
    cursor.close()
    assert len(result) == 0


def test_example(db_connection):
    from db.CompanyDB import CompanyDB
    from scrape.model import Company
    db = CompanyDB(db_connection)
    result: Company = db.load_company_by_name("쿠팡")
    assert result.id == "CP00000055"
    assert result.name == "쿠팡"
    assert "커머스" in result.keyword
    assert result.investment.stage == "IPO"
    assert len(result.recruit.detail) > 0
