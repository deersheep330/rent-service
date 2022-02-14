import traceback

from rent.parser.virtual_parser import VirtualParser


class SaleParser(VirtualParser):

    def __init__(self,
                 is_first_time=False,
                 price_min='200',
                 price_max='555',
                 age_min='1',
                 age_max='30'):

        super().__init__(is_first_time=is_first_time)

        self.url = 'https://sale.591.com.tw/?shType=list&regionid=2&kind=9&houseage=$_33$&shape=3,4&price=333$_777$'
        self.item_url_template_prefix = 'https://sale.591.com.tw/home/house/detail/2/'
        self.item_url_template_suffix = '.html'

        self.elements = {

            'intercepted': "//div[contains(@class, 'union_responsive')]",

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

            'rooms_3': "//*[contains(@class, 'pattern')]//*[contains(@data-gtm-stat, '3房')]",
            'rooms_3_checked': "//*[contains(@class, 'pattern')]//*[contains(@data-gtm-stat, '3房') and contains(@class, 'select')]",
            'rooms_4': "//*[contains(@class, 'pattern')]//*[contains(@data-gtm-stat, '4房')]",
            'rooms_4_checked': "//*[contains(@class, 'pattern')]//*[contains(@data-gtm-stat, '4房') and contains(@class, 'select')]",

            'age': "//*[contains(@class, 'houseage')]//*[contains(text(), '屋齡')]",
            'age_min': "//*[contains(@class, 'filter-more-list') and not(contains(@style, 'none'))]//input[contains(@class, 'min')]",
            'age_max': "//*[contains(@class, 'filter-more-list') and not(contains(@style, 'none'))]//input[contains(@class, 'max')]",
            'age_submit': "//*[contains(@class, 'filter-more-list') and not(contains(@style, 'none'))]//*[contains(@class, 'submit')]",

            'items': "//*[@data-bind and contains(@class, 'houseList-item') and not(contains(@class, 'houseList-item-collect'))]",
            'next_page': "//*[contains(@class, 'pageNext') and not(contains(@class, 'last'))]",

            'loading_now': "//*[@rel='loading' and not(contains(@style, 'none'))]",
            'loading_completed': "//*[@rel='loading' and contains(@style, 'none')]"
        }

        # price and age should be type of string
        self.price_min = price_min
        self.price_max = price_max
        self.age_min = age_min
        self.age_max = age_max

    def parse(self):

        print(f'*** sale parsing start ***')

        super().parse()

        try:
            completed = False
            retry = 0
            max_retry = 3
            while not completed and retry < max_retry:
                try:

                    self.driver.get(self.url)
                    self._wait_for('loading_completed')

                    if self._is_exist('intercepted'):
                        self.driver.execute_script("document.getElementsByClassName('union_responsive')[0].remove()")

                    self._get_items()
                    _retry = 0
                    _max_retry = 10
                    while _retry < _max_retry and self._is_exist('next_page'):
                        self._click_and_wait('next_page', 'loading_now')
                        self._wait_for('loading_completed')
                        self._get_items()
                        _retry += 1
                    completed = True
                except Exception as e:
                    print(e)
                    if retry == max_retry:
                        raise e
                    else:
                        print(f'retry: {retry}')
                finally:
                    retry += 1
        except Exception as _e:
            print(f'*** sale parsing exception {_e} ***')
        finally:
            self.driver.quit()
            print(f'*** sale parsing return ***')