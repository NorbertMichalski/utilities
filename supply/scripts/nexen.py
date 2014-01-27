# -*- coding: utf-8 -*-

import requests
from lxml import html


class NexenScraper(object):

    USERNAME = 'larubber'
    PASSWORD = 'larubber1898'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.73 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Referer': 'http://www.nexengroup.com/nxn/users/index/login/',
                'Origin': 'http://www.nexengroup.com/nxn/users/index/login',
                'Host': 'www.nexengroup.com'
                }

    def __init__(self, *args, **kwargs):
        self.session = requests.Session()
        self.session.headers = self.HEADERS
        self.logged_in = False

    def login(self):
        self.session.get('http://www.nexengroup.com/nxn/users/index/login')
        resp = self.session.post('http://www.nexengroup.com/nxn/users/index/login', data={
            'referer': 'http://www.nexengroup.com/',
            'username': self.USERNAME,
            'password': self.PASSWORD,
            'submit': 'Login',
        })
        self.logged_in = True

    def get_availability(self, cat_num):
        if not self.logged_in:
            self.login()
        resp = self.session.get('http://www.nexengroup.com/nxn/default/products/details/id/%s' % cat_num)
        x = html.fromstring(resp.content)
        availability = {}
        try:
            avail = x.xpath("//span[contains(@class,'price')]/table//th[.='Qty Available:']/following::td")[0].text_content()
            if '*' in avail:
                availability['nexen'] = avail.split('*')[0].strip()
            else:
                availability['nexen'] = avail.strip()
        except IndexError as e:
            print e
            print 'wrong part number'
        for location in availability:
            try:
                availability[location] = int(availability[location])
            except Exception:
                availability[location] = 0
        return availability

if __name__ == '__main__':
    scraper = NexenScraper()
    print scraper.get_availability('800100')
