from dotenv import dotenv_values, load_dotenv
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from model.repository._base import Base

# .env 파일 로드
load_dotenv()


class DatabaseManager:
    """SQLAlchemy를 사용한 데이터베이스 관리자 클래스"""

    _engines = {}  # URL별로 엔진을 저장하는 클래스 변수

    def __init__(self, database=None, user=None, password=None, host=None, port=None):
        """
        환경 변수에서 설정을 가져와 데이터베이스 연결을 초기화합니다.
        매개변수를 제공하면 환경 변수보다 우선합니다.
        """
        # 환경 변수에서 설정 가져오기 (기본값 제공)
        envs = dotenv_values()
        db = database or envs.get("POSTGRES_DATABASE", "dev")
        user = user or envs.get("POSTGRES_USER", "user")
        pwd = password or envs.get("POSTGRES_PASSWORD", "user")
        port = port or envs.get("POSTGRES_PORT", "5432")

        # host 정규화: localhost와 127.0.0.1을 동일하게 처리
        host = host or envs.get("POSTGRES_HOST", "localhost")
        if host in ["localhost", "127.0.0.1"]:
            host = "localhost"  # 정규화된 값으로 통일

        # 데이터베이스 URL 생성 (엔진 키로 사용)
        self.db_url = f"postgresql+psycopg://{user}:{pwd}@{host}:{port}/{db}"

        # URL에 해당하는 엔진 가져오기 (없으면 새로 생성)
        if self.db_url not in self._engines:
            self._engines[self.db_url] = create_engine(self.db_url, echo=False)
        self.engine: Engine = self._engines[self.db_url]

    def __enter__(self):
        """컨텍스트 매니저 진입 시 호출됩니다."""
        self.session = scoped_session(sessionmaker(bind=self.engine))
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        """컨텍스트 매니저 종료 시 호출됩니다."""
        if exc_type is not None:
            self.session.rollback()
            print(f"세션 롤백: {exc_val}")
        else:
            self.session.commit()
        self.session.close()

    def create_tables(self):
        """모든 모델의 테이블을 생성합니다."""
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        """모든 테이블을 삭제합니다."""
        Base.metadata.drop_all(self.engine)


if __name__ == "__main__":
    from sqlalchemy.schema import CreateTable

    def _ddl():
        res = ""
        engine = create_engine("sqlite:///:memory:")
        for table in Base.metadata.sorted_tables:
            ddl = str(CreateTable(table).compile(engine))
            res += f"{ddl.strip()};\n"
        return res

    print(_ddl())
