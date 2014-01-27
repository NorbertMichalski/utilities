# -*- coding: utf-8 -*-

import requests
from lxml import html
import json
import datetime


class ClickyScraper(object):
    base_url = 'http://api.clicky.com/api/stats/4?site_id=66501030&sitekey=12489b40c2cf0373'
    
    def get_visits(self, date=datetime.date.today()):
        link = self.base_url + '&type=pages&output=json&limit=all&date=%s' %date
        resp = requests.get(link)
        dict = json.loads(resp.content)
        visits = dict[0]['dates'][0]['items']
        print date
        return visits

    def brand_visits(self, brand, date=datetime.date.today()):
        keywords = {'baldor':['baldor', 'maska'], 'leeson': ['lincoln', 'leeson', 'grove-gear', 'grove_gear', 'electra'],
                    'redlion': ['redlion'], 'dodge':['dodge'], 'all':['']
                    }
        search_keywords = keywords[brand.lower()]
        count = 0
        visits = self.get_visits(date)
        if brand.lower() == 'all':
            return len(visits)
        for visit in visits:
            try:
                title = visit['title'].lower()
                for keyword in search_keywords:
                    if keyword in title:
                        count += int(visit['value'])
                        #print title
                        break
            except:
                title = visit['url'].lower()
                for keyword in search_keywords:
                    if keyword in title:
                        count += int(visit['value'])
                        #print title
                        break
        return count
        

class RankScraper(object):
    USER = 'matthew'
    PASSWORD = 'menashe'
    BASE_URL = 'rank-checker.crasch.com.ar/'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.73 Safari/537.36',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding':'gzip,deflate,sdch',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                }

    def __init__(self, *args, **kwargs):
        self.session = requests.Session()
        self.session.headers = self.HEADERS
        self.logged_in = False
    
    def login(self):
        url = "https://%s:%s@%s" %(self.USER, self.PASSWORD, self.BASE_URL)
        try:
            resp = self.session.get(url, verify=False)
            self.logged_in = True
            return resp.content
        except Exception as e:
            # this website is often down
            self.logged_in = False
            return ''
        
    def get_rank(self, brand):
        if not self.logged_in:
            content = self.login()
        # this website is often down
        try:
            x = html.fromstring(content)
        except Exception as e:
            return
        try:
            completion_rates = x.xpath(".//div[@class='reliability']/text()")
        except Exception as e:
            # this website is often down
            print e
            return
        for index, completion in enumerate(completion_rates):
            #print completion
            rate = float(completion.split(' ')[1][:-1])
            if rate > 30:
                latest_complete = index
                break
        
        if brand == 'all':
            try:
                brand_div = x.xpath(".//div[@class='panel']")[0]
                last_ranks = brand_div.xpath(".//td[contains(text(),'Avg. ranking')]/following-sibling::td/span/text()")
                latest_rank = last_ranks[latest_complete].strip()
                return latest_rank
            except Exception as e:
                print e
                return
        brand_name = brand.capitalize()
        if brand_name=='Redlion':
            brand_name = 'Red Lion Controls'
        try:
            brand_div = x.xpath(".//div[@id=$name]", name=brand_name)[0]
            last_ranks = brand_div.xpath(".//td[contains(text(),'Avg. ranking')]/following-sibling::td/span/text()")
            latest_rank = last_ranks[latest_complete].strip()
            return latest_rank
        except Exception as e:
            print e
            return

class OrderScraper(object):
    USER = 'mmenashe'
    PASSWORD = 'green444'
    BASE_URL = 'http://184.169.158.235/admin/'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.73 Safari/537.36',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding':'gzip,deflate,sdch',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host':'184.169.158.235',
                'Origin':'http://184.169.158.235',
                'Referer':'http://184.169.158.235/admin/',
                }

    def __init__(self, *args, **kwargs):
        self.session = requests.Session()
        self.session.headers = self.HEADERS
    
    def get_sales(self, brand, today = datetime.date.today()):
        tomorrow = today + datetime.timedelta(days=1)
        brand_name = brand.lower()
        keywords = {'baldor':['baldor', 'maska'], 'leeson': ['lincoln', 'leeson', 'electra'],
                    'redlion': ['redlion'], 'dodge':['dodge'], 'all':['']
                    }
        search_keywords = keywords[brand]
        count = 0
        
        url = self.BASE_URL
        resp = self.session.get(url)
        x = html.fromstring(resp.content)
        token = x.xpath(".//input[@name='csrfmiddlewaretoken']/@value")[0]
        resp = self.session.post(url, data={'csrfmiddlewaretoken': token,
                                            'username': self.USER,
                                            'password': self.PASSWORD,
                                            'this_is_the_login_form':'1',
                                            'next': ('/admin/orders/order/?created_at__lt=' + str(tomorrow) + '+00%3A00%3A00-07%3A00&'
                                                     'created_at__gte=' + str(today) +'+00%3A00%3A00-07%3A00')
                                            
                                            
                                            }, allow_redirects=True)
        x = html.fromstring(resp.content)
        rows = x.xpath(".//table[@id='result_list']/tbody/tr")
        all_sales = len(rows)
        print 'day\'s all sales', all_sales
        if brand_name == 'all':
            return all_sales
        for row in rows:
            for keyword in search_keywords:
                supplier = row.xpath(".//td[7]/text()")[0].lower()
                #print supplier
                if keyword in supplier:
                    count += 1
    
        return count
        

class CashScraper(object):
    BASE_URL = 'http://184.169.158.235/api/order_statistic/'
    TOKEN = '/?token=n075fK4uUtYyXSJ0xdcVgs8s0C1vRRWNNnbVn0E1DzhYV13Rzx'
    
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.73 Safari/537.36',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding':'gzip,deflate,sdch',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host':'184.169.158.235',
                'Origin':'http://184.169.158.235',
                'Referer':'http://184.169.158.235/admin/',
                }
    
    def __init__(self, *args, **kwargs):
        self.session = requests.Session()
        self.session.headers = self.HEADERS
        
    def get_money(self, date=datetime.date.today()):
        url = self.BASE_URL + date.strftime('%Y/%m/%d') + self.TOKEN
        resp = self.session.get(url)
        dict = json.loads(resp.content)
        print 'money for the day ', dict["total_ext_price"]   
        return dict["total_ext_price"]    
        
    
if __name__ == '__main__':
    scraper = ClickyScraper()
    print scraper.brand_visits('baldor')
    print scraper.brand_visits('leeson')
    print scraper.brand_visits('dodge')
    print scraper.brand_visits('redlion')
    #scraper = RankScraper()
    #scraper.get_rank('baldor')
    scraper = OrderScraper()
    print scraper.get_sales('baldor')