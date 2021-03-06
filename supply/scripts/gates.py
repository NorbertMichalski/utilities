# -*- coding: utf-8 -*-

import requests
from lxml import html
from datetime import datetime
from time import sleep


class GatesScraper(object):

    USERNAME = 'ddurst'
    PASSWORD = 'larco1898'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.73 Safari/537.36',
                'Referer': 'https://www.ptplace.com',
                'Origin': 'https://www.ptplace.com',
                'Host': 'www.ptplace.com'
                }

    def __init__(self, *args, **kwargs):
        self.session = requests.Session()
        self.session.headers = self.HEADERS
        self.logged_in = False

    def login(self):
        self.session.get('https://www.ptplace.com/ptp/do/mall')
        resp = self.session.post('https://www.ptplace.com/ptp/do/login', data={
            'username': self.USERNAME,
            'password': self.PASSWORD,
            'newStore':'Gates',
            'loginButton':'Go',
            'selectedlanguage':'English',
            'navbartype':'Mall',
            'selectedcountry':'USA',
            'selectedstore':'PTPlace',
            'viewstore':'false',
            'bflag':'',
            'js_enabled':'true',
        })
        self.logged_in = True


    def get_availability(self, cat_num):
        today = datetime.now().strftime("%m/%d/%Y")
        if not self.logged_in:
            self.login()
        resp = self.session.get('https://www.ptplace.com/ptp/do/pricingEntryLine?lastPageViewed=pricingEntryLine&navbartype=Store&selectedcountry=USA&viewstore=false&selectedstore=Gates&bflag=false&selectedlanguage=English')
        x = html.fromstring(resp.content)
        token = x.xpath('//input[@name="org.apache.struts.taglib.html.TOKEN"]/@value')
        new_headers = [ ('Referer', 'https://www.ptplace.com/ptp/do/pricingEntryLine?lastPageViewed=pricingEntryLine&navbartype=Store&selectedcountry=USA&viewstore=false&selectedstore=Gates&bflag=false&selectedlanguage=English')]
        self.session.headers.update(new_headers)
        resp = self.session.post('https://www.ptplace.com/ptp/do/pricingEntryLine', data={
            'org.apache.struts.taglib.html.TOKEN':token,
            'selectedcountry':'USA',
            'selectedlanguage':'English',
            'viewstore':'false',
            'selectedstore':'Gates',
            'navbartype':'Store',
            'bflag':'false',
            'orderHeaderForm.oemNumber':'',
            'orderHeaderForm.quoteID':'',
            'entryLinesForm.checkPA':'true',
            'entryLinesForm.elDefaultsForm.partType':'VENDOR',
            'entryLinesForm.requestedShipDate': today,
            'entryLinesForm.lastOrderEntryPage':'pricingEntryLine',
            'entryLinesForm.fromUpload':'false',
            'entryLinesForm.useHeaderRequestedDate':'true',
            'entryLinesForm.hasComments':'false',
            'entryLinesForm.isLastItemDeleted':'false',
            'entryLinesForm.entryLine[0].deleted':'false',
            'entryLinesForm.entryLine[0].validateRequestDate':'false',
            'entryLinesForm.entryLine[0].ULF.selectedID':'',
            'entryLinesForm.entryLine[0].selectedSupercededID':'',
            'entryLinesForm.entryLine[0].quantity':'1',
            'entryLinesForm.entryLine[0].partNumber':cat_num,
            'entryLinesForm.entryLine[1].deleted':'false',
            'entryLinesForm.entryLine[1].validateRequestDate':'false',
            'entryLinesForm.entryLine[1].ULF.selectedID':'',
            'entryLinesForm.entryLine[1].selectedSupercededID':'',
            'entryLinesForm.entryLine[1].quantity':'',
            'entryLinesForm.entryLine[1].partNumber':'',
            'entryLinesForm.addItemsToCartWithPAButton':'Check Pricing & Availability',
        })

        availability = {}

        # these are the 2 javascript requests that bring the availability data, one with the quantity and the other one without
        # it seems they interchange, so we need to parse both

        new_headers = [('X-Requested-With', 'XMLHttpRequest')]
        self.session.headers.update(new_headers)
        resp = self.session.post('https://www.ptplace.com/ptp/do/ajaxPRCart?dispatch=pricingrequest&navbartype=Store&selectedcountry=USA&viewstore=false&selectedstore=Gates&bflag=false&selectedlanguage=English',
                                    data={'longPoll':'false',
                                    'delay':'false',
                                    'getTimeEstimate':'true'})

        # print resp.text
        x = html.fromstring(resp.content)
        data = x.xpath('//locations//option')
        for row in data:
            try:
                partition = row.text_content().split(':')
                location = partition[0]
                avail = partition[1]
                availability[location] = avail
            except IndexError:
                 continue

        # we need a delay beteewn javascript requests
        sleep(5)
        resp = self.session.post('https://www.ptplace.com/ptp/do/ajaxPRCart?dispatch=pricingrequest&navbartype=Store&selectedcountry=USA&viewstore=false&selectedstore=Gates&bflag=false&selectedlanguage=English',
                                    data={'longPoll':'false',
                                    'delay':'false',
                                    'getTimeEstimate':'true'})

        # print resp.text
        x = html.fromstring(resp.content)
        data = x.xpath('//locations//option')
        for row in data:
            try:
                partition = row.text_content().split(':')
                location = partition[0]
                avail = partition[1]
                availability[location] = avail
            except IndexError:
                 continue

        for location in availability:
            try:
                availability[location] = int(availability[location])
            except Exception:
                availability[location] = 0
        return availability

 

if __name__ == '__main__':
    scraper = GatesScraper()
    # print scraper.get_availability('3L550')
    print scraper.get_tracking('S1169045')
