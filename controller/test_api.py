from typing import cast

import pytest


@pytest.mark.asyncio
@pytest.mark.slow
async def test_create_video():
    """비디오 생성 API 테스트"""
    from controller.main import create_video
    from model.controller import VideoCreateRequest, VideoCreateResponse

    req = VideoCreateRequest(video_id="-vUUQ2ENjWs")
    res: VideoCreateResponse = await create_video(req)
    assert req.video_id == res.video_id
    assert res.title == "치킨 원탑 소스"

    assert f"https://i.ytimg.com/vi/{req.video_id}/" in cast(str, res.thumbnail_url)

    # Google YouTube API의 결과는 실제 웹 페이지에 출력되는 조회수 대비 -10%의 오차가 발생함
    assert cast(int, res.views) >= 5_030_000 * 0.9


@pytest.mark.asyncio
@pytest.mark.slow
async def test_crawl_hashtag():
    """해시태그 크롤링 API 테스트"""
    from controller.main import crawl_hashtag
    from model.controller import HashTagCrawlRequest, HashTagCrawlResponse

    req = HashTagCrawlRequest(hashtag="밈", limit=10)
    res: HashTagCrawlResponse = await crawl_hashtag(req)
    assert res.length >= 10
    for content in res.contents:
        assert content.view_count >= 1_000_000
