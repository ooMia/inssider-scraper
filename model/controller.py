from datetime import datetime

from pydantic import BaseModel, Field


class VideoCreateRequest(BaseModel):
    video_id: str = Field(
        description="유튜브 비디오 ID",
        json_schema_extra={"example": "MLpmiywRNzY"},
    )


class VideoCreateResponse(BaseModel):
    video_id: str
    title: str | None = None
    description: str | None = None
    length: int | None = None
    views: int | None = None
    rating: float | None = None
    publish_date: datetime | None = None
    thumbnail_url: str | None = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


class HashTagCrawlRequest(BaseModel):
    hashtag: str = Field(
        description="검색 해시태그",
        json_schema_extra={"example": "밈"},
    )
    limit: int = Field(
        description="검색 결과 개수",
        default=10,
    )


class HashTagCrawlResponse(BaseModel):
    class SearchResult(BaseModel):
        video_id: str
        thumbnail_url: str
        video_url: str
        title: str
        channel: str
        view_count: int
        date: str

    length: int
    contents: list[SearchResult]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            contents=[cls.SearchResult(**item) for item in data.get("contents", [])],
            length=data.get("length", len(data.get("contents", []))),
        )
