from model.controller import HashTagCrawlRequest


class HashTagService:
    def crawl_hashtag(self, req: HashTagCrawlRequest) -> dict:
        from urllib.parse import quote

        from service.youtube.crawler import YouTubeCrawler
        from service.youtube.strategy import HashTagStrategy

        with YouTubeCrawler() as crawler:
            url = f"https://www.youtube.com/hashtag/{quote(req.hashtag)}"
            data = crawler.scrape(url, HashTagStrategy(), req.limit)

            # [ ] TODO db 저장

            return data

    def crawl_namuwiki(self) -> dict:
        from service.youtube.crawler import NamuWikiCrawler
        from service.youtube.strategy import NamuWikiStrategy

        with NamuWikiCrawler() as crawler:
            url = "https://namu.wiki/w/%EB%B0%88(%EC%9D%B8%ED%84%B0%EB%84%B7%20%EC%9A%A9%EC%96%B4)#s-6.1"
            data = crawler.scrape(url, NamuWikiStrategy())

            # [ ] TODO db 저장

            return data

if __name__ == "__main__":
    res = HashTagService().crawl_namuwiki()
    print(res)
