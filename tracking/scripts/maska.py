# -*- coding: utf-8 -*-

import requests
from lxml import html
from datetime import datetime, timedelta

class MaskaScraper(object):

    USERNAME = 'ddurst_mdb'
    PASSWORD = 'larco1898'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.73 Safari/537.36',
                'Referer': 'https://www.baldorvip.com/',
                'Origin': 'https://www.baldorvip.com',
                'Host': 'www.baldorvip.com'
                }

    def __init__(self, *args, **kwargs):
        self.session = requests.Session()
        # cookies={'Culture': 'en-US', 'vipUsername': 'ddurst_mdb'},
                # headers=self.HEADERS
        self.session.cookies = {'Culture': 'en-US'}
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
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        )
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

    def get_tracking(self, order_num):
        if not self.logged_in:
            self.login()

        resp = self.session.get('https://baldorvip.com/OrderStatus')
        x = html.fromstring(resp.content)
        # we need to grab all this info to fill up the search form
        customer_number = x.xpath("//input[@id='CustomerNumber']/@value")[0]
        distribution_channel = x.xpath("//input[@id='DistributionChannel']/@value")[0]
        division = x.xpath("//input[@id='Division']/@value")[0]
        sales_org = x.xpath("//input[@id='SalesOrg']/@value")[0]
        today = datetime.now().strftime('%m/%d/%Y')
        month = timedelta(days=28)
        next_month = (datetime.now() + month).strftime('%m/%d/%Y')
        # submit the form
        resp = self.session.post('https://www.baldorvip.com/OrderStatus/Submit', data={
                'CustomerNumber': customer_number,
                'Language':'en',
                'DistributionChannel':distribution_channel,
                'Division': division,
                'SalesOrg': sales_org,
                'SalesOrderNumber':'',
                'PurchaseOrderNumber': order_num,
                'PartNumber':'',
                'StartDate': today,
                'EndDate': next_month,
                'Status':'ALL',
                'X-Requested-With':'XMLHttpRequest',

        }, allow_redirects=True, headers={'X-Requested-With': 'XMLHttpRequest',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
        # the response is actually a javascript redirect; grab the link
        try:
            redirect = str(resp.content).split("'")[1]
        except IndexError:
            # no redirect means wrong purchase order number
            return ''
        # the final page where the tracking number resides
        resp = self.session.get('https://www.baldorvip.com' + redirect)
        results = {}
        x = html.fromstring(resp.content)
        rows = x.xpath(".//div[@id='tabs-3']//table[contains(@class, 'defaultTable')]/tbody//tr")
        for row in rows:
            part_number = row.xpath(".//a[@data-linkmenu='product']/text()")[0]
            try:
                tracking_number = row.xpath(".//td[last()]/a/text()")[0]
                results[part_number] = tracking_number
            except IndexError:
                results[part_number] = ''
        return results


if __name__ == '__main__':
    scraper = MaskaScraper()
    # print scraper.get_availability('10H')
    print scraper.get_tracking('S1169534')
