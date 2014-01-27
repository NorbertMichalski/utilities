# -*- coding: utf-8 -*-

import requests
import re, csv
import json
from lxml import html
from datetime import datetime, timedelta
from prices.tools.models import ProxyRotator
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

    # PROXY = {'http':'http://notherhalo:green444@38.78.197.196:60099'}
    PROXY = {}
    proxy_obj = ProxyRotator()

    def __init__(self, *args, **kwargs):
        self.proxy_obj = ProxyRotator()
        self.PROXY = json.loads(self.proxy_obj.rotate_proxy())
        print self.PROXY
        self.session = requests
        self.session.headers = self.HEADERS

    def clean_results(self, price):
        try:
            return float(re.search('[\d\.,]+', price).group(0).replace(',', ''))
        except AttributeError:
            return 0

class ElectricmotorwholesaleScraper(Scraper):

    def get_price(self, part_num):
        part_num = part_num.strip()
        self.PROXY = json.loads(self.proxy_obj.rotate_proxy())
        url = 'http://www.electricmotorwholesale.com/index.cfm?fuseaction=catalog.search'
        print url
        try:
            resp = self.session.post(url, proxies=self.PROXY, data={'searchQuery': part_num,
                                                                    'submitSearch':'Search'
                                                                    })
        except Exception as e:
            return 0
        x = html.fromstring(resp.content)
        try:
            price = x.xpath(".//div[contains(@class,'listCatalogProductSalePrice')]/text()")[0].strip()
        except IndexError:
            return 0
        return self.clean_results(price)

    def scrap(self, brand):
        pass



class GlobalindustrialScraper(Scraper):

    def get_price(self, part_num):
        part_num = part_num.strip()
        self.PROXY = json.loads(self.proxy_obj.rotate_proxy())
        url = 'http://www.globalindustrial.com/searchResult?ref=h%2Fsearch&q=' + part_num + '&x=31&y=15'
        print url
        try:
            resp = self.session.get(url, proxies=self.PROXY)
            print resp.text
        except Exception as e:
            print e
            return 0
        x = html.fromstring(resp.content)
        try:
            price = x.xpath(".//div[contains(@style,'font-size:14px; padding-top: 5px;') and contains(text(),'$')]/text()")[0].strip()
        except Exception as e:
            print e
            return 0
        return self.clean_results(price)

    def scrap(self, brand):
        pass



class SqoneScraper(Scraper):

    def get_price(self, part_num):
        part_num = part_num.strip()
        self.PROXY = json.loads(self.proxy_obj.rotate_proxy())
        url = 'http://www.sqone.com/index.cfm?fuseaction=catalog.search'
        print url
        try:
            resp = self.session.post(url, proxies=self.PROXY, data={'searchQuery': part_num,
                                                                    'submitSearch.x':'0',
                                                                    'submitSearch.y':'0',
                                                                    'submitSearch':'Search',
                                                                    })
        except Exception as e:
            print e
            return 0
        x = html.fromstring(resp.content)
        try:
            price = x.xpath(".//div[contains(@class,'listCatalogProductSalePrice')]/text()")[0].strip()
            print price
        except Exception as e:
            print e
            return 0
        return self.clean_results(price)

    def scrap(self, brand):
        pass


class TemcoScraper(Scraper):

    def get_price(self, part_num):
        part_num = part_num.strip()
        self.PROXY = json.loads(self.proxy_obj.rotate_proxy())
        url = 'http://www.temcoindustrialpower.com/search.html?t1=%s' % part_num
        print url
        try:
            resp = self.session.get(url, proxies=self.PROXY)
        except Exception as e:
            return 0
        x = html.fromstring(resp.content)
        try:
            title = x.xpath(".//table[@class='search_results']//td[@class='ctr']/a/text()")[0]
            if part_num not in title:
                return 0
            price = x.xpath(".//h3[contains(@class,'price')]/text()")[0]
        except IndexError:
            return 0
        return self.clean_results(price)

    def scrap(self, brand):
        pass


class MotoragentsScraper(Scraper):

    def get_price(self, part_num):
        brand = 'Baldor'
        part_num = part_num.strip()
        self.PROXY = json.loads(self.proxy_obj.rotate_proxy())
        url = 'http://www.motoragents.com/%sMotors/%s.html' % (brand.capitalize(), part_num)
        print url
        try:
            resp = self.session.get(url, proxies=self.PROXY)
        except Exception as e:
            return 0
        x = html.fromstring(resp.content)
        try:
            price = x.xpath(".//b/font[contains(text(),'$')]/text()")[0].strip()
        except IndexError as e:
            print e
            return 0
        return self.clean_results(price)

    def scrap(self, brand):
        pass


class WalkeremdScraper(Scraper):

    def get_price(self, part_num):
        part_num = part_num.strip()
        self.PROXY = json.loads(self.proxy_obj.rotate_proxy())
        url = 'http://www.walkeremd.com/SearchResults.asp?Search=%s' % part_num
        print url
        try:
            resp = self.session.get(url, proxies=self.PROXY)
        except Exception as e:
            print e
            return 0
        x = html.fromstring(resp.content)

        try:
            not_found = x.xpath(".//div[contains(@class,'additional_search_phrases') and contains(text(),'No exact matches found')] | .//td[contains(text(),'No products match your search criteria')]")[0]
            return 0
        except IndexError as e:
            pass

        try:
            price = x.xpath(".//font[contains(@class,'pricecolor colors_productprice')]/text()")[0].strip()
        except IndexError as e:
            print url
            return 0
        return self.clean_results(price)

    def scrap(self, brand):
        pass


class AlliedelecScraper(Scraper):

    def get_price(self, part_num):
        part_num = part_num.strip()
        self.PROXY = json.loads(self.proxy_obj.rotate_proxy())
        resp = self.session.get('https://www.alliedelec.com/')
        x = html.fromstring(resp.text)
        event_validation = x.xpath(".//input[@name='__EVENTVALIDATION']/@value")
        view_state = x.xpath(".//input[@name='__VIEWSTATE']/@value")
        previous_page = x.xpath(".//input[@name='__PREVIOUSPAGE']/@value")
        previous_page = x.xpath(".//input[@name='__PREVIOUSPAGE']/@value")
        try:
            resp = self.session.post('https://www.alliedelec.com/', proxies=self.PROXY, data={'__LASTFOCUS':'',
                                                                    '__EVENTTARGET':'',
                                                                    '__EVENTARGUMENT':'',
                                                                    '__VIEWSTATE': view_state,
                                                                    '__PREVIOUSPAGE': previous_page,
                                                                    '__EVENTVALIDATION': event_validation,
                                                                    'ctl00$txtSearch': part_num,
                                                                    'ctl00$btnSearch.x':'44',
                                                                    'ctl00$btnSearch.y':'6',
                                                                    'ctl00$contentMain$txtUserName':'',
                                                                    'ctl00$contentMain$txtPassword':'',
                                                                    'ctl00$contentMain$txtEmail':'your email address',
                                                                    })
        except Exception as e:
            print e
            return 0
        x = html.fromstring(resp.content)
        try:
            price = x.xpath(".//b[contains(text(),'$')]/text()")[0].strip()
        except IndexError:
            return 0
        return self.clean_results(price)

    def scrap(self, brand):
        pass


class DigikeyScraper(Scraper):

    def get_price(self, part_num):
        part_num = part_num.strip()
        self.PROXY = json.loads(self.proxy_obj.rotate_proxy())
        url = 'http://www.digikey.com/product-search/en?x=16&y=16&lang=en&site=us&KeyWords=%s' % part_num
        print url
        try:
            resp = self.session.get(url, proxies=self.PROXY)
            # print resp.text
        except Exception as e :
            print e
            return 0
        x = html.fromstring(resp.content)

        try:
            # price = x.xpath(".//th[contains(text(),'Price')]/ancestor::tr/following::tr/text()")[0].strip()
            price = x.xpath(".//td[re:match(text(), '\d+\.\d+')]/text()", namespaces={"re": "http://exslt.org/regular-expressions"})[1].strip()
            print price
        except IndexError as e:
            print e
            print url
            return 0
        return self.clean_results(price)

    def scrap(self, brand):
        pass



class PlccenterScraper(object):
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

    PROXY = {}
    proxy_obj = ProxyRotator()

    def __init__(self, brand):
        self.brand = brand
        self.proxy_obj = ProxyRotator()
        self.PROXY = json.loads(self.proxy_obj.rotate_proxy())
        print self.PROXY
        self.session = requests
        self.session.headers = self.HEADERS
    
    def clean_results(self, price):
        try:
            return float(re.search('[\d\.,]+', price).group(0).replace(',', ''))
        except AttributeError:
            return 0
    
    def get_price(self, part_num):
        part_num = part_num.strip()
        if self.brand == 'Redlion':
            url = 'http://www.plccenter.com/en-US/Buy/RED LION CONTROLS/%s' % part_num
        else:
            try:
                part_num = '%06d' % int(part_num)
                url = 'http://www.plccenter.com/en-US/Buy/RELIANCE ELECTRIC/%s' % part_num
            except:
                pass
                url = 'http://www.plccenter.com/en-US/Buy/DODGE/%s' % part_num
        print self.proxy_obj
        print self.proxy_obj.rotate_proxy()
        data = self.proxy_obj.rotate_proxy()
        self.PROXY = json.loads(data)

        print url
        try:
            resp = self.session.get(url, proxies=self.PROXY)
            print resp.url
        except Exception as e:
            print e
            return 0
        x = html.fromstring(resp.content)

        try:
            price = x.xpath(".//div[contains(@class,'productDetailPriceRowOurPrice')]/text()")[0].strip()
            if 'Est.' in price:
                price = price.split('Est.')[1]
            print price
        except IndexError as e:
            print e
            print url
            return 0
        return self.clean_results(price)

    def scrap(self, brand):
        pass



class TranscatScraper(Scraper):

    def get_price(self, part_num):
        part_num = part_num.strip()
        self.PROXY = json.loads(self.proxy_obj.rotate_proxy())
        url = 'http://www.transcat.com/catalog/productdetail.aspx?itemnum=%s' % part_num
        print url
        try:
            resp = self.session.get(url, proxies=self.PROXY)
            print resp.url
        except Exception as e:
            print e
            return 0
        x = html.fromstring(resp.content)

        try:
            price = x.xpath(".//span[contains(@id,'ctl00_ContentPlaceHolderMiddle_lblPrice1')]/font/text()")[0].strip()
            print price
        except IndexError as e:
            print e
            print url
            return 0
        return self.clean_results(price)

    def scrap(self, brand):
        pass



class NewarkScraper(Scraper):

    def get_price(self, part_num):
        part_num = part_num.strip()
        url = 'http://www.newark.com/jsp/viewDefault/search/advancedsearch.jsp?'
        print url
        self.PROXY = json.loads(self.proxy_obj.rotate_proxy())
        payload = { '_dyncharset':'UTF-8',
                    '/pf/search/AdvancedSearchFormHandler.searchErrorURL':'advancedsearch.jsp',
                    '_D:/pf/search/AdvancedSearchFormHandler.searchErrorURL':'',
                    'partNumber': part_num,
                    '_D:partNumber':'',
                    '_D:/pf/search/AdvancedSearchFormHandler.partNumberMatchMode':'',
                    '/pf/search/AdvancedSearchFormHandler.partNumberMatchMode':'2',
                    'description':'',
                    '_D:description':'',
                    '_D:/pf/search/AdvancedSearchFormHandler.descriptionMatchMode':'',
                    '/pf/search/AdvancedSearchFormHandler.descriptionMatchMode':'4',
                    '/pf/search/AdvancedSearchFormHandler.manufacturer':'',
                    '_D:/pf/search/AdvancedSearchFormHandler.manufacturer':'',
                    '/pf/search/AdvancedSearchFormHandler.manufacturerId':'0',
                    '_D:/pf/search/AdvancedSearchFormHandler.manufacturerId':'',
                    '_D:/pf/search/AdvancedSearchFormHandler.onlyInStockProducts':'',
                    '_D:/pf/search/AdvancedSearchFormHandler.excludeExtendedProductsRange':'',
                    '_D:/pf/search/AdvancedSearchFormHandler.includeNICs':'',
                    '_D:/pf/search/AdvancedSearchFormHandler.onlyRoHSProducts':'',
                    '/pf/search/AdvancedSearchFormHandler.search.x':'41',
                    '/pf/search/AdvancedSearchFormHandler.search.y':'15',
                    '_D:/pf/search/AdvancedSearchFormHandler.search':'',
                    '_DARGS':'/jsp/viewDefault/search/fragments/advancedsearch.jsp',

                   }
        try:
            resp = self.session.post(url, proxies=self.PROXY, data=payload)
        except Exception as e:
            print e
            return 0
        x = html.fromstring(resp.content)

        try:
            price = x.xpath(".//span[contains(@class,'mfProductDescriptionAndPrice')]/text()")[-1].strip()
            print price
        except IndexError as e:
            print e
            print url
            return 0
        return self.clean_results(price)

    def scrap(self, brand):
        pass



class WbdsScraper(Scraper):

    def get_price(self, part_num):
        brand = 'Baldor'
        part_num = part_num.strip()
        try:
            part_num = '%06d' % int(part_num)
        except:
            pass
        self.PROXY = json.loads(self.proxy_obj.rotate_proxy())
        url = 'http://www.wbds.com/htm/%s-Dod.htm' % part_num
        print url
        try:
            resp = self.session.get(url, proxies=self.PROXY)
        except Exception as e:
            return 0
        x = html.fromstring(resp.content)
        try:
            price = x.xpath(".//td[contains(@class,'headfont') and contains(text(),'Price')]/following-sibling::td/text()")[0].strip()
        except IndexError as e:
            print e
            return 0
        return self.clean_results(price)

    def scrap(self, brand):
        pass



class MotionindustriesScraper(Scraper):

    def get_price(self, part_num):
        part_num = part_num.strip()
        try:
            part_num = '%06d' % int(part_num)
        except:
            pass
        url = 'http://www.motionindustries.com/motion3/jsp/mii/productSearch.jsp'
        self.PROXY = json.loads(self.proxy_obj.rotate_proxy())
        payload = { 'AM_ACTION':'ProductSearchAM',
                    'BUS_ACTION':'MFR_ONLY',
                    'LANGUAGE':'0',
                    'AM_FIRST':'',
                    'PAGE_ID':'productSearch.jsp',
                    'SEARCH_TYPE':'A',
                    'SPECIAL_SEARCH':'',
                    'SEARCH_DESC': part_num,
                    'SEARCH_FIELD':'D',
                    'SELECT_MFR':'00250',
                    'MFR':'00250',
                    'SEARCH_CGC':'',
                    'ALL_MFR':'N',
                    'REMOVE_FILTER':'N',
                    'FILTER_LEVEL':'-1',
                    'FILTER_DESC':'Dodge',
                    'SET_4THLEVEL':'',
                    'lvl1_descr':'',
                    'lvl2_descr':'',
                    'lvl3_descr':'',
                    'lvl4_descr':'',
                    'lvl1_cgc':'',
                    'lvl2_cgc':'',
                    'lvl3_cgc':'',
                    'lvl4_cgc':'',
                    'PARAMETRIC_LEVEL':'1',
                    'PARAMETRIC_ACTION':'1',
                    'CATEGORY':'2',
                    'additional-search':''

                   }
        try:
            resp = self.session.post(url, proxies=self.PROXY, data=payload)
        except Exception as e:
            print e
            return 0
        x = html.fromstring(resp.content)

        try:
            price = float(x.xpath(".//input[contains(@name,'unit_price1')]/@value")[0].strip())
            print price
        except IndexError as e:
            print e
            print url
            return 0
        return self.clean_results(str(price))

    def scrap(self, brand):
        pass



class KscdirectScraper(Scraper):

    def scrap(self):
        f = open('/home5/shopmroc/utilities/prices/management/commands/kscdirect_results.csv', 'wb')
        f.close()
        f = open('/home5/shopmroc/utilities/prices/management/commands/kscdirect_links.csv', 'rb')
        links = f.readlines()
        results = []
        with open('/home5/shopmroc/utilities/prices/management/commands/kscdirect_results.csv', 'ab') as g:
            writer = csv.writer(g, dialect='excel')
            for link in links:
                url = unicode('http://www.kscdirect.com' + link.strip())
                print url
                self.PROXY = json.loads(self.proxy_obj.rotate_proxy())
                resp = self.session.get(url)
                x = html.fromstring(resp.content)
                try:
                    price = x.xpath(".//h3[contains(text(),'Your Price')]/text()")[0]
                    part_number = x.xpath(".//strong[contains(text(), 'MFG Part #:')]/following::td/text()")[0]
                    print 'part number %s with price %s' % (part_number, price)
                    writer.writerow((link, part_number, self.clean_results(str(price))))
                except:
                    continue


class WilliamsonScraper(Scraper):
    def get_price(self, part_num):
        brand = 'Baldor'
        part_num = part_num.strip()
        self.PROXY = json.loads(self.proxy_obj.rotate_proxy())
        url = 'http://williamsonneelectric.com/search.aspx?find=%s' % part_num
        print url
        try:
            resp = self.session.get(url, proxies=self.PROXY)
        except Exception as e:
            return 0
        x = html.fromstring(resp.content)
        try:
            price = x.xpath(".//span[contains(@class,'product-list-cost-value')]/text()")[0].strip()
        except IndexError as e:
            print e
            return 0
        return self.clean_results(price)

    def scrap(self, brand):
        pass


if __name__ == '__main__':
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
