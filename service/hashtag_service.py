from model.controller import HashTagCrawlRequest, HashTagCrawlResponse


class HashTagService:
    def crawl_hashtag(self, req: HashTagCrawlRequest) -> HashTagCrawlResponse:
        from urllib.parse import quote

        from service.youtube.strategy import HashTagStrategy
        from service.youtube.crawler import YouTubeCrawler

        with YouTubeCrawler() as crawler:
            url = f"https://www.youtube.com/hashtag/{quote(req.hashtag)}"
            data = crawler.scrape(url, HashTagStrategy, req.limit)

            # TODO db 저장

            return data
