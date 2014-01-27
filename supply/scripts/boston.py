# -*- coding: utf-8 -*-

import requests
from lxml import html


class BostonScraper(object):

    USERNAME = 'msais'
    PASSWORD = 'larco1898'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.73 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Accept': '*/*',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding':'gzip,deflate,sdch',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive',
                'Referer': 'https://www.bostongear.com/smartcat/app/smartbuy/sb_logon.asp?dist=true&code=bostongear',
                'Origin': 'https://www.bostongear.com',
                'Host': 'www.bostongear.com'
                }

    def __init__(self, *args, **kwargs):
        self.session = requests.Session()
        self.session.headers = self.HEADERS
        self.logged_in = False

    def login(self):
        resp = self.session.get('https://www.bostongear.com/smartcat/app/smartbuy/sb_logon.asp?dist=true&code=bostongear')
        x = html.fromstring(resp.content)
        form_url = x.xpath('//form[@name="frmLogon"]/@action')[0]
        link = 'https://www.bostongear.com/smartcat/app/smartbuy/' + form_url
        resp = self.session.post(link, data={
            'Target':'../../sc_app/default.asp?MainLoc=../app/smartbuy/distributoronly.asp&code=bostongear',
            'vid':'15,100,3,0',
            'items': '',
            'txtUserName': self.USERNAME,
            'txtPassword': self.PASSWORD,
        }, allow_redirects=True)
        self.logged_in = True

    def get_availability(self, cat_num):
        if not self.logged_in:
            self.login()

        resp = self.session.get('http://www.bostongear.com/smartcat/app/smartbuy/sb_srchbody.asp?vid=0%2C0%2C0%2C0&prtNo=' + cat_num + '&desc=&upc=&mod=&custNo=')
        x = html.fromstring(resp.content)
        availability = {}
        for row in x.xpath("//table[contains(@id,'Table1')]//tr"):
            code = row.xpath(".//a[contains(@href,'javascript:ShowFacility')]/text()")[0].strip()
            avail = row.xpath(".//td[10]/font/text()")[0].strip()
            resp = self.session.get('http://www.bostongear.com/smartcat/app/smartbuy/ShowFacility.asp?fac=%s' % code)
            x = html.fromstring(resp.content)
            location = x.xpath("//td[contains(text(),'Location')]/following-sibling::td/text()")[0].strip()
            availability[location] = avail

        for location in availability:
            try:
                availability[location] = int(availability[location])
            except Exception:
                availability[location] = 0
        return availability


if __name__ == '__main__':
    scraper = BostonScraper()
    # print scraper.get_availability('10234')
    print scraper.get_tracking('S1167354')
