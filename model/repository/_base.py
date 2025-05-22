from datetime import datetime, timedelta

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at = Column(DateTime, insert_default=func.now(), doc="생성 시간")
    updated_at = Column(DateTime, insert_default=func.now(), onupdate=func.now(), doc="수정 시간")


class SoftDeleteMixin:
    deleted_at = Column(DateTime, nullable=True, doc="삭제 시간")
    is_deleted = Column(Boolean, default=False, doc="삭제 여부")


class ExpirationTimestampMixin:
    created_at = Column(DateTime, insert_default=func.now(), doc="생성 날짜")
    expired_at = Column(
        DateTime,
        insert_default=lambda: func.now() + timedelta(minutes=5),
        doc="만료 날짜",
    )


class SoftDeleteTimestampMixin(TimestampMixin, SoftDeleteMixin):
    __abstract__ = True
    __table_args__ = ({"extend_existing": True},)

    def soft_delete(self):
        self.deleted_at = func.now()
        self.is_deleted = True


def accounts_id_fk():
    return ForeignKey("accounts.id", ondelete="CASCADE")


def posts_id_fk():
    return ForeignKey("posts.id")
