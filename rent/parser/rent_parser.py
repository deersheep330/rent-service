from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from sqlalchemy import exists
from webdriver_manager.chrome import ChromeDriverManager

from rent.db import create_engine_from_url, start_session, insert
from rent.models import House
from rent.utilities import get_db_connection_url


class RentParser():

    def __init__(self):

        self.engine = create_engine_from_url(get_db_connection_url())
        self.session = start_session(self.engine)

        self.wait_timeout = 10
        self.click_retry_timeout = 3

        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_setting_values.notifications': 2}
        options.add_experimental_option('prefs', prefs)
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
        self.url = 'https://rent.591.com.tw/?kind=0&region=1'
        self.elements = {
            'area_close': "//*[contains(@class, 'area-box-close')]",
            'credit_close': "//*[contains(@class, 'accreditPop') and not(contains(@style, 'none'))]//*[contains(@class, 'close')]",
            'section': "//*[contains(@google-data-stat, '按鄉鎮選擇')]",
            'shilin': "//label//span[contains(text(), '士林區')]",
            'shilin_checked': "//*[contains(@class, 'checkTips')]//span[contains(text(), '士林區')]",
            'type': "//*[contains(@class, 'search-rentType-span') and contains(@google-data-stat, '獨立套房')]",
            'type_checked': "//*[contains(@class, 'search-rentType-span') and contains(@class, 'select') and contains(@google-data-stat, '獨立套房')]",
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
        self.price_min = '10000'
        self.price_max = '20000'
        self.plain_min = '8'
        self.plain_max = '18'
        self.items = []
        self.new_items = []

    def __is_item_exist_in_db(self, item):
        return self.session.query(exists().where(House.id == item)).scalar()

    def get_new_items_url(self):
        if len(self.items) == len(self.new_items):
            print('first time ...')
            return []
        new_items_url = []
        for new_item in self.new_items:
            new_items_url.append(f'https://rent.591.com.tw/rent-detail-{new_item}.html')
        return new_items_url

    def __is_exist(self, target):
        try:
            self.driver.find_element_by_xpath(self.elements[target])
        except NoSuchElementException:
            return False
        return True

    def __wait_for(self, target):
        try:
            WebDriverWait(self.driver, self.wait_timeout).until(
                expected_conditions.presence_of_element_located((By.XPATH, self.elements[target]))
            )
            return True
        except Exception as e:
            print(e)
            return False

    def __click(self, target):
        self.driver.find_element_by_xpath(self.elements[target]).click()

    def __click_and_wait(self, target, expected):
        success = False
        while success is not True:
            try:
                _target = self.driver.find_element_by_xpath(self.elements[target])
                _target.click()
                WebDriverWait(self.driver, self.click_retry_timeout).until(
                    expected_conditions.presence_of_element_located((By.XPATH, self.elements[expected]))
                )
                success = True
            except Exception as e:
                print(e)

    def __send_keys(self, target, keys):
        _target = self.driver.find_element_by_xpath(self.elements[target])
        _target.send_keys(keys)

    def __get_items(self):
        items_per_page = self.driver.find_elements_by_xpath(self.elements['items'])
        for item in items_per_page:
            id = item.get_attribute('data-bind')
            if self.__is_item_exist_in_db(id):
                pass
            else:
                insert(self.session, House, {'id': id})
                self.session.commit()
                self.new_items.append(id)
                print(f'new item found: {id}')
            self.items.append(id)
        print(self.items)

    def parse(self):
        print(f'==> parse page: {self.url}')

        self.driver.get(self.url)

        # close modal
        self.__wait_for('area_close')
        self.__click('area_close')
        #self.__wait_for('credit_close')
        #self.__click('credit_close')

        # select section
        self.__click_and_wait('section', 'shilin')
        self.__click_and_wait('shilin', 'shilin_checked')

        # select type
        self.__click_and_wait('type', 'type_checked')

        # input price
        self.__send_keys('price_min', self.price_min)
        self.__send_keys('price_max', self.price_max)
        self.__wait_for('price_submit')
        self.__click_and_wait('price_submit', 'loading_now')
        self.__wait_for('loading_completed')

        # input plain
        self.__send_keys('plain_min', self.plain_min)
        self.__send_keys('plain_max', self.plain_max)
        self.__wait_for('plain_submit')
        self.__click_and_wait('plain_submit', 'loading_now')
        self.__wait_for('loading_completed')

        self.__get_items()
        while self.__is_exist('next_page'):
            self.__click_and_wait('next_page', 'loading_now')
            self.__wait_for('loading_completed')
            self.__get_items()

        self.driver.quit()
