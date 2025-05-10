from sqlalchemy import Column, DateTime, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at = Column(DateTime, default=func.now(), doc="생성 시간")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), doc="수정 시간")


def users_id_fk():
    return ForeignKey("users.id", ondelete="CASCADE")
