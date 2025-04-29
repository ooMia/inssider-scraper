import os
import sys

sys.path.append(os.path.dirname(__file__))

from dotenv import load_dotenv

load_dotenv()

SCRAPE_BASE_URL: str = os.getenv('SCRAPE_BASE_URL')
SCRAPE_INITIAL_URL: str = os.getenv('SCRAPE_INITIAL_URL')
SCRAPE_LOGIN_URL: str = os.getenv('SCRAPE_LOGIN_URL')
SCRAPE_LOGIN_USER_ID: str = os.getenv('SCRAPE_LOGIN_USER_ID')
SCRAPE_LOGIN_USER_PW: str = os.getenv('SCRAPE_LOGIN_USER_PW')

SCRAPE_DETAIL_SAMPLE_URL: str = os.getenv('SCRAPE_DETAIL_SAMPLE_URL')
SCRAPE_DETAIL_CORP_FIELD_XPATH: str = os.getenv('SCRAPE_DETAIL_CORP_INFO_XPATH')
SCRAPE_DETAIL_INVESTMENT_SELECTOR: str = os.getenv('SCRAPE_DETAIL_INVESTMENT_SELECTOR')
SCRAPE_DETAIL_HIRING_SELECTOR: str = os.getenv('SCRAPE_DETAIL_HIRING_SELECTOR')
SCRAPE_CUR_PAGE: int = int(os.getenv('SCRAPE_CUR_PAGE', 1))

GUI_BASE_X: int = int(os.getenv('GUI_BASE_X'))
GUI_BASE_Y: int = int(os.getenv('GUI_BASE_Y'))
GUI_BASE_WIDTH: int = int(os.getenv('GUI_BASE_WIDTH'))
GUI_BASE_HEIGHT: int = int(os.getenv('GUI_BASE_HEIGHT'))

from selenium.webdriver.chrome.options import Options

driver_options = Options()
driver_options.add_argument(f"--window-position={GUI_BASE_X},{GUI_BASE_Y}")
driver_options.add_argument(f"--window-size={GUI_BASE_WIDTH},{GUI_BASE_HEIGHT}")
