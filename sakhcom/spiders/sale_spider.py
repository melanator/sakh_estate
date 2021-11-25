import scrapy
from scrapy.loader import ItemLoader
from sakhcom.items import SakhcomItem
from datetime import datetime

class SaleSpider(scrapy.Spider):
    name = 'sale'

    # URL for navigating throughout website
    start_url = 'https://dom.sakh.com/flat/sell/list1/'
    ad_url = 'https://dom.sakh.com/flat/sell/'

    next_page_url = 'https://dom.sakh.com/flat/sell/list'
    next_page_url_end = '/'

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse)

    def parse(self, response):

        # Retrive on which page we are on this iteration
        ads_count = int(response.xpath(
            '//div[@class="pages"]/div[@class="title"]/b/text()').get())
        pages = (ads_count // 20) + 1 #Must be 20
        current_page = int(response.xpath(
            '//div[@class="pages"]//div[@class="item selected"]/text()').get())
        next_page_url = self.next_page_url + \
            str(current_page + 1) + self.next_page_url_end

        self.logger.info(f'parsing URL: {response.url}', )

        for offer in response.xpath('//div[@class="offers"]/div[@class="item"]'):
            ad_id = offer.xpath(
                './/span[@title="Номер объявления"]/text()').get()
            ad_id = ad_id[2:]  # Delete '№ ' beginning
            ad_url = self.ad_url + ad_id

            yield response.follow(ad_url, self.parse_ad, meta={'ad_id': ad_id})

        # Check if reached last page
        if current_page < pages:
            yield response.follow(next_page_url, callback=self.parse)
        else:
            self.logger.info(f'Last page reached. Stop spides.')

    def parse_ad(self, response):
        """
        Get item from ad page.
        """
        loader = ItemLoader(item=SakhcomItem(), selector=response)
        loader.add_value('ad_id', response.meta['ad_id'])
        loader.add_xpath('price', './/span[@class="value"]/text()')
        loader.add_xpath('area', './/div[@class="area"]/text()')
        loader.add_xpath('floor', './/div[@class="area"]/text()[2]')
        loader.add_xpath('room', './/div[@id="offer"]/h3/text()')
        loader.add_xpath('address', './/div[@id="offer"]/h4/text()')
        loader.add_xpath(
            'address', './/div[@id="offer"]//span[@class="text"]/text()')
        loader.add_xpath('params', './/div[@class="params"]/div/text()')
        loader.add_xpath('added', './/div[@class="stat"]/div/text()[1]')
        loader.add_xpath('updated', './/div[@class="stat"]/div/span/text()')
        loader.add_xpath(
            'photo_inside', './/div[@class="photos clearfix"]//div[@class="preview"]')
        loader.add_xpath(
            'photo_outside', './/div[@class="photos clearfix"][2]//img/@src')
        loader.add_value('scraped', datetime.today().date())

        yield loader.load_item()
