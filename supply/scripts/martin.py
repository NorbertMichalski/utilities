# -*- coding: utf-8 -*-

import requests
from lxml import html
from datetime import datetime


class MartinScraper(object):

    USERNAME = 'mark1983'
    PASSWORD = 'msais1234'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.73 Safari/537.36',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding':'gzip,deflate,sdch',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Referer': 'https://btweb.martinsprocket.com/PartsLookup/CheckLogin.aspx',
                'Origin': 'https://btweb.martinsprocket.com',
                'Host': 'btweb.martinsprocket.com'
                }

    def __init__(self, *args, **kwargs):
        self.session = requests.Session()
        self.session.headers = self.HEADERS
        self.logged_in = False

    def login(self):
        resp = self.session.get('https://btweb.martinsprocket.com/PartsLookup/CheckLogin.aspx')
        # grab some hidden inputs values for the next form
        x = html.fromstring(resp.content)
        event_target = x.xpath(".//input[@name='__EVENTTARGET']/@value")[0]
        event_argument = x.xpath(".//input[@name='__EVENTARGUMENT']/@value")[0]
        view_state = x.xpath(".//input[@name='__VIEWSTATE']/@value")[0]
        event_validation = x.xpath(".//input[@name='__EVENTVALIDATION']/@value")[0]

        resp = self.session.post('https://btweb.martinsprocket.com/PartsLookup/CheckLogin.aspx', data={
                                'txtEmail': self.USERNAME,
                                'txtPassword': self.PASSWORD,
                                'butLogin': 'Login',
                                '__EVENTTARGET': event_target,
                                '__EVENTARGUMENT': event_argument,
                                '__VIEWSTATE': view_state,
                                '__EVENTVALIDATION': event_validation,
                            })
        x = html.fromstring(resp.content)
        try:
            check_login = x.xpath(".//span[contains(text(),'MECHANICAL DRIVES & BELTING')]")[0]
            self.logged_in = True
            return True
        except IndexError:
            self.logged_in = False
            return False

    def get_availability(self, cat_num):
        if not self.logged_in and not self.login():
            return
        if '-' in cat_num:
            cat_num = cat_num.replace('-', ' ')
        availability = {}
        new_headers = [ ('Referer', 'https://btweb.martinsprocket.com/PartsLookup/Default.aspx')]
        self.session.headers.update(new_headers)
        resp = self.session.get('https://btweb.martinsprocket.com/PartsLookup/Default.aspx')
        # grab some hidden inputs values for the next form
        x = html.fromstring(resp.content)
        event_target = x.xpath(".//input[@name='__EVENTTARGET']/@value")
        event_argument = x.xpath(".//input[@name='__EVENTARGUMENT']/@value")
        view_state = x.xpath(".//input[@name='__VIEWSTATE']/@value")
        event_validation = x.xpath(".//input[@name='__EVENTVALIDATION']/@value")
        resp = self.session.post('https://btweb.martinsprocket.com/PartsLookup/Default.aspx', data={
                                'txtPartNumber1':cat_num,
                                'txtQuantity1':'1',
                                'txtPartNumber2':'',
                                'txtQuantity2':'1',
                                'txtPartNumber3':'',
                                'txtQuantity3':'1',
                                'txtPartNumber4':'',
                                'txtQuantity4':'1',
                                'txtPartNumber5':'',
                                'txtQuantity5':'1',
                                'butLookup':'Lookup',
                                '__EVENTTARGET': event_target,
                                '__EVENTARGUMENT': event_argument,
                                '__VIEWSTATE': view_state,
                                '__EVENTVALIDATION': event_validation,
                                })
        x = html.fromstring(resp.content)
        rows = True
        i = 1
        while (rows):
            try:
                location = x.xpath("//span[@id='txtLocation%sa']/text()" % i)[0].strip()
                avail = x.xpath("//span[@id='txtQty%sa']/text()" % i)[0].strip()
                availability[location] = avail
                i += 1
            except IndexError:
                rows = False
        for location in availability:
            try:
                availability[location] = int(availability[location])
            except Exception:
                availability[location] = 0
        return availability

    def get_tracking(self, order_num):
        if not self.logged_in and not self.login():
            return
        results = []
        #  go to the order's status page
        new_headers = [ ('Referer', 'http://btweb.martinsprocket.com/customermenu/default.aspx')]
        self.session.headers.update(new_headers)
        resp = self.session.get('http://btweb.martinsprocket.com/customermenu/Login.aspx?AppCode=OrderStatus', allow_redirects=True)
        # grab some hidden inputs values for the next form
        x = html.fromstring(resp.content)
        view_state = x.xpath(".//input[@name='__VIEWSTATE']/@value")
        event_validation = x.xpath(".//input[@name='__EVENTVALIDATION']/@value")

        resp = self.session.post('https://btweb.martinsprocket.com/OrderStatus/Default.aspx', data={
                                '__VIEWSTATE': view_state,
                                '__EVENTVALIDATION': event_validation,
                                'txtPONum': order_num,
                                'butPO':'Go',
                                'txtPONum2':'',
                                'txtPartNum':'',
                                })
        x = html.fromstring(resp.content)
        products = [i.strip() for i in x.xpath(".//a[contains(@href,'OrderStatusDetail.aspx?')]/text()")]
        links = x.xpath(".//a[contains(@href,'OrderStatusDetail.aspx?')]/@href")
        for product, link in zip(products, links):
            resp = self.session.get('https://btweb.martinsprocket.com/OrderStatus/%s' % link)
            x = html.fromstring(resp.content)
            try:
                tracking_number = x.xpath(".//td[contains(@title, 'Click on tracking number to link to the carrier site')]/p/a/text()")[0].strip()
                carrier = x.xpath(".//td[contains(@title, 'Click on tracking number to link to the carrier site')]/preceding-sibling::td[1]/p/text()")[0].strip()
                print carrier
                ship_date = x.xpath(".//td[2]/p/text()")[0].strip()
                ship_date = datetime.strptime(ship_date, '%m/%d/%Y')
                result_dictionary = {'item_id':'', 'status':'', 'tracking_number':'', 'ship_date':ship_date}
                result_dictionary['item_id'] = product
                result_dictionary['tracking_number'] = tracking_number
                result_dictionary['status'] = 'shipped'
                result_dictionary['shipping_method'] = carrier
                results.append(result_dictionary)
            except IndexError:
                continue

        return results

if __name__ == '__main__':
    scraper = MartinScraper()
    print scraper.get_availability('6H')
    print scraper.get_tracking('S1170853')
