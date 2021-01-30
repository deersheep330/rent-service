import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class RentParser():

    def __init__(self):
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        # options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
        self.url = 'https://rent.591.com.tw/?kind=0&region=1'
        self.elements = {
            'area_close': "//*[contains(@class, 'area-box-close')]",
            'credit_close': "//*[contains(@class, 'accreditPop')]//*[contains(@class, 'close')]",
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
            'next_page': "//*[contains(@class, 'pageNext') and not(contains(@class, 'last'))]"
        }
        self.price_min = '10000'
        self.price_max = '20000'
        self.plain_min = '8'
        self.plain_max = '18'
        self.items = []

    def __click_and_wait(self, target, expected):
        success = False
        while success is not True:
            try:
                _target = self.driver.find_element_by_xpath(self.elements[target])
                _target.click()
                WebDriverWait(self.driver, 15).until(
                    expected_conditions.presence_of_element_located((By.XPATH, self.elements[expected]))
                )
                success = True
            except Exception as e:
                print(e)

    def parse(self):
        print(f'==> parse page: {self.url}')

        self.driver.get(self.url)

        # select section
        self.__click_and_wait('section', 'shilin')
        '''
        WebDriverWait(driver, 15).until(
            expected_conditions.presence_of_element_located((By.XPATH, self.xpath))
        )
        elements = driver.find_elements_by_xpath(self.xpath)

        pattern = re.compile(r'\([^)]+\)')
        for ele in elements:
            #print(ele.text)
            arr = pattern.findall(ele.text)
            if arr is not None and len(arr) > 0:
                self.list.append(arr[0][1:-1])
            #print(self.list[-1])
        '''
        self.driver.quit()
