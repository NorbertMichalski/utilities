# -*- coding: utf-8 -*-

import requests
from lxml import html
from datetime import datetime, timedelta
# from prices.settings.models import Proxy
# import prices.settings.models



class TemcoScraper(object):

    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.73 Safari/537.36',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset':'utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding':'gzip,deflate,sdch',
                'Accept-Language':'it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4',
                'Connection':'keep-alive',
                'Content-Type':'application/x-www-form-urlencoded',
                # 'Referer': '',
                # 'Origin': '',
                # 'Host': ''
                }

    PROXY = ''

    def __init__(self, *args, **kwargs):
        # self.PROXY = Proxy().rotate_proxy()
        self.session = requests
        self.session.headers = self.HEADERS


    def get_price(self, part_num):
        url = 'http://www.temcoindustrialpower.com/search.html?t1=%s' % part_num
        try:
            resp = self.session.get(url, proxies=self.PROXY)
        except:
            return e
        x = html.fromstring(resp.content)
        try:
            price = x.xpath(".//h3[contains(@class,'price')]/text()")[0]
        except IndexError:
            return ''
        return price

    def scrap(self, brand):
        pass

if __name__ == '__main__':
    scraper = TemcoScraper()
    print scraper.get_price('AEM2238-4')
