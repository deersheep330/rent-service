from rent.parser.virtual_parser import VirtualParser


class RentParser(VirtualParser):

    def __init__(self,
                 is_first_time = False,
                 rent_type='flat',
                 price_min='10000',
                 price_max='20000',
                 plain_min='15',
                 plain_max='80'):

        super().__init__(is_first_time=is_first_time)

        self.url = 'https://rent.591.com.tw/?kind=1&region=3&section=37,38&searchtype=1&area=15,80&showMore=1&multiPrice=10000_20000'
        self.item_url_template_prefix = 'https://rent.591.com.tw/rent-detail-'
        self.item_url_template_suffix = '.html'

        self.elements = {
            'items': "//*[contains(@class, 'vue-list-rent-item')]/a[@href]",
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

        print(f'*** rent parsing start ***')

        super().parse()

        try:
            self.driver.get(self.url)
            self._wait_for('loading_completed')

            self._get_items('href')
            while self._is_exist('next_page'):
                self._click_and_wait('next_page', 'loading_now')
                self._wait_for('loading_completed')
                self._get_items('href')

        except Exception as e:
            print(f'*** rent parsing exception {e} ***')
        finally:
            self.driver.quit()
            print(f'*** rent parsing return ***')
