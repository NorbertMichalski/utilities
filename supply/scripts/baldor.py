# -*- coding: utf-8 -*-

import requests
from lxml import html
from datetime import datetime, timedelta


class BaldorScraper(object):

    USERNAME = 'mmenashe_mdb'
    PASSWORD = 'green444'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.73 Safari/537.36',
                'Referer': 'https://www.baldorvip.com/',
                'Origin': 'https://www.baldorvip.com',
                'Host': 'www.baldorvip.com'
                }

    def __init__(self, *args, **kwargs):
        self.session = requests.Session()
        self.session.headers = self.HEADERS
        self.logged_in = False

    def login(self):
        self.session.get('https://www.baldorvip.com/')
        self.session.post('https://www.baldorvip.com/Account/LogIn', data={
            'ReturnUrl': '',
            'UserName': self.USERNAME,
            'Password': self.PASSWORD,
            'SavePassword': 'false',
            'X-Requested-With': 'XMLHttpRequest'
        },
            headers={'X-Requested-With': 'XMLHttpRequest',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
            cookies={'Culture': 'en-US'})
        self.logged_in = True

    def get_availability(self, cat_num):
        if not self.logged_in:
            self.login()
        resp = self.session.get('https://www.baldorvip.com/Product/Search?SearchString=%s&SearchCategory=P&SearchType=E' % cat_num)
        x = html.fromstring(resp.content)
        availability = {}
        for row in x.xpath("//table[contains(@class,'availabilityTable')]//tr"):
            locations = row.xpath(".//td/a/text()")
            avail = [i.strip() for i in
                        row.xpath(".//td[a]/following-sibling::td[1]/text()") if i.strip()]
            if locations:
                availability.update(dict(map(None, locations, avail)))
        for location in availability:
            try:
                availability[location] = int(availability[location])
            except Exception:
                availability[location] = 0
        return availability

    
if __name__ == '__main__':
    scraper = BaldorScraper()
    # print scraper.get_availability('AEM2238-4')
    print scraper.get_tracking('S1169886')