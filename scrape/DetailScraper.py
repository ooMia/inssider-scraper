class DetailScraper:
    from selenium.webdriver.remote.webelement import WebElement
    from scrape import SCRAPE_DETAIL_SAMPLE_URL

    def __init__(self, url: str = SCRAPE_DETAIL_SAMPLE_URL, driver=None):
        from selenium import webdriver
        from selenium.webdriver.support.wait import WebDriverWait
        from scrape import driver_options

        self.__driver = driver if driver is not None else webdriver.Chrome(options=driver_options)
        self.__wait = WebDriverWait(self.__driver, 3)

        # TODO: disable login -> use tor browser
        if not self.__is_login():
            self.__login()
        self.__driver.get(url)
        self.__scrap_corp_keywords()
        self.__scrap_corp_investment()
        self.__scrap_corp_recruit()

    def __find_element_by(self, method: str, at: str) -> WebElement:
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions
        from selenium.common import StaleElementReferenceException
        try:
            by = getattr(By, method)
            return self.__wait.until(expected_conditions.presence_of_element_located((by, at)))
        except StaleElementReferenceException:
            from time import sleep
            sleep(1)
            return self.__wait.until(expected_conditions.presence_of_element_located((by, at)))

    def __find_element_by_selector(self, selector: str) -> WebElement or None:
        from selenium.common import TimeoutException
        try:
            element = self.__find_element_by('CSS_SELECTOR', selector)
            self.__driver.execute_script(f"document.querySelector('{selector}').scrollIntoView();")
            return element
        except TimeoutException:
            return None

    def __is_login(self):
        from selenium.common import JavascriptException
        try:
            return self.__driver.execute_script("return window.localStorage.getItem('accessToken')") is not None
        except JavascriptException:
            return False

    def __login(self):
        from scrape import SCRAPE_LOGIN_URL, SCRAPE_LOGIN_USER_ID, SCRAPE_LOGIN_USER_PW
        from selenium.common import TimeoutException

        self.__driver.get(SCRAPE_LOGIN_URL)
        self.__find_element_by('NAME', 'email').send_keys(SCRAPE_LOGIN_USER_ID)
        self.__find_element_by('NAME', 'password').send_keys(SCRAPE_LOGIN_USER_PW)

        try:
            self.__find_element_by('CSS_SELECTOR', 'main form').submit()
        except TimeoutException:
            import pyautogui
            pyautogui.moveTo(600, 797)  # print(pyautogui.position())
            pyautogui.click()

        self.__wait.until(lambda check: self.__is_login())

    def __scrap_corp_keywords(self):
        from scrape import SCRAPE_DETAIL_CORP_FIELD_XPATH
        element = self.__find_element_by('XPATH', SCRAPE_DETAIL_CORP_FIELD_XPATH)
        self.keywords = element.text.split('\n')[::2]

    def __scrap_corp_investment(self):
        from scrape import SCRAPE_DETAIL_INVESTMENT_SELECTOR
        raw_text = self.__find_element_by_selector(SCRAPE_DETAIL_INVESTMENT_SELECTOR).text

        import re
        search_update = re.search(r"업데이트 : (.+)", raw_text)
        search_stage = re.search(r"최종투자단계\n(.+)", raw_text)
        search_amount = re.search(r"누적투자유치금액\n(.+)", raw_text)
        search_count = re.search(r"투자유치건수\n(.+)", raw_text)

        self.investment = {
            "update": search_update.group(1) if search_update else None,
            "stage": search_stage.group(1) if search_stage else None,
            "amount": search_amount.group(1) if search_amount else None,
            "count": search_count.group(1) if search_count else None,
        }

    def __scrap_corp_recruit(self):
        self.__click_load_button()
        e = self.__find_element_by_selector("#section-recruit")
        self.recruit = self.__parse_html(e.get_attribute('outerHTML')) if e is not None else None

    def __click_load_button(self):
        while True:
            button = self.__find_element_by_selector("#section-recruit > div > div > div > div > div > button")
            if button is None:
                break
            self.__driver.execute_script("arguments[0].click();", button)

    @staticmethod
    def __parse_html(raw_html):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(raw_html, 'html.parser')
        li_tags = soup.find_all('li')

        result = []
        for li in li_tags:
            li_dict = {
                "href": "" if li.find('a') is None else li.find('a')['href'],
                "name": "" if li.find('h1') is None else li.find('h1').text,
                "incentive": "" if li.find('p') is None else li.find('p').text,
                "type": "" if li.find('span') is None else li.find('span').text,
            }
            result.append(li_dict)
        return result


if __name__ == '__main__':
    detail_scraper = DetailScraper()
    print(detail_scraper.keywords)
    print(detail_scraper.investment)
    print(detail_scraper.recruit)
    print(len(detail_scraper.recruit))
