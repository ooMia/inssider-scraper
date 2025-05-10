from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from model.repository._base import Base, TimestampMixin


class Video(Base, TimestampMixin):
    __tablename__ = "videos"

    id: Mapped[str] = mapped_column(String(20), primary_key=True, doc="유튜브 영상 ID")
    title: Mapped[str] = mapped_column(String(255), doc="영상 제목")
    description: Mapped[str | None] = mapped_column(Text, doc="영상 설명")
    length: Mapped[int | None] = mapped_column(Integer, doc="영상 길이")
    views: Mapped[int | None] = mapped_column(Integer, default=0, doc="조회수")
    rating: Mapped[float | None] = mapped_column(Float, doc="평균 평점")
    publish_date: Mapped[datetime | None] = mapped_column(DateTime, doc="영상 게시 날짜")
    thumbnail_url: Mapped[str | None] = mapped_column(String(255), doc="썸네일 URL")
