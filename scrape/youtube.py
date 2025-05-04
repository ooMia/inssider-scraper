import abc
import os
from urllib.request import Request

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from seleniumwire import webdriver


class Scraper(abc.ABC):
    """웹 스크래퍼의 추상 클래스입니다."""


class DefaultScraper(Scraper):
    """기본 웹 스크래퍼 클래스입니다."""

    def __init__(self):
        """드라이버를 초기화합니다."""
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


class YouTube(DefaultScraper):
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

    def __find_text(self, value, by: By = By.CSS_SELECTOR):
        return self.driver.find_element(by, value).text

    def scrape(self, url: str) -> dict:
        """YouTube URL에서 데이터를 스크랩합니다."""
        self.driver.get(url)
        self.driver.implicitly_wait(10)

        title = self.__find_text("#title > h1 > yt-formatted-string")
        channel = self.__find_text("#text > a")
        views = self.__find_text("#info > span:nth-child(1)")
        likes = self.__find_text(
            "#top-level-buttons-computed > segmented-like-dislike-button-view-model > yt-smartimation > div > div > like-button-view-model > toggle-button-view-model > button-view-model > button > div.yt-spec-button-shape-next__button-text-content"
        )
        self.driver.save_screenshot("screenshot.png")

        return {"title": title, "channel": channel, "views": views, "likes": likes}


if __name__ == "__main__":
    with YouTube() as youtube_scraper:
        url = "https://www.youtube.com/watch?v=6rMtd9jSPD8"
        url = "https://www.youtube.com/watch?v=LAQZfeETFbg&t=27561s"
        data = youtube_scraper.scrape(url)
        for key, value in data.items():
            print(f"{key}: {value}")
