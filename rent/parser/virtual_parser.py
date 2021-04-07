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
from rent.utilities import get_db_connection_url


class VirtualParser():

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
        options.add_argument('window-size=1920,1080')
        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

        self.url = ''
        self.item_url_template_prefix = ''
        self.item_url_template_suffix = ''

        self.elements = {}

        self.items = []
        self.new_items = []

        count = delete_older_than(self.session, House, House.date, datetime.now().date() - timedelta(days=60))
        print(f'==> delete {count} old records ...')

    def _is_item_exist_in_db(self, item):
        return self.session.query(exists().where(House.id == item)).scalar()

    def get_new_items_url(self):
        if len(self.items) == len(self.new_items):
            print('==> first time parsing ...')
            return []
        new_items_url = []
        for new_item in self.new_items:
            new_items_url.append(self.item_url_template_prefix + new_item + self.item_url_template_suffix)
        return new_items_url

    def _is_exist(self, target):
        try:
            self.driver.find_element_by_xpath(self.elements[target])
        except NoSuchElementException:
            return False
        return True

    def _wait_for(self, target):
        try:
            WebDriverWait(self.driver, self.wait_timeout).until(
                expected_conditions.presence_of_element_located((By.XPATH, self.elements[target]))
            )
            return True
        except Exception as e:
            print(e)
            return False

    def _click(self, target):
        self.driver.find_element_by_xpath(self.elements[target]).click()

    def _click_and_wait(self, target, expected):
        success = False
        retry = 0
        max_retry = 10
        while success is not True and retry < max_retry:
            try:
                _target = self.driver.find_element_by_xpath(self.elements[target])
                _target.click()
                WebDriverWait(self.driver, self.click_retry_timeout).until(
                    expected_conditions.presence_of_element_located((By.XPATH, self.elements[expected]))
                )
                success = True
            except Exception as e:
                print(e)
                traceback.print_exception(type(e), e, e.__traceback__)
                self.driver.save_screenshot('test.png')
            retry += 1

    def _send_keys(self, target, keys):
        _target = self.driver.find_element_by_xpath(self.elements[target])
        _target.send_keys(keys)

    def _get_items(self):
        items_per_page = self.driver.find_elements_by_xpath(self.elements['items'])
        for item in items_per_page:
            try:
                id = item.get_attribute('data-bind')
                if self._is_item_exist_in_db(id):
                    pass
                else:
                    insert(self.session, House, {'id': id})
                    self.session.commit()
                    self.new_items.append(id)
                    print(f'new item found: {id}')
                self.items.append(id)
            except Exception as e:
                print(f'Cannot find {item} anymore: {e}')
        print(self.items)

    def parse(self):
        if self.url == '' or self.item_url_template_prefix == '' or self.item_url_template_suffix == '':
            raise RuntimeError('url, item_url_template_prefix and item_url_template_suffix should be provided!')
        print(f'==> parse page: {self.url}')
