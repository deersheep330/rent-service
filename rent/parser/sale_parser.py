import time
import traceback
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from sqlalchemy import exists
from webdriver_manager.chrome import ChromeDriverManager

from rent.db import create_engine_from_url, start_session, insert, delete_older_than
from rent.models import House
from rent.parser.virtual_parser import VirtualParser
from rent.utilities import get_db_connection_url


class SaleParser(VirtualParser):

    def __init__(self, price_min='200', price_max='555'):

        super().__init__()

        self.url = 'https://sale.591.com.tw/'
        self.item_url_template_prefix = 'https://sale.591.com.tw/home/house/detail/2/'
        self.item_url_template_suffix = '.html'

        self.elements = {

            'credit_close': "//*[contains(@class, 'accreditPop') and not(contains(@style, 'none'))]//*[contains(@class, 'close')]",
            'close_popup': "//*[contains(@class, 'tips-popbox-img')]",

            'unfocus': "//*[contains(@class, 'houseList-head-title')]",

            'area': "(//*[contains(@class, 'filter-location-btn')])[1]",
            'keelung': "//*[contains(@class, 'region-list-item')]//a[contains(text(), '基隆市')]",
            'keelung_checked': "//*[contains(@class, 'region-list-item') and contains(@class, 'select')]//a[contains(text(), '基隆市')]",

            'section': "//*[contains(@class, 'filter-location-btn') and contains(text(), '選擇鄉鎮')]",
            'xinyi': "//*[contains(@class, 'section-list-item-link') and contains(text(), '信義區')]",
            'xinyi_checked': "//*[contains(@class, 'section-list-item-link') and contains(@class, 'select') and contains(text(), '信義區')]",
            'renai': "//*[contains(@class, 'section-list-item-link') and contains(text(), '仁愛區')]",
            'renai_checked': "//*[contains(@class, 'section-list-item-link') and contains(@class, 'select') and contains(text(), '仁愛區')]",
            'zhongzheng': "//*[contains(@class, 'section-list-item-link') and contains(text(), '中正區')]",
            'zhongzheng_checked': "//*[contains(@class, 'section-list-item-link') and contains(@class, 'select') and contains(text(), '中正區')]",

            'flat': "//*[contains(@data-gtm-stat, '住宅')]",
            'flat_checked': "//*[contains(@data-gtm-stat, '住宅') and contains(@class, 'select')]",

            #'price_show_more': "//*[contains(@class, 'saleprice')]//*[contains(@class, 'small-toggle')]",
            #'price_show_more_opened': "//*[contains(@class, 'saleprice')]//*[contains(@class, 'small-toggle') and contains(@class, 'open')]",
            'price_min': "//*[contains(@class, 'saleprice')]//input[contains(@class, 'min')]",
            'price_max': "//*[contains(@class, 'saleprice')]//input[contains(@class, 'max')]",
            'price_submit': "//*[contains(@class, 'saleprice')]//*[contains(@class, 'submit')]",

            'rooms': "//*[contains(@class, 'pattern')]//*[contains(@data-gtm-stat, '3房')]",
            'rooms_checked': "//*[contains(@class, 'pattern')]//*[contains(@data-gtm-stat, '3房') and contains(@class, 'select')]",

            'items': "//*[@data-bind and contains(@class, 'houseList-item')]",
            'next_page': "//*[contains(@class, 'pageNext') and not(contains(@class, 'last'))]",

            'loading_now': "//*[@rel='loading' and not(contains(@style, 'none'))]",
            'loading_completed': "//*[@rel='loading' and contains(@style, 'none')]"
        }

        # price should be type of string
        self.price_min = price_min
        self.price_max = price_max

    def parse(self):

        super().parse()

        try:

            self.driver.get(self.url)
            self._wait_for('loading_completed')

            # close gdpr
            #if self._is_exist('credit_close'):
            #    self._click('credit_close')

            # close popup
            self._wait_for('close_popup')
            if self._is_exist('close_popup'):
                self._click('close_popup')

            # select area
            self._click_and_wait('area', 'keelung')
            self._click_and_wait('keelung', 'keelung_checked')
            #self._wait_for('loading_completed')

            #time.sleep(10)

            # select section
            #self._click_and_wait('section', 'xinyi')
            self._click_and_wait('xinyi', 'xinyi_checked')
            self._click_and_wait('renai', 'renai_checked')
            self._click_and_wait('zhongzheng', 'zhongzheng_checked')
            self._click('unfocus')
            self._wait_for('loading_completed')

            # select type
            self._click_and_wait('flat', 'flat_checked')
            self._wait_for('loading_completed')

            # input price
            #self._click_and_wait('price_show_more', 'price_min')
            self._send_keys('price_min', self.price_min)
            self._send_keys('price_max', self.price_max)
            self._wait_for('price_submit')
            self._click_and_wait('price_submit', 'loading_now')
            self._wait_for('loading_completed')

            # select rooms
            self._click_and_wait('rooms', 'rooms_checked')
            self._wait_for('loading_completed')

            self._get_items()
            while self._is_exist('next_page'):
                self._click_and_wait('next_page', 'loading_now')
                self._wait_for('loading_completed')
                self._get_items()

            self.driver.quit()

        except Exception as e:
            print(e)
            traceback.print_exception(type(e), e, e.__traceback__)
            self.driver.save_screenshot('screenshot.png')
