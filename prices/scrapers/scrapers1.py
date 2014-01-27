# -*- coding: utf-8 -*-

import grequests
import re
from lxml import html
from datetime import datetime, timedelta
# from prices.settings.models import Proxy
# import prices.settings.models



class Scraper(object):

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

    def clean_results(self, price):
        try:
            return re.search('[\d\.,]+', price).group(0)
        except AttributeError:
            return ''

class WholesaleScraper(Scraper):

    def get_price(self, part_num):
        url = 'http://www.electricmotorwholesale.com/index.cfm?fuseaction=catalog.search'
        try:
            resp = self.session.post(url, proxies=self.PROXY, data={'searchQuery': part_num,
                                                                    'submitSearch':'Search'
                                                                    })
        except:
            return e
        x = html.fromstring(resp.content)
        try:
            price = x.xpath(".//div[contains(@class,'listCatalogProductSalePrice')]/text()")[0].strip()
        except IndexError:
            return ''
        return self.clean_results(price)

    def scrap(self, brand):
        pass



class GlobalindustrialScraper(Scraper):

    def get_price(self, part_num):
        url = 'http://www.globalindustrial.com/searchResult?ref=h%2Fsearch&q=' + part_num + '&x=31&y=15'
        try:
            resp = self.session.get(url, proxies=self.PROXY)
        except:
            return e
        x = html.fromstring(resp.content)
        try:
            price = x.xpath(".//div[contains(@style,'font-size:14px; padding-top: 5px;') and contains(text(),'$')]/text()")[0].strip()
        except IndexError:
            return ''
        return self.clean_results(price)

    def scrap(self, brand):
        pass



class SqoneScraper(Scraper):

    def get_price(self, part_num):
        url = 'http://www.sqone.com/index.cfm?fuseaction=catalog.search'
        try:
            resp = self.session.post(url, proxies=self.PROXY, data={'searchQuery': part_num,
                                                                    'submitSearch.x':'0',
                                                                    'submitSearch.y':'0',
                                                                    'submitSearch':'Search',
                                                                    })
        except:
            return e
        x = html.fromstring(resp.content)
        try:
            price = x.xpath(".//div[contains(@class,'listCatalogProductSalePrice')]/text()")[0].strip()
        except IndexError:
            return ''
        return self.clean_results(price)

    def scrap(self, brand):
        pass


class TemcoScraper(Scraper):

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
        return self.clean_results(price)

    def scrap(self, brand):
        pass


class MotoragentScraper(Scraper):

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
        return self.clean_results(price)

    def scrap(self, brand):
        pass


class WalkerScraper(Scraper):

    def get_price(self, part_num):
        url = 'http://www.walkeremd.com/SearchResults.asp?Search=%s' % part_num
        try:
            resp = self.session.get(url, proxies=self.PROXY)
        except:
            return e
        x = html.fromstring(resp.content)

        try:
            not_found = x.xpath(".//div[contains(@class,'additional_search_phrases') and contains(text(),'No exact matches found')] | .//td[contains(text(),'No products match your search criteria')]")[0]
            return ''
        except IndexError as e:
            pass

        try:
            price = x.xpath(".//font[contains(@class,'pricecolor colors_productprice')]/text()")[0].strip()
        except IndexError as e:
            print url
            return ''
        return self.clean_results(price)

    def scrap(self, brand):
        pass




if __name__ == '__main__':
    '''
    scraper = WalkerScraper()
    print scraper.get_price('mumu')
    scraper = WholesaleScraper()
    print scraper.get_price('AEM2238-4')
    scraper = GlobalindustrialScraper()
    print scraper.get_price('AEM2238-4')
    scraper = SqoneScraper()
    print scraper.get_price('AEM2238-4')
    scraper = TemcoScraper()
    print scraper.get_price('AEM2238-4')
    scraper = MotoragentScraper()
    print scraper.get_price('CL1301', 'baldor')
    '''
    urls = [
    'http://www.heroku.com',
    'http://python-tablib.org',
    'http://httpbin.org',
    'http://docs.python-requests.org/en/latest/',
    'http://kennethreitz.com'
]
    rs = (grequests.get(u) for u in urls)
    print grequests.map(rs)
