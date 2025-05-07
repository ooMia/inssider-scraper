import abc

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from seleniumwire import webdriver


class ScrapeStrategy(abc.ABC):
    """스크래핑 전략을 정의하는 추상 클래스입니다."""

    @staticmethod
    def run(driver: webdriver.Chrome) -> dict:
        """스크래핑 전략을 실행합니다."""
        result = ScrapeStrategy._run(driver)
        return {
            "length": len(result),
            "contents": list(filter(HashTagStrategy._filter, result)),
        }

    @staticmethod
    @abc.abstractmethod
    def _run(driver: webdriver.Chrome) -> list[dict]:
        """스크래핑한 콘텐츠를 필터링합니다."""
        raise NotImplementedError("_filter 메서드는 서브클래스에서 구현해야 합니다.")

    @staticmethod
    @abc.abstractmethod
    def _filter(content: dict) -> bool:
        """스크래핑한 콘텐츠를 필터링합니다."""
        raise NotImplementedError("_filter 메서드는 서브클래스에서 구현해야 합니다.")


class HashTagStrategy(ScrapeStrategy):
    """해시태그 스크래핑 전략을 정의하는 클래스입니다."""

    @staticmethod
    def _run(driver: webdriver.Chrome) -> list[dict]:
        """해시태그 검색 결과를 스크래핑합니다."""
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.webdriver.common.keys import Keys

        actions = ActionChains(driver)
        _from, _to = 0, 100
        parsed_contents = []
        html = driver.find_element(By.TAG_NAME, "html")

        while _from < _to:
            contents = driver.find_elements(
                By.CSS_SELECTOR, "#contents > ytd-rich-item-renderer"
            )[_from:]
            html.send_keys(Keys.PAGE_DOWN)

            for content in contents:
                actions.move_to_element(content).perform()
                parsed_contents.append(HashTagStrategy._get_video_details(content))
            _from += len(contents)

        return parsed_contents

    @staticmethod
    def _get_video_details(content: WebElement) -> dict:

        thumbnail = content.find_element(By.CSS_SELECTOR, "#thumbnail #thumbnail")

        video_url = thumbnail.get_attribute("href")
        thumbnail_url = thumbnail.find_element(
            By.CSS_SELECTOR, "yt-image > img"
        ).get_attribute("src")

        details = content.find_element(By.ID, "details")
        meta = details.find_element(By.ID, "meta")

        title = meta.find_element(By.ID, "video-title")
        channel = meta.find_element(By.CSS_SELECTOR, "#channel-name #text > a")
        view_count = meta.find_element(
            By.CSS_SELECTOR, "#metadata-line > span:nth-child(3)"
        )
        date = meta.find_element(By.CSS_SELECTOR, "#metadata-line > span:nth-child(4)")

        return {
            "thumbnail_url": thumbnail_url,
            "video_url": video_url,
            "title": title.text,
            "channel": channel.text,
            "view_count": HashTagStrategy._parse_view_count(view_count.text),
            "date": date.text,
        }

    @staticmethod
    def _parse_view_count(view_count_text: str) -> int:
        """한국어 형태의 조회수 텍스트를 정수로 변환합니다.

        예시:
        - "조회수 1.6억회" -> 160000000
        - "조회수 1282만회" -> 12820000
        - "조회수 1.8만회" -> 18000
        - "조회수 3.5천회" -> 3500
        - "조회수 329회" -> 329
        """
        count_text = view_count_text.split()[1][:-2]
        if "억" in count_text:
            number = float(count_text.replace("억", ""))
            return int(number * 100_000_000)
        elif "만" in count_text:
            number = float(count_text.replace("만", ""))
            return int(number * 10_000)
        elif "천" in count_text:
            number = float(count_text.replace("천", ""))
            return int(number * 1_000)
        else:
            return int(count_text)

    @staticmethod
    def _filter(content: dict) -> bool:
        """콘텐츠를 필터링합니다."""
        return content["view_count"] >= 1000000
