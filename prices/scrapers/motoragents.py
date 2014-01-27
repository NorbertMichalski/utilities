# -*- coding: utf-8 -*-

import requests
from lxml import html
from datetime import datetime, timedelta
# from prices.settings.models import Proxy
# import prices.settings.models



class MotoragentScraper(object):

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


    def get_price(self, part_num, brand):
        url = 'http://www.motoragents.com/%sMotors/%s.html' % (brand.capitalize(), part_num)
        try:
            resp = self.session.get(url, proxies=self.PROXY)
        except:
            return e
        x = html.fromstring(resp.content)
        try:
            price = x.xpath(".//b/font[contains(text(),'$')]/text()")[0].strip()
        except IndexError as e:
            print e
            return ''
        return price

    def scrap(self, brand):
        pass

if __name__ == '__main__':
    scraper = MotoragentScraper()
    print scraper.get_price('CL1301', 'baldor')
