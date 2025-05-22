from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model.repository import Post

from sqlalchemy import BigInteger, Boolean, String, Text
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from model.repository._base import Base, SoftDeleteTimestampMixin, accounts_id_fk


class Like(MappedAsDataclass, Base, SoftDeleteTimestampMixin):
    __tablename__ = "likes"
    from enum import Enum

    class LikeTargetType(str, Enum):
        POST = "post"
        COMMENT = "comment"

    # 1. PK (init=False)
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, init=False)
    account_id: Mapped[int] = mapped_column(
        BigInteger, accounts_id_fk(), nullable=False, init=False
    )

    # 2. 필수값 (init=True, 디폴트 없음)
    target_type: Mapped[LikeTargetType] = mapped_column(String(50), nullable=False, init=True)
    target_id: Mapped[int] = mapped_column(BigInteger, nullable=False, init=True)

    # 3. 관계 (init=True, default=None)
    account: Mapped["Account"] = relationship(
        "Account",
        back_populates="likes",
        init=True,
        default=None,
        uselist=False,
        info={"doc": "Like를 누른 사용자"},
    )

    # 4. 제약조건
    from sqlalchemy import UniqueConstraint

    __table_args__ = (
        UniqueConstraint("account_id", "target_type", "target_id", name="uq_like_account_target"),
    )


class Follow(MappedAsDataclass, Base, SoftDeleteTimestampMixin):
    __tablename__ = "follows"

    from_account_id: Mapped[int] = mapped_column(
        BigInteger, accounts_id_fk(), primary_key=True, doc="팔로우를 요청한 사용자 ID"
    )
    to_account_id: Mapped[int] = mapped_column(
        BigInteger, accounts_id_fk(), primary_key=True, doc="팔로우 요청 대상의 사용자 ID"
    )


class Profile(MappedAsDataclass, Base, SoftDeleteTimestampMixin):
    __tablename__ = "profiles"

    # 1. PK (account_id, init=False)
    account_id: Mapped[int] = mapped_column(
        BigInteger, accounts_id_fk(), primary_key=True, doc="accounts 테이블 PK", init=False
    )

    # 2. 선택값 (default=None)
    introduction: Mapped[str | None] = mapped_column(
        Text, nullable=True, doc="자기소개", default=None
    )
    profile_url: Mapped[str | None] = mapped_column(
        String(255), nullable=True, doc="프로필 URL", default=None
    )
    nickname: Mapped[str | None] = mapped_column(
        String(255), nullable=True, doc="사용자 이름", default=None
    )

    # 3. 관계 (init=True, default=None)
    account: Mapped["Account"] = relationship(
        "Account",
        back_populates="details",
        init=True,
        default=None,
        uselist=False,
    )

    # 4. 옵션 (default=True)
    account_visibility: Mapped[bool] = mapped_column(Boolean, default=True, doc="프로필 공개 여부")
    follower_visibility: Mapped[bool] = mapped_column(Boolean, default=True, doc="팔로워 공개 여부")


class Account(MappedAsDataclass, Base, SoftDeleteTimestampMixin):
    __tablename__ = "accounts"

    # 1. PK (init=False)
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        init=False,
    )

    # 2. 필수값 (init=True, 디폴트 없음)
    email: Mapped[str] = mapped_column(String(255), unique=True, doc="이메일 주소")

    password: Mapped[str | None] = mapped_column(
        String(255), nullable=True, doc="비밀번호 해싱값 (이메일 인증 시)"
    )
    password_salt: Mapped[str | None] = mapped_column(
        String(255), nullable=True, doc="비밀번호 해싱용 salt (이메일 인증 시)"
    )

    # 3. 필수 값 (init=False, 디폴트 있음)
    account_type: Mapped[str] = mapped_column(
        String(50), default="email", doc="계정 유형 (email, google, facebook 등)"
    )
    role: Mapped[str] = mapped_column(String(50), default="user", doc="사용자 권한")

    # 소셜 로그인 사용자의 경우, 해당 프로바이더에서 제공하는 고유 ID
    provider_user_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        default=None,
        doc="OAuth 공급자의 사용자 고유 ID (소셜 로그인 시)",
    )

    # 4. 관계 필드 (init=False, 객체지향적 사용)
    details: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="account",
        cascade="all, delete-orphan",
        uselist=False,
        init=False,
        info={"doc": "Account와 Profile의 1:1 관계"},
    )

    following: Mapped[list["Follow"]] = relationship(
        "Account",
        secondary="follows",
        primaryjoin=id == Follow.from_account_id,
        secondaryjoin=id == Follow.to_account_id,
        backref="followers",
        init=False,
        info={"doc": "Account가 팔로우하는 Account 목록"},
    )

    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="account",
        cascade="all, delete-orphan",
        init=False,
        info={"doc": "Account와 Post 간의 1:N 관계"},
    )

    likes: Mapped[list["Like"]] = relationship(
        "Like",
        back_populates="account",
        cascade="all, delete-orphan",
        init=False,
        info={"doc": "Account가 좋아요를 누른 Post 목록"},
    )
