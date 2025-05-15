import abc
import os
from urllib.request import Request
from warnings import filterwarnings

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from service.youtube.strategy import ScrapeStrategy

filterwarnings("ignore", "", DeprecationWarning, "seleniumwire")
filterwarnings("ignore", "", DeprecationWarning, "OpenSSL.crypto", 1679)

from seleniumwire import webdriver  # noqa: E402


class DefaultCrawler(abc.ABC):

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        original_init = cls.__init__

        def new_init(self, *args, **kwargs):
            DefaultCrawler.__init__(self)
            return original_init(self, *args, **kwargs)

        cls.__init__ = new_init

    def __init__(self):
        brave_path = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
        if not os.path.exists(brave_path):
            print("경고: Brave Browser를 찾을 수 없습니다. 기본 Chrome을 사용합니다.")
            self.driver = webdriver.Chrome()
        else:
            options = Options()
            options.binary_location = brave_path
            self.driver = webdriver.Chrome(options=options)

        self.driver.get("https://httpbin.io/headers")
        self.headers = eval(self.driver.find_element(By.TAG_NAME, "body").text)
        self.driver.request_interceptor = self.request_interceptor

    def __enter__(self):
        """컨텍스트 매니저 진입 시 호출됩니다."""
        return self

    def __exit__(self, *args):
        """컨텍스트 매니저 종료 시 호출됩니다."""
        self.driver.quit()

    def request_interceptor(self, request: Request):
        """요청 인터셉터를 설정합니다."""
        request.headers = self.headers

    @abc.abstractmethod
    def scrape(self, url: str, strategy: ScrapeStrategy) -> dict:
        """전달받은 strategy에 따라 해당 URL에서 데이터를 스크랩합니다."""
        raise NotImplementedError()


class YouTubeCrawler(DefaultCrawler):
    """영상 세부 정보 탐색 이외의 용도로 활용 가능한 YouTube 크롤러입니다."""

    def __init__(self):
        """요청 헤더를 초기화합니다."""
        self.host = "www.youtube.com"
        self.headers["headers"]["Host"] = self.host
        self.headers["headers"]["Referer"] = f"https://{self.host}/"

    def scrape(self, url: str, strategy: ScrapeStrategy, limit: int = 10) -> dict:
        self.driver.get(url)
        # self.driver.implicitly_wait(10)
        return strategy.run(self.driver, limit)


class NamuWikiCrawler(DefaultCrawler):
    """NamuWiki 크롤러입니다."""

    def __init__(self):
        """요청 헤더를 초기화합니다."""
        self.host = "namu.wiki"
        self.headers["headers"]["Host"] = self.host
        self.headers["headers"]["Referer"] = f"https://{self.host}/"
        # TODO invalid browser 문제 해결

    def scrape(self, url: str, strategy: ScrapeStrategy, limit: int = 10) -> dict:
        self.driver.get(url)
        # self.driver.implicitly_wait(10)
        return strategy.run(self.driver, limit)
