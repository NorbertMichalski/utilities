# -*- coding: utf-8 -*-

import requests
from lxml import html


class RedlionScraper(object):

    # USERNAME = 'redcat'
    PASSWORD = 'redcat'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.73 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Referer': 'sellmore.redlion.net',
                'Origin': 'sellmore.redlion.net',
                'Host': 'sellmore.redlion.net'
                }

    def __init__(self, *args, **kwargs):
        self.session = requests.Session()
        self.session.headers = self.HEADERS
        self.logged_in = False

    def login(self):
        self.session.get('http://sellmore.redlion.net/newpass.plx')
        resp = self.session.post('http://sellmore.redlion.net/newpass.plx', data={
            'code': self.PASSWORD,
        })
        self.logged_in = True

    def get_availability(self, cat_num):
        if not self.logged_in:
            self.login()
        new_headers = [ ('Referer', 'http://www.redlion.net/stock/stockcheck.asp'),
                        ('Origin', 'http://www.redlion.net'),
                        ('Host', 'www.redlion.net')
                    ]
        self.session.headers.update(new_headers)
        resp = self.session.post('http://www.redlion.net/stock/stockcheck.asp', data={
            'pagenum': '1',
            'part': cat_num,
        })
        x = html.fromstring(resp.content)
        availability = {}
        try:
            avail = x.xpath("//*[@id='row1']/td[3]")[0].text_content().strip()
            if avail == '****':
                avail = 0
            availability['redlion'] = avail
        except IndexError as e:
            print e
            print 'wrong part number'
        for location in availability:
            try:
                availability[location] = int(availability[location])
            except Exception:
                availability[location] = 0
        return availability

    def get_tracking(self, order_num):
        if not self.logged_in:
            self.login()
        new_headers = [ ('Referer', 'http://www.redlion.net/stock/CustomerPOTracking.asp'),
                        ('Origin', 'http://www.redlion.net'),
                        ('Host', 'www.redlion.net')
                    ]

        self.session.headers.update(new_headers)
        resp = self.session.post('http://www.redlion.net/stock/CustomerPOTracking.asp', data={
            'pagenum': '1',
            'custpo': order_num,
        })
        results = {}
        x = html.fromstring(resp.content)
        try:
            tracking_number = x.xpath(".//td[contains(text(),'Tracking Number')]/following-sibling::td")[0].text_content().strip()
            return tracking_number
        except:
            return 'NOT FOUND'

if __name__ == '__main__':
    scraper = RedlionScraper()
    # print scraper.get_availability('CUB7P010')
    print scraper.get_tracking('S1168527')
