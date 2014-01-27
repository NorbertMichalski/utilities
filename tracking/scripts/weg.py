# -*- coding: utf-8 -*-

import requests
from lxml import html
from datetime import datetime


class WegScraper(object):

    USERNAME = 'ddurst@mechdrives.com'
    PASSWORD = 'ddurst18'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.73 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Referer': 'https://e-commerce.weg.net',
                'Origin': 'https://e-commerce.weg.net',
                'Host': 'e-commerce.weg.net'
                }

    APP_KEY = ''
    CUSTOMER_CODE = ''

    def __init__(self, *args, **kwargs):
        self.session = requests.Session()
        self.session.headers = self.HEADERS
        self.logged_in = False

    def login(self):
        self.session.get('https://e-commerce.weg.net/enter-pass.asp')
        resp = self.session.post('https://e-commerce.weg.net/login.asp', data={
            'username': self.USERNAME,
            'password': self.PASSWORD,
            'submit1.x':'33',
            'submit1.y':'7'
        }, allow_redirects=True)
        self.logged_in = True
        self.APP_KEY = resp.url.split('AppriseWebKey=')[1].split('&')[0]
        self.CUSTOMER_CODE = resp.url.split('AppriseCustCode=')[1].split('&')[0]

    def get_availability(self, cat_num):
        if not self.logged_in:
            self.login()
        resp = self.session.get('https://e-commerce.weg.net/invdisp.asp?AppriseWebKey=%s&AppriseCustCode=%s&product=%s' % (self.APP_KEY, self.CUSTOMER_CODE, cat_num))
        x = html.fromstring(resp.content)
        availability = {}
        table = x.xpath('//div[@id="tab-content-1"]//table[1]//table[1]//table[1]')[1]
        for row in table.xpath('.//tr'):
            try:
                location = row.xpath(".//td[@class='8'][3]/font/text()")[0].strip()
                if '-' in location:
                    location = location.split('-')[1].strip()
                avail = row.xpath(".//td[@class='8'][5]/font/text()")[0].strip()
                availability[location] = avail
            except IndexError:
                pass

        for location in availability:
            try:
                availability[location] = int(availability[location])
            except Exception:
                availability[location] = 0
        return availability

    def get_tracking(self, order_num):
        if not self.logged_in:
            self.login()
        today = datetime.now().strftime('%m/%d/%Y')
        self.session.get('https://e-commerce.weg.net/open-order.asp?AppriseWebKey=%s&AppriseCustCode=%s' % (self.APP_KEY, self.CUSTOMER_CODE))
        # get the link to the final tracking page
        resp = self.session.post('https://e-commerce.weg.net/open-order.asp', data={
                                'SearchText': order_num,
                                'requireddate': today,
                                'SearchType':'CustPO',
                                'AppriseCustCode': self.CUSTOMER_CODE,
                                'AppriseWebKey': self.APP_KEY,
                                'InPosition':'0'
                                })
        x = html.fromstring(resp.content)
        try:
            tracking_link = x.xpath(".//a[contains(@href,'./carrier.asp?')]/@href")[0]
        except IndexError:
            return ''
        # actual page with the tracking number
        resp = self.session.get('https://e-commerce.weg.net' + str(tracking_link[1:]))
        x = html.fromstring(resp.content)
        try:
            tracking_number = x.xpath(".//td[@class='8'][5]/font")[0].text_content().strip()
        except Exception as e:
            print e
            return 'NOT FOUND'
        return tracking_number

if __name__ == '__main__':
    scraper = WegScraper()
    # print scraper.get_availability('02518OT3P284T')
    print scraper.get_tracking('S1169437')
