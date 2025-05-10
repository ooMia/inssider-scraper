from model.controller import HashTagCrawlRequest


class HashTagService:
    def crawl_hashtag(self, req: HashTagCrawlRequest) -> dict:
        from urllib.parse import quote

        from service.youtube.crawler import YouTubeCrawler
        from service.youtube.strategy import HashTagStrategy

        with YouTubeCrawler() as crawler:
            url = f"https://www.youtube.com/hashtag/{quote(req.hashtag)}"
            data = crawler.scrape(url, HashTagStrategy(), req.limit)

            # TODO db 저장

            return data
