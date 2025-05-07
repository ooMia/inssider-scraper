import abc
import os
from urllib.request import Request

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from seleniumwire import webdriver

from scrape.strategy import HashTagStrategy, ScrapeStrategy


class DefaultCrawler(abc.ABC):
    """기본 웹 크롤러 클래스입니다."""

    def __init__(self):
        super().__init__()

    def __enter__(self):
        """컨텍스트 매니저 진입 시 호출됩니다."""
        return self

    def __exit__(self, *args):
        """컨텍스트 매니저 종료 시 호출됩니다."""
        self.close()

    @abc.abstractmethod
    def close(self):
        """스크래퍼가 사용한 리소스를 정리합니다."""
        raise NotImplementedError()


class YouTube(DefaultCrawler):
    """YouTube 스크래퍼 클래스입니다."""

    def __init__(self):
        """드라이버를 초기화합니다."""
        super().__init__()
        self.host = "www.youtube.com"

        brave_path = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
        if not os.path.exists(brave_path):
            print("경고: Brave Browser를 찾을 수 없습니다. 기본 Chrome을 사용합니다.")
            self.driver = webdriver.Chrome()
        else:
            options = Options()
            options.binary_location = brave_path
            self.driver = webdriver.Chrome(options=options)

        self.driver.set_page_load_timeout(300)
        self.driver.set_script_timeout(300)

        self.driver.get("https://httpbin.io/headers")

        headers = self.driver.find_element(By.TAG_NAME, "body").text
        headers = eval(headers)  # convert str to dict
        headers["headers"]["Host"] = self.host
        headers["headers"]["Referer"] = f"https://{self.host}/"

        def request_interceptor(request: Request):
            request.headers = headers

        self.driver.request_interceptor = request_interceptor

    def close(self):
        """드라이버를 종료합니다."""
        self.driver.quit()

    def scrape(self, url: str, strategy: ScrapeStrategy) -> dict:
        """YouTube URL에서 데이터를 스크랩합니다."""
        self.driver.get(url)
        self.driver.implicitly_wait(10)

        self.driver.save_screenshot("screenshot.png")
        with open("target.html", "w+", encoding="utf-8") as f:
            f.write(self.driver.page_source)
        return strategy.run(self.driver)


if __name__ == "__main__":
    with YouTube() as youtube_scraper:
        url = "https://www.youtube.com/hashtag/%EB%B0%88"

        data = youtube_scraper.scrape(url, HashTagStrategy)
        # store as a JSON file
        with open("data.json", "w+", encoding="utf-8") as f:
            import json

            json.dump(data, f, ensure_ascii=False, indent=4)
