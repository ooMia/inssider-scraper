import abc
from typing import override

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class ScrapeStrategy(abc.ABC):
    """스크래핑 전략을 정의하는 추상 클래스입니다."""

    @classmethod
    def run(cls, driver: Chrome, len_items: int) -> dict:
        """스크래핑 전략을 실행합니다."""
        res, idx, limit = [], 0, 400  # YouTube provides max 450 contents
        try:
            while idx < limit and len(res) < len_items:
                found = cls._run(driver, idx)
                idx += len(found)
                filtered = list(filter(cls._filter, found))
                res.extend(filtered)
        except Exception:
            # return current result if error occurs
            pass
        return {"length": len(res), "contents": res}

    @classmethod
    @abc.abstractmethod
    def _run(cls, driver: Chrome, idx: int) -> list[dict]:
        """해시태그 검색 결과를 스크래핑합니다."""
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def _filter(cls, content: dict) -> bool:
        """스크래핑한 콘텐츠를 필터링합니다."""
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def _scrape_content(cls, content: WebElement) -> dict:
        """스크래핑한 콘텐츠를 파싱합니다."""
        raise NotImplementedError()


class HashTagStrategy(ScrapeStrategy):
    """해시태그 스크래핑 전략을 정의하는 클래스입니다."""

    @classmethod
    @override
    def _run(cls, driver: Chrome, idx: int) -> list[dict]:
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.webdriver.common.keys import Keys

        actions = ActionChains(driver)
        _from, _to = idx, idx + 36  # YouTube loads 36 contents at once
        parsed_contents = []
        html = driver.find_element(By.TAG_NAME, "html")

        while _from < _to:
            contents = driver.find_elements(By.CSS_SELECTOR, "#contents > ytd-rich-item-renderer")[
                _from:
            ]
            html.send_keys(Keys.PAGE_DOWN)

            for content in contents:
                actions.move_to_element(content).perform()
                parsed_contents.append(cls._scrape_content(content))
            _from += len(contents)

        return parsed_contents

    @classmethod
    @override
    def _scrape_content(cls, content: WebElement) -> dict:
        thumbnail = content.find_element(By.CSS_SELECTOR, "#thumbnail #thumbnail")

        video_url = thumbnail.get_attribute("href")
        video_id = video_url.split("/")[-1]
        thumbnail_url = thumbnail.find_element(By.CSS_SELECTOR, "yt-image > img").get_attribute(
            "src"
        )
        if not thumbnail_url:
            thumbnail_url = f"https://i.ytimg.com/vi/{video_id}/hq2.jpg"

        details = content.find_element(By.ID, "details")
        meta = details.find_element(By.ID, "meta")

        title = meta.find_element(By.ID, "video-title")
        channel = meta.find_element(By.CSS_SELECTOR, "#channel-name #text > a")
        view_count = meta.find_element(By.CSS_SELECTOR, "#metadata-line > span:nth-child(3)")
        date = meta.find_element(By.CSS_SELECTOR, "#metadata-line > span:nth-child(4)")

        return {
            "video_id": video_id,
            "thumbnail_url": thumbnail_url,
            "video_url": video_url,
            "title": title.text,
            "channel": channel.text,
            "view_count": cls._parse_view_count(view_count.text),
            "date": date.text,
        }

    @classmethod
    @override
    def _filter(cls, content: dict) -> bool:
        """콘텐츠를 필터링합니다."""
        return content["view_count"] >= 1_000_000

    @staticmethod
    def _parse_view_count(view_count_text: str) -> int:
        """한국어 형태의 조회수 텍스트를 정수로 변환합니다.

        예시:
        - "조회수 1.6억회" -> 160000000
        - "조회수 1282만회" -> 12820000
        - "조회수 1.8만회" -> 18000
        - "조회수 3.5천회" -> 3500
        - "조회수 329회" -> 329
        - "조회수 없음" -> 0
        """
        try:
            count_text = view_count_text.replace("조회수", "").replace("회", "").strip()
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
                return int(float(count_text))
        except ValueError:
            # 변환할 수 없는 경우에는 0을 반환합니다.
            return 0


class NamuWikiStrategy(ScrapeStrategy):
    """나무위키 스크래핑 전략을 정의하는 클래스입니다."""

    @classmethod
    @override
    def _run(cls, driver: Chrome, idx: int) -> list[dict]:

        # [ ] TODO  나무위키 스크래핑 구현
        _from, _to = idx, idx + 36  # YouTube loads 36 contents at once
        parsed_contents = []

        while _from < _to:
            contents = driver.find_elements(By.PARTIAL_LINK_TEXT, "namu.wiki")[_from:]

            for content in contents:
                parsed_contents.append(cls._scrape_content(content))
            _from += len(contents)

        return parsed_contents

    @classmethod
    @override
    def _scrape_content(cls, content: WebElement) -> dict:
        # [ ] TODO  나무위키 스크래핑 구현
        link = content.find_element(By.CSS_SELECTOR, "a")
        return {"link": link}

    @classmethod
    @override
    def _filter(cls, content: dict) -> bool:
        """콘텐츠를 필터링합니다."""
        return True
