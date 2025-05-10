from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model.repository import Post

from sqlalchemy import BigInteger, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.repository._base import Base, TimestampMixin, users_id_fk


class Follow(Base, TimestampMixin):
    __tablename__ = "follows"

    from_user_id: Mapped[int] = mapped_column(
        BigInteger, users_id_fk(), primary_key=True, doc="팔로우를 요청한 사용자 ID"
    )
    to_user_id: Mapped[int] = mapped_column(
        BigInteger, users_id_fk(), primary_key=True, doc="팔로우 요청 대상의 사용자 ID"
    )


class UserDetail(Base, TimestampMixin):
    __tablename__ = "user_details"

    user_id: Mapped[int] = mapped_column(
        BigInteger, users_id_fk(), primary_key=True, doc="users 테이블 PK"
    )
    username: Mapped[str | None] = mapped_column(String(255), nullable=True, doc="사용자 이름")
    introduction: Mapped[str | None] = mapped_column(String(255), nullable=True, doc="자기소개")
    profile_url: Mapped[str | None] = mapped_column(String(255), nullable=True, doc="프로필 URL")
    account_visibility: Mapped[bool] = mapped_column(Boolean, default=True, doc="프로필 공개 여부")
    follower_visibility: Mapped[bool] = mapped_column(Boolean, default=True, doc="팔로워 공개 여부")

    user: Mapped["User"] = relationship("User", back_populates="details")


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, doc="이메일 주소")
    password: Mapped[str] = mapped_column(String(255), doc="비밀번호 해싱값")
    password_salt: Mapped[str] = mapped_column(String(255), doc="비밀번호 해싱용 salt")

    details: Mapped["UserDetail"] = relationship(
        "UserDetail",
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
        info={"doc": "User와 UserDetail의 1:1 관계"},
    )

    following: Mapped[list["Follow"]] = relationship(
        "User",
        secondary="follows",
        primaryjoin=id == Follow.from_user_id,
        secondaryjoin=id == Follow.to_user_id,
        backref="followers",
        info={"doc": "User가 팔로우하는 User 목록"},
    )

    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="user",
        cascade="all, delete-orphan",
        info={"doc": "User와 Post 간의 1:N 관계"},
    )
