import uuid
from datetime import datetime, timedelta

from sqlalchemy import DateTime, Float, Integer, String, Text, func
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column

from model.repository._base import Base, ExpirationTimestampMixin, SoftDeleteTimestampMixin


class Video(MappedAsDataclass, Base, SoftDeleteTimestampMixin):
    __tablename__ = "videos"

    id: Mapped[str] = mapped_column(String(20), primary_key=True, doc="유튜브 영상 ID")
    title: Mapped[str] = mapped_column(String(255), doc="영상 제목")
    description: Mapped[str | None] = mapped_column(Text, doc="영상 설명")
    length: Mapped[int | None] = mapped_column(Integer, doc="영상 길이")
    rating: Mapped[float | None] = mapped_column(Float, doc="평균 평점")
    publish_date: Mapped[datetime | None] = mapped_column(DateTime, doc="영상 게시 날짜")
    thumbnail_url: Mapped[str | None] = mapped_column(String(255), doc="썸네일 URL")
    views: Mapped[int | None] = mapped_column(Integer, default=0, doc="조회수")


class EmailVerificationCode(MappedAsDataclass, Base, ExpirationTimestampMixin):
    __tablename__ = "email_verification_codes"

    email: Mapped[str] = mapped_column(String(255), primary_key=True, doc="이메일")
    code: Mapped[str] = mapped_column(String(6), primary_key=True, doc="인증 코드")


class AuthorizationCode(MappedAsDataclass, Base, ExpirationTimestampMixin):
    __tablename__ = "authorization_codes"

    code: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        insert_default=lambda: str(uuid.uuid4()),
        doc="인가 코드 (UUID v4)",
    )
