from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from model.repository import TimestampMixin

Str = Mapped[str]
StrOpt = Mapped[Optional[str]]
IntOpt = Mapped[Optional[int]]
FloatOpt = Mapped[Optional[float]]
Datetime = Mapped[datetime]
DatetimeOpt = Mapped[Optional[datetime]]


class Base(DeclarativeBase):
    pass


class Video(Base, TimestampMixin):
    """유튜브 영상 기본 정보"""

    __tablename__ = "videos"

    video_id: Str = mapped_column(String(20), primary_key=True)  # 유튜브 영상 ID
    title: Str = mapped_column(String(255))  # 영상 제목 (nullable=False 자동 설정)
    description: StrOpt = mapped_column(Text)  # 영상 설명 (nullable=True 자동 설정)
    length: IntOpt = mapped_column(Integer)  # 영상 길이 (nullable=True 자동 설정)
    # 조회수 (nullable=True 자동 설정)
    views: IntOpt = mapped_column(Integer, default=0)
    rating: FloatOpt = mapped_column(Float)  # 평균 평점 (nullable=True 자동 설정)
    publish_date: DatetimeOpt = mapped_column(
        DateTime
    )  # 영상 게시 날짜 (nullable=True 자동 설정)
    thumbnail_url: StrOpt = mapped_column(
        String(255)
    )  # 썸네일 URL (nullable=True 자동 설정)

    created_at: Datetime = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )  # 데이터 생성 시간
    updated_at: Datetime = mapped_column(
        DateTime,
        default=lambda: datetime.now(
            # 데이터 업데이트 시간
            timezone.utc
        ),
        onupdate=lambda: datetime.now(timezone.utc),
    )
