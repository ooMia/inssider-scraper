from typing import Optional

from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    # fmt: off
    id       = Column(BigInteger, primary_key=True, autoincrement=True)
    email    = Column(String(255), immutable=True, unique=True)
    password = Column(String(255))  # 해싱된 비밀번호
    salt     = Column(String(255))  # 비밀번호 해싱용 salt
    # fmt: on

    details = relationship(
        "UserDetail", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )


class UserDetail(Base):
    __tablename__ = "user_details"

    # fmt: off
    user_id      = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    username     = Column(Optional(String(255)))  # 사용자 이름
    introduction = Column(Optional(String(255)))  # 자기소개
    profile_url  = Column(Optional(String(255)))  # 프로필 사진 URL

    account_visibility   = Column(Boolean, default=True)  # 프로필 공개 여부
    followers_visibility = Column(Boolean, default=True)  # 팔로워 목록 공개 여부
    # fmt: on

    user = relationship("User", back_populates="details")
