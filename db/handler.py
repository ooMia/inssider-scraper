from dotenv import dotenv_values, load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from db.model import Base

# .env 파일 로드
load_dotenv()
envs = dotenv_values()


class DatabaseManager:
    """SQLAlchemy를 사용한 데이터베이스 관리자 클래스"""

    def __init__(self, database=None, user=None, password=None, host=None, port=None):
        """
        환경 변수에서 설정을 가져와 데이터베이스 연결을 초기화합니다.
        매개변수를 제공하면 환경 변수보다 우선합니다.
        """
        # 환경 변수에서 설정 가져오기 (기본값 제공)
        db = database or envs.get("MYSQL_DATABASE", "dev")
        user = user or envs.get("MYSQL_USER", "user")
        pwd = password or envs.get("MYSQL_PASSWORD", "user")
        host = host or envs.get("MYSQL_HOST", "localhost")
        port = port or envs.get("MYSQL_PORT", "3306")

        # 데이터베이스 URL 생성
        self.db_url = f"mysql+mysqlconnector://{user}:{pwd}@{host}:{port}/{db}"

        # 엔진 및 세션 팩토리 초기화
        self.engine = create_engine(self.db_url, echo=True)

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
