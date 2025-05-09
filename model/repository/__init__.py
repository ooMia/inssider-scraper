"""
Conventions

클래스명은 카멜 케이스, 테이블은 파스칼 케이스로 작성합니다.
클래스명은 단수형, 테이블명은 복수형을 사용합니다.
예시: 클래스 UserDetail, 테이블 user_details

"""

from sqlalchemy import Column, DateTime, func


class TimestampMixin:
    # fmt: off
    created_at = Column(DateTime, default=func.now(), doc="생성 시간")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), doc="수정 시간")
    # fmt: on
