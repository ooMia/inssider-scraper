from dotenv import dotenv_values, load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# .env 파일 로드
load_dotenv()
envs = dotenv_values()

from model.repository._base import Base


class DatabaseManager:
    """SQLAlchemy를 사용한 데이터베이스 관리자 클래스"""

    _instances = {}  # URL별로 인스턴스를 저장하는 클래스 변수

    def __new__(cls, database=None, user=None, password=None, host=None, port=None):
        """URL 기반으로 싱글톤 인스턴스를 생성하거나 반환"""
        # 환경 변수에서 설정 가져오기 (기본값 제공)
        db = database or envs.get("MYSQL_DATABASE", "dev")
        user = user or envs.get("MYSQL_USER", "user")
        pwd = password or envs.get("MYSQL_PASSWORD", "user")
        port = port or envs.get("MYSQL_PORT", "3306")

        # host 정규화: localhost와 127.0.0.1을 동일하게 처리
        host = host or envs.get("MYSQL_HOST", "localhost")
        if host in ["localhost", "127.0.0.1"]:
            host = "localhost"  # 정규화된 값으로 통일

        # 데이터베이스 URL 생성 (인스턴스 키로 사용)
        db_url = f"mysql+mysqlconnector://{user}:{pwd}@{host}:{port}/{db}"

        # URL에 해당하는 인스턴스 가져오기 (없으면 None)
        instance = cls._instances.get(db_url)

        # 인스턴스가 없으면 새로 생성
        if instance is None:
            instance = super(DatabaseManager, cls).__new__(cls)
            instance._db_url = db_url
            instance._initialized = False
            cls._instances[db_url] = instance

        return instance

    def __init__(self, **kwargs):
        """
        환경 변수에서 설정을 가져와 데이터베이스 연결을 초기화합니다.
        매개변수를 제공하면 환경 변수보다 우선합니다.
        """
        # 이미 초기화된 인스턴스인 경우 중복 초기화 방지
        if getattr(self, "_initialized", False):
            return

        self.db_url = self._db_url
        self.engine = create_engine(self.db_url, echo=False)  # 디버깅을 위해 echo=True로 설정 가능

        # 초기화 완료 표시
        self._initialized = True

    def create_tables(self):
        """모든 모델의 테이블을 생성합니다."""
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        """모든 모델의 테이블을 삭제합니다."""
        Base.metadata.drop_all(self.engine)

    def __enter__(self):
        """컨텍스트 매니저 진입 시 호출됩니다."""
        self.session = scoped_session(sessionmaker(bind=self.engine))
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        """컨텍스트 매니저 종료 시 호출됩니다."""
        if exc_type is not None:
            # 예외가 발생한 경우 롤백
            self.session.rollback()
            print(f"세션 롤백: {exc_val}")
        else:
            # 예외가 없으면 커밋
            self.session.commit()
        self.session.close()


if __name__ == "__main__":

    def print_ddl():
        from sqlalchemy import create_engine
        from sqlalchemy.schema import CreateTable

        engine = create_engine("sqlite:///:memory:")
        for table in Base.metadata.sorted_tables:
            ddl = str(CreateTable(table).compile(engine))
            print(f"{ddl};")

    print_ddl()
