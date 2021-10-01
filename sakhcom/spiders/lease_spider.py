from .sale_spider import SaleSpider


class LeaseSpaider(SaleSpider):
    name = "lease"
    url = 'https://dom.sakh.com/flat/lease/list1/?search_query=3d3430d1e16eefd3f01fe3af1fa28ca5'
    ad_url = 'https://dom.sakh.com/flat/lease/'
    next_page_url = f'https://dom.sakh.com/flat/lease/list'
    next_page_url_end = '/?search_query=3d3430d1e16eefd3f01fe3af1fa28ca5'