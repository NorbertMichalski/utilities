# -*- coding: utf-8 -*-

import requests
from lxml import html

class LeesonScraper(object):

    USERNAME = 'sales@mechdrives.com'
    PASSWORD = 'larco1898'
    TOKEN = ''
    HEADERS = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.73 Safari/537.36',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset':'utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding':'gzip,deflate,sdch',
                'Accept-Language':'it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4',
                'Connection':'keep-alive',
                'Content-Type':'application/x-www-form-urlencoded',
                }

    HOST = 'https://leebiz-apps.leeson.com/OA_HTML'

    def __init__(self, *args, **kwargs):
        self.session = requests.Session()
        self.session.headers = self.HEADERS
        self.logged_in = False

    def login(self):
        resp = self.session.get('https://leebiz-login.leeson.com/login/login')
        self.TOKEN = resp.url.split('site2pstoretoken=')[1].split('&')[0].strip()
        self.session.post('https://leebiz-login.leeson.com/sso/auth', data={
            'site2pstoretoken': self.TOKEN,
            'ssousername': self.USERNAME,
            'password': self.PASSWORD,

        }, allow_redirects=True)
        self.logged_in = True

    def get_availability(self, cat_num):
        if not self.logged_in:
            self.login()

        # open the availability page
        resp = self.session.get(self.HOST + '/ibeCAcpSSOLogin.jsp?ref=le_biz_ibeCScdCheckAvailAjax.jsp%3Fa=b%26minisite%3D10082')

        # simulate javascript add to cart and grab some validation code to pass over to the next request
        resp = self.session.get(self.HOST + '/rbc_default_ajaxAddCartItem.jsp?pnum=%s&active=N&qty=1&xsell=0&cartId=&sid=' % cat_num)
        send_text = resp.text
        if 'Part number does not exist' in send_text:
            return {}

        # another javascript request that returns the actual database id of the product searched
        resp = self.session.get(self.HOST + '/le_biz_ajaxDisplayDirectEntryCart.jsp?parentWindow=DIECART&sid=&wh1=&itm=&lid=&searchitem=%s' % send_text)
        x = html.fromstring(resp.content)
        # grabbing the cartId for later use
        cartId = x.xpath('//a[contains(text(),"Delete all")]/@href')[0].split("'")[1]
        # grab the database ids from the parameters of a javascript function attached to a span
        try:
            avail_link = x.xpath('//span[contains(@onclick, "javascript:goThr")]/@onclick')[0]
            itemId = avail_link.split("'")[1]
            rowId = avail_link.split("'")[5]
        except IndexError:
            # sometimes for some products there is no availability link present
            return {}

        # the final request that actually brings the availability table
        resp = self.session.get(self.HOST + '/le_biz_gbDisplayAllInventory.jsp?itemId=%s&custno=&rowid=%s&defwh=948&qty=1' % (itemId, rowId))

        x = html.fromstring(resp.content)
        availability = {}
        # using these to clean the results
        separators = ['- LEESON', 'LEESON', 'DIST']

        for row in x.xpath("//table[contains(@class,'resultSet')]//tr"):
            try:
                location = row.xpath("./td/a/text()")[0]
                # cut the jibber jabber from locations
                for separator in separators:
                    if separator in location:
                        location = location.split(separator)[0].strip()
                        break
                avail = row.xpath("./td[a]/following-sibling::td/text()")[0].strip()
                availability[location] = avail
            except IndexError:
                continue

        # empty the cart list
        self.session.get(self.HOST + '/rbc_default_ajaxDeleteCartItem.jsp?cartId=%s&lineId=&sid=' % cartId)

        for location in availability:
            try:
                availability[location] = int(availability[location])
            except Exception:
                availability[location] = 0
        return availability


    def get_tracking(self, order_num):
        if not self.logged_in:
            self.login()
        results = {}
        # open the tracking page
        resp = self.session.get('https://leebiz.leeson.com/portal/page/portal/Leeson/LEebiz/TrackOrders')
        x = html.fromstring(resp.content)
        # the name of the inputs from this form have some kind of random code attached in front
        # we have to grab the code and customer ID
        all_inputs = x.forms[1].fields
        for field in all_inputs:
            if '.custAccountId' in field:
                code = field.split('.')[0]
                customer_ID = all_inputs[field]
                break
        resp = self.session.post('https://leebiz.leeson.com/portal/page/portal/Leeson/LEebiz/TrackOrders', data={
                                code + '.strutsAction':'searchtrackorders.do',
                                code + '.custAccountId': customer_ID,
                                code + '.customerName':'Mechanical Drives & Belting (Los Angeles)',
                                code + '.siteId':'',
                                code + '.brand':'LE',
                                code + '.searchType':'',
                                code + '.operationType':'',
                                code + '.invoke':'viewQuickSearchResults',
                                code + '.advancedSearchFlag':'',
                                code + '.trackFilterType':'',
                                code + '.orderSearchFilterType':'basicordernumbersearch',
                                code + '.openOrders':'',
                                code + '.poNumberType':'',
                                code + '.orderNumber':'',
                                code + '.poNumber':order_num,
                                code + '.modelNumber':'',
                                code + '.customerPartNumber':'',
                                code + '.quickOrderSearchType':'NUMBER_SEARCH',
                                code + '.optQuickOrderSearchType':'NUMBER_SEARCH',
                                code + '.searchOrderNumberType':'PO_NUMBER',
                                'searchVal':order_num,
                                code + '.trackOrderDays':'',
                                    })
        # the results page
        x = html.fromstring(resp.content)
        rows = x.xpath(".//table[contains(@style,'table-layout:fixed; width:960px;') and contains(@class,'resultSet')]//tr")
        for row in rows:
            try:
                part_number = row.xpath('.//td[2]/text()')[0].strip()
                # sometimes we have a link sometimes no...
                tracking_number = row.xpath('.//td[7]/a/text() | .//td[7]/text()')[-1].strip()
                results[part_number] = tracking_number
                # this is the short version modification
                return tracking_number
            except IndexError:
                continue
        # this is the short version modification
        else:
            return 'NOT FOUND'
        return results


if __name__ == '__main__':
    scraper = LeesonScraper()
    # print scraper.get_availability('110088.00')
    print scraper.get_tracking('S1169601')
