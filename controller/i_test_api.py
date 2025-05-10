import asyncio
import unittest
from typing import cast


class AsyncTestCase(unittest.TestCase):
    """비동기 테스트를 지원하는 TestCase 기본 클래스"""

    def __init__(self, method_name="runTest"):
        super().__init__(method_name)
        self._asyncio_loop = None

    def setUp(self):
        self._asyncio_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._asyncio_loop)

    def tearDown(self):
        if self._asyncio_loop:
            self._asyncio_loop.close()
        asyncio.set_event_loop(None)

    def run_async(self, coroutine):
        """비동기 코루틴을 실행하는 헬퍼 메서드"""
        if self._asyncio_loop:
            return self._asyncio_loop.run_until_complete(coroutine)


class IntegrationTestAPI(AsyncTestCase):
    """API에 대한 통합 테스트 (크롤링 포함)"""

    def test_create_video(self):
        from model.controller import VideoCreateRequest, VideoCreateResponse

        async def test_coro():
            from controller.main import create_video

            req = VideoCreateRequest(video_id="-vUUQ2ENjWs")
            res: VideoCreateResponse = await create_video(req)
            self.assertEqual(req.video_id, res.video_id)
            self.assertEqual(res.title, "치킨 원탑 소스")

            self.assertIn(
                f"https://i.ytimg.com/vi/{req.video_id}/",
                cast(str, res.thumbnail_url),
            )

            # Google YouTube API의 결과는 실제 웹 페이지에 출력되는 조회수 대비 -10%의 오차가 발생함
            self.assertGreaterEqual(cast(int, res.views), 5_030_000 * 0.9)

        try:
            self.run_async(test_coro())
        except KeyboardInterrupt:
            raise AssertionError("KeyboardInterrupt 발생")

    def test_crawl_hashtag(self):
        from model.controller import HashTagCrawlRequest, HashTagCrawlResponse

        async def test_coro():
            from controller.main import crawl_hashtag

            req = HashTagCrawlRequest(hashtag="밈", limit=10)
            res: HashTagCrawlResponse = await crawl_hashtag(req)
            self.assertGreaterEqual(res.length, 10)
            for content in res.contents:
                self.assertGreaterEqual(content.view_count, 1_000_000)

        try:
            self.run_async(test_coro())
        except KeyboardInterrupt:
            raise AssertionError("KeyboardInterrupt 발생")


if __name__ == "__main__":
    unittest.main()
