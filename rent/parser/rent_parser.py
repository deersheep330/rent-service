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


class RentParser(VirtualParser):

    def __init__(self, rent_type='flat', price_min='10000', price_max='20000', plain_min='10', plain_max='35'):

        super().__init__()

        # region = 1 : taipei city
        # region = 3 : new taipei city
        # self.url = 'https://rent.591.com.tw/?kind=0&region=1'
        self.url = 'https://rent.591.com.tw/?kind=0&region=3'
        self.item_url_template_prefix = 'https://rent.591.com.tw/rent-detail-'
        self.item_url_template_suffix = '.html'

        self.elements = {
            'area_close': "//*[contains(@class, 'area-box-close')]",
            'credit_close': "//*[contains(@class, 'accreditPop') and not(contains(@style, 'none'))]//*[contains(@class, 'close')]",

            'section': "//*[contains(@google-data-stat, '按鄉鎮選擇')]",
            'shilin': "//label//span[contains(text(), '士林區')]",
            'shilin_checked': "//*[contains(@class, 'checkTips')]//span[contains(text(), '士林區')]",
            'beitou': "//label//span[contains(text(), '北投區')]",
            'beitou_checked': "//*[contains(@class, 'checkTips')]//span[contains(text(), '北投區')]",
            'zhongshan': "//label//span[contains(text(), '中山區')]",
            'zhongshan_checked': "//*[contains(@class, 'checkTips')]//span[contains(text(), '中山區')]",

            'zhonghe': "//label//span[contains(text(), '中和區')]",
            'zhonghe_checked': "//*[contains(@class, 'checkTips')]//span[contains(text(), '中和區')]",
            'yonghe': "//label//span[contains(text(), '永和區')]",
            'yonghe_checked': "//*[contains(@class, 'checkTips')]//span[contains(text(), '永和區')]",

            'suite': "//*[contains(@class, 'search-rentType-span') and contains(@google-data-stat, '獨立套房')]",
            'suite_checked': "//*[contains(@class, 'search-rentType-span') and contains(@class, 'select') and contains(@google-data-stat, '獨立套房')]",
            'flat': "//*[contains(@class, 'search-rentType-span') and contains(@google-data-stat, '整層住家')]",
            'flat_checked': "//*[contains(@class, 'search-rentType-span') and contains(@class, 'select') and contains(@google-data-stat, '整層住家')]",

            'price_min': "//input[@id='rentPrice-min']",
            'price_max': "//input[@id='rentPrice-max']",
            'price_submit': "//*[contains(@class, 'rentPrice-btn') and not(contains(@style, 'none'))]",

            'plain_min': "//input[@id='plain-min']",
            'plain_max': "//input[@id='plain-max']",
            'plain_submit': "//*[contains(@class, 'plain-btn') and not(contains(@style, 'none'))]",

            'items': "//ul[@data-bind]",
            'next_page': "//*[contains(@class, 'pageNext') and not(contains(@class, 'last'))]",

            'loading_now': "//*[@rel='loading' and not(contains(@style, 'none'))]",
            'loading_completed': "//*[@rel='loading' and contains(@style, 'none')]"
        }

        self.rent_type = rent_type  # could be suite or flat

        # price and plain should be type of string
        self.price_min = price_min
        self.price_max = price_max
        self.plain_min = plain_min
        self.plain_max = plain_max

    def parse(self):

        super().parse()

        self.driver.get(self.url)

        # close modal
        self._wait_for('area_close')
        self._click('area_close')
        #self._wait_for('credit_close')
        #self._click('credit_close')

        # select section
        self._click_and_wait('section', 'zhonghe')
        self._click_and_wait('zhonghe', 'zhonghe_checked')
        self._click_and_wait('yonghe', 'yonghe_checked')

        # select type
        if self.rent_type == 'suite':
            self._click_and_wait('suite', 'suite_checked')
        elif self.rent_type == 'flat':
            self._click_and_wait('flat', 'flat_checked')
        else:
            raise Exception(f'Unsupported Rent Type: {self.rent_type}')

        # input price
        self._send_keys('price_min', self.price_min)
        self._send_keys('price_max', self.price_max)
        self._wait_for('price_submit')
        self._click_and_wait('price_submit', 'loading_now')
        self._wait_for('loading_completed')

        # input plain
        self._send_keys('plain_min', self.plain_min)
        self._send_keys('plain_max', self.plain_max)
        self._wait_for('plain_submit')
        self._click_and_wait('plain_submit', 'loading_now')
        self._wait_for('loading_completed')

        self._get_items()
        while self._is_exist('next_page'):
            self._click_and_wait('next_page', 'loading_now')
            self._wait_for('loading_completed')
            self._get_items()

        self.driver.quit()
