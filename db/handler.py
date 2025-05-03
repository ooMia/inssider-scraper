import os

import mysql.connector
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


class MySQLDB:
    def __init__(self, database=None, user=None, password=None, host=None, port=None):
        """
        환경 변수에서 설정을 가져와 데이터베이스 연결을 초기화합니다.
        매개변수를 제공하면 환경 변수보다 우선합니다.
        """
        # 환경 변수에서 설정 가져오기 (기본값 제공)
        self.conn_params = {
            "database": database or os.getenv("MYSQL_DATABASE", "dev"),
            "user": user or os.getenv("MYSQL_USER", "user"),
            "password": password or os.getenv("MYSQL_PASSWORD", "user"),
            "host": host or os.getenv("MYSQL_HOST", "localhost"),
            "port": int(port or os.getenv("MYSQL_PORT", "3306"))
        }
        self.conn = None
        self.cursor = None

    def connect(self):
        """MySQL 데이터베이스에 연결합니다."""
        try:
            self.conn = mysql.connector.connect(**self.conn_params)
            self.cursor = self.conn.cursor()
            print(f"데이터베이스 '{self.conn_params['database']}'에 연결되었습니다.")
            return self.conn
        except mysql.connector.Error as err:
            print(f"데이터베이스 연결 오류: {err}")
            raise

    def close(self):
        """데이터베이스 연결을 종료합니다."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def execute(self, query, params=()):
        """쿼리를 실행합니다."""
        if not self.conn:
            self.connect()
        self.cursor.execute(query, params)
        return self.cursor

    def commit(self):
        """변경사항을 커밋합니다."""
        if self.conn:
            self.conn.commit()


if __name__ == "__main__":
    # 예시 사용법
    db = MySQLDB()
    try:
        db.connect()
        # 쿼리 실행 예시
        db.execute("CREATE TABLE IF NOT EXISTS dev (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")
        db.execute("INSERT INTO dev (name) VALUES (%s)", ("example",))
        db.commit()
        db.execute("SELECT * FROM dev")
        results = db.cursor.fetchall()
        for row in results:
            print(row)
    finally:
        db.close()
