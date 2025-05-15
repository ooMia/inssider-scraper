from sqlalchemy import Boolean, Column, DateTime, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at = Column(DateTime, default=func.now(), doc="생성 시간")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), doc="수정 시간")


class SoftDeleteMixin:
    deleted_at = Column(DateTime, nullable=True, doc="삭제 시간")
    is_deleted = Column(Boolean, default=False, doc="삭제 여부")


class SoftDeleteTimestampMixin(TimestampMixin, SoftDeleteMixin):
    __abstract__ = True
    __table_args__ = ({"extend_existing": True},)

    def soft_delete(self):
        self.deleted_at = func.now()
        self.is_deleted = True


def users_id_fk():
    return ForeignKey("users.id", ondelete="CASCADE")


def posts_id_fk():
    return ForeignKey("posts.id")
