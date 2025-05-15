from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model.repository import Post

from sqlalchemy import BigInteger, Boolean, String, Text
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from model.repository._base import Base, SoftDeleteTimestampMixin, users_id_fk


class Like(MappedAsDataclass, Base, SoftDeleteTimestampMixin):
    __tablename__ = "likes"
    from enum import Enum

    class LikeTargetType(str, Enum):
        POST = "post"
        COMMENT = "comment"

    # 1. PK (init=False)
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, init=False)
    user_id: Mapped[int] = mapped_column(BigInteger, users_id_fk(), nullable=False, init=False)

    # 2. 필수값 (init=True, 디폴트 없음)
    target_type: Mapped[LikeTargetType] = mapped_column(String(50), nullable=False, init=True)
    target_id: Mapped[int] = mapped_column(BigInteger, nullable=False, init=True)

    # 3. 관계 (init=True, default=None)
    user: Mapped["User"] = relationship(
        "User",
        back_populates="likes",
        init=True,
        default=None,
        uselist=False,
        info={"doc": "Like를 누른 사용자"},
    )

    # 4. 제약조건
    from sqlalchemy import UniqueConstraint

    __table_args__ = (
        UniqueConstraint("user_id", "target_type", "target_id", name="uq_like_user_target"),
    )


class Follow(MappedAsDataclass, Base, SoftDeleteTimestampMixin):
    __tablename__ = "follows"

    from_user_id: Mapped[int] = mapped_column(
        BigInteger, users_id_fk(), primary_key=True, doc="팔로우를 요청한 사용자 ID"
    )
    to_user_id: Mapped[int] = mapped_column(
        BigInteger, users_id_fk(), primary_key=True, doc="팔로우 요청 대상의 사용자 ID"
    )


class UserDetail(MappedAsDataclass, Base, SoftDeleteTimestampMixin):
    __tablename__ = "user_details"

    # 1. PK (user_id, init=False)
    user_id: Mapped[int] = mapped_column(
        BigInteger, users_id_fk(), primary_key=True, doc="users 테이블 PK", init=False
    )

    # 2. 선택값 (default=None)
    introduction: Mapped[str | None] = mapped_column(
        Text, nullable=True, doc="자기소개", default=None
    )
    profile_url: Mapped[str | None] = mapped_column(
        String(255), nullable=True, doc="프로필 URL", default=None
    )
    username: Mapped[str | None] = mapped_column(
        String(255), nullable=True, doc="사용자 이름", default=None
    )

    # 3. 관계 (init=True, default=None)
    user: Mapped["User"] = relationship(
        "User",
        back_populates="details",
        init=True,
        default=None,
        uselist=False,
    )

    # 4. 옵션 (default=True)
    account_visibility: Mapped[bool] = mapped_column(Boolean, default=True, doc="프로필 공개 여부")
    follower_visibility: Mapped[bool] = mapped_column(Boolean, default=True, doc="팔로워 공개 여부")


class User(MappedAsDataclass, Base, SoftDeleteTimestampMixin):
    __tablename__ = "users"

    # 1. PK (init=False)
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        init=False,
    )

    # 2. 필수값 (init=True, 디폴트 없음)
    email: Mapped[str] = mapped_column(String(255), unique=True, doc="이메일 주소")
    password: Mapped[str] = mapped_column(String(255), doc="비밀번호 해싱값")
    password_salt: Mapped[str] = mapped_column(String(255), doc="비밀번호 해싱용 salt")

    # 3. 관계 필드 (init=False, 객체지향적 사용)
    details: Mapped["UserDetail"] = relationship(
        "UserDetail",
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
        init=False,
        info={"doc": "User와 UserDetail의 1:1 관계"},
    )

    following: Mapped[list["Follow"]] = relationship(
        "User",
        secondary="follows",
        primaryjoin=id == Follow.from_user_id,
        secondaryjoin=id == Follow.to_user_id,
        backref="followers",
        init=False,
        info={"doc": "User가 팔로우하는 User 목록"},
    )

    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="user",
        cascade="all, delete-orphan",
        init=False,
        info={"doc": "User와 Post 간의 1:N 관계"},
    )

    likes: Mapped[list["Like"]] = relationship(
        "Like",
        back_populates="user",
        cascade="all, delete-orphan",
        init=False,
        info={"doc": "User가 좋아요를 누른 Post 목록"},
    )
