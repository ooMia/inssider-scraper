from fastapi import FastAPI

from model.controller import (
    HashTagCrawlRequest,
    HashTagCrawlResponse,
    VideoCreateRequest,
    VideoCreateResponse,
)


def _project_version() -> str:
    import tomllib
    from pathlib import Path

    try:
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        with open(pyproject_path, "rb") as f:
            pyproject_data = tomllib.load(f)
            return pyproject_data["project"]["version"]
    except (FileNotFoundError, KeyError):
        return "0.0.1"


app = FastAPI(
    title="Inssider Crawler",
    description="인사이더 데이터 크롤링 및 조회 API",
    version=_project_version(),
    contact={
        "name": "ooMia",
        "url": "http://github.com/ooMia",
        "email": "hyeonhak.kim.dev@gmail.com",
    },
)


@app.post("/api/v1/videos")
async def create_video(req: VideoCreateRequest) -> VideoCreateResponse:
    from service.video_service import VideoService

    service = VideoService(req.video_id)
    data = service.create_video()

    return VideoCreateResponse.from_dict(data)


@app.post("/api/v1/crawl/hashtag")
async def crawl_hashtag(req: HashTagCrawlRequest) -> HashTagCrawlResponse:
    from service.hashtag_service import HashTagService

    service = HashTagService()
    data = service.crawl_hashtag(req)

    return HashTagCrawlResponse.from_dict(data)
