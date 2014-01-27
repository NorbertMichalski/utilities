# -*- coding: utf-8 -*-

import requests
from lxml import html


class BandoScraper(object):

    USERNAME = 'jrobinson@larubber.com'
    PASSWORD = '1hehehaha'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.73 Safari/537.36',
                'Referer': 'http://www.idc-usa.com/',
                'Origin': 'http://www.idc-usa.com',
                'Host': 'www.idc-usa.com'
                }

    def __init__(self, *args, **kwargs):
        self.session = requests.Session()
        self.session.headers = self.HEADERS
        self.logged_in = False

    def login(self):
        self.session.get('http://www.idc-usa.com')
        resp = self.session.post('http://www.idc-usa.com/default.aspx?page=Logon', data={
            'txtEmail': self.USERNAME,
            'txtPassword':self.PASSWORD,
            'SubmitLogon_Content.x':'48',
            'SubmitLogon_Content.y':'7',
            'SubmitLogon_Content.x':'1'
        })
        self.logged_in = True

    def get_availability(self, cat_num):
        if not self.logged_in:
            self.login()
        resp = self.session.get('http://www.idc-usa.com/Default.aspx?Page=Uploaded%20Vendor%20Availability%20Report&ContentPage=TRUE&ItemCode=BAN+' + cat_num)
        x = html.fromstring(resp.content)
        availability = {}
        for row in x.xpath("//table[contains(@class,'UploadedVendorAvailabilityReport_Table')]//table"):
            locations = [i.strip() for i in row.xpath(".//td[1]/text()")]
            avail = [i.strip() for i in
                        row.xpath(".//td[2]/text()") if i.strip()]
            if locations:
                availability.update(dict(map(None, locations, avail)))

        availability = { key : value for key, value in availability.iteritems() if key != 'Total' }
        for location in availability:
            try:
                availability[location] = int(availability[location])
            except Exception:
                availability[location] = 0
        return availability

    
if __name__ == '__main__':
    scraper = BandoScraper()
    print scraper.get_availability('1040-8M-30')
