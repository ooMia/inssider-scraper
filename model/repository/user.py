from typing import Optional

from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, String, func
from sqlalchemy.orm import DeclarativeBase, relationship


def users_id_fk():
    return ForeignKey("users.id", ondelete="CASCADE")


class TimestampMixin:
    # fmt: off
    created_at = Column(DateTime, default=func.now(), doc="생성 시간")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), doc="수정 시간")
    # fmt: on


class Base(DeclarativeBase):
    pass


class Follow(Base, TimestampMixin):
    __tablename__ = "follows"

    # fmt: off
    from_user_id = Column(BigInteger, users_id_fk(), primary_key=True, doc="팔로우를 요청한 사용자 ID")
    to_user_id   = Column(BigInteger, users_id_fk(), primary_key=True, doc="팔로우 요청 대상의 사용자 ID")
    # fmt: on


class User(Base, TimestampMixin):
    __tablename__ = "users"

    # fmt: off
    id            = Column(BigInteger, primary_key=True, autoincrement=True)
    email         = Column(String(255), unique=True, doc="이메일 주소")
    password      = Column(String(255), doc="비밀번호 해싱값")
    password_salt = Column(String(255), doc="비밀번호 해싱용 salt")
    # fmt: on

    details = relationship(
        "UserDetail",
        back_populates="user",
        cascade="all, delete-orphan",  # User 삭제 시, UserDetail도 함께 삭제됨
        uselist=False,  # 1:1 관계
        info={"doc": "User와 UserDetail의 1:1 관계"},
    )

    following = relationship(
        "User",
        secondary="follows",  # M:N 관계
        primaryjoin=id == Follow.from_user_id,
        secondaryjoin=id == Follow.to_user_id,
        backref="followers",
        info={"doc": "User 간의 팔로우를 나타내는 M:N 관계"},
    )


class UserDetail(Base, TimestampMixin):
    __tablename__ = "user_details"

    # fmt: off
    user_id      = Column(BigInteger, users_id_fk(), primary_key=True, doc="users 테이블의 PK")
    username     = Column(String(255), nullable=True, doc="사용자 이름")
    introduction = Column(String(255), nullable=True, doc="자기소개")
    profile_url  = Column(String(255), nullable=True, doc="프로필 사진 URL")

    account_visibility   = Column(Boolean, default=True, doc="프로필 공개 여부")
    followers_visibility = Column(Boolean, default=True, doc="팔로워 목록 공개 여부")
    # fmt: on

    user = relationship("User", back_populates="details")
