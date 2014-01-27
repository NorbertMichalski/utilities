# -*- coding: utf-8 -*-

import requests
from lxml import html
from lxml.html.clean import Cleaner
from lxml import etree
from datetime import datetime, timedelta
import re

class IdcScraper(object):

    USERNAME = 'RMONIMA@MECHDRIVES.COM'
    PASSWORD = 'larco2915'
    HEADERS = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.73 Safari/537.36',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset':'utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding':'gzip,deflate,sdch',
                'Accept-Language':'it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4',
                'Connection':'keep-alive',
                # 'Content-Type':'application/x-www-form-urlencoded',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                # 'X-Requested-With':'XMLHttpRequest',
                # 'Host':'www.efstms.com',
                # 'Origin':'http://www.efstms.com',
                # 'Referer':'http://www.efstms.com/IDCUSA/Look_IDCUSA/Main/frmIDCUSAMain.aspx',
                }

    def __init__(self, *args, **kwargs):
        self.session = requests.Session()
        self.session.headers = self.HEADERS
        self.logged_in = False

    def clean_results(self, price):
        try:
            return float(re.search('[\d\.,]+', price).group(0).replace(',', ''))
        except AttributeError:
            return 0


    def login(self):
        resp = self.session.get('http://www.efstms.com/IDCUSA/Look_IDCUSA/Main/frmIDCUSAMain.aspx')
        x = html.fromstring(resp.content)
        event_target = x.xpath(".//input[@name='__EVENTTARGET']/@value")[0]
        event_argument = x.xpath(".//input[@name='__EVENTARGUMENT']/@value")[0]
        view_state = x.xpath(".//input[@name='__VIEWSTATE']/@value")[0]
        # event_validation = x.xpath(".//input[@name='__EVENTVALIDATION']/@value")[0]
        resp = self.session.post('http://www.efstms.com/IDCUSA/Look_IDCUSA/Main/frmIDCUSAMain.aspx', data={
            '__EVENTTARGET': event_target,
            '__EVENTARGUMENT': event_argument,
            '__VIEWSTATE': view_state,
            'ctl00$objMenu$txt_sQuickOriginZipCode$txt':'',
            'ctl00$objMenu$txt_sQuickDestinationZipCode$txt':'',
            'ctl00$objMenu$ShipmentType':'rbl_DomesticLTL',
            'ctl00$objMenu$txt_sTrackingNo$txt':'',
            'ctl00$objMenu$txt_sZusLogin$txt': self.USERNAME,
            'ctl00$objMenu$txt_sZusPassword$txt': self.PASSWORD,
            'ctl00$objMenu$cmdLogin':'Login',
            'hid_nPopupLevel':'0',
            'hid_nMasterID':'0',
            'hid_nFkMasterID':'0',
            'hid_sFkMasterColumn':'',
            'hid_bLockMasterField':'False',
            'hid_bShowNewButton':'True',
            'hid_bExpectReturnData':'False',
            'hid_bEditMode':'False',
            'hid_bShowDeleteButton':'True',
        })
        x = html.fromstring(resp.content)
        try:
            check_login = x.xpath(".//h1[contains(text(),'Roger Monima')]")[0]
            print 'logged in'
            self.logged_in = True
            return True
        except IndexError:
            print 'error'
            self.logged_in = False
            return False


    def get_estimate(self, zipcode1, zipcode2, weight, date=datetime.now()):
        if not self.logged_in:
            self.login()
        week = timedelta(days=5)
        next_week = (date + week).strftime('%m/%d/%Y')
        date = date.strftime('%m/%d/%Y')

        resp = self.session.get('http://www.efstms.com/IDCUSA/Look_IDCUSA/Main/frmIDCUSAMain.aspx')
        # grab some hidden inputs values for the next form
        x = html.fromstring(resp.content)
        event_target = x.xpath(".//input[@name='__EVENTTARGET']/@value")[0]
        event_argument = x.xpath(".//input[@name='__EVENTARGUMENT']/@value")[0]
        view_state = x.xpath(".//input[@name='__VIEWSTATE']/@value")[0]

        # submit the first form
        resp = self.session.post('http://www.efstms.com/IDCUSA/Look_IDCUSA/Main/frmIDCUSAMain.aspx', data={
                                '__EVENTTARGET': 'ctl00$objMenu$cmdQuickQuote',
                                '__EVENTARGUMENT': '',
                                '__VIEWSTATE': view_state,
                                'ctl00$objMenu$txt_sQuickOriginZipCode$txt':zipcode1,
                                'ctl00$objMenu$txt_sQuickDestinationZipCode$txt': zipcode2,
                                'ctl00$objMenu$ShipmentType':'rbl_DomesticLTL',
                                'ctl00$objMenu$txt_sTrackingNo$txt':'',
                                'hid_nPopupLevel':'0',
                                'hid_nMasterID':'0',
                                'hid_nFkMasterID':'0',
                                'hid_sFkMasterColumn':'',
                                'hid_bLockMasterField':'False',
                                'hid_bShowNewButton':'True',
                                'hid_bExpectReturnData':'False',
                                'hid_bEditMode':'False',
                                'hid_bShowDeleteButton':'True',

        }, allow_redirects=True, headers={ 'Host':'www.efstms.com',
                                            'Origin':'http://www.efstms.com',
                                            'Referer':'http://www.efstms.com/IDCUSA/Look_IDCUSA/Main/frmIDCUSAMain.aspx',
                                           })

        # grab some hidden inputs values for the next form
        x = html.fromstring(resp.content)
        event_target = x.xpath(".//input[@name='__EVENTTARGET']/@value")[0]
        event_argument = x.xpath(".//input[@name='__EVENTARGUMENT']/@value")[0]
        view_state = x.xpath(".//input[@name='__VIEWSTATE']/@value")[0]

        # the second form brings the complete information
        resp = self.session.post('http://www.efstms.com/IDCUSA/App_Efreightsolutions/OrderProcess/frmStep2.aspx', data={
                                '__VIEWSTATE': view_state,
                                '__EVENTTARGET':'',
                                '__EVENTARGUMENT':'',
                                'ctl00$objMasterPageContent$txt_sQuickOriginZipCode$txt': zipcode1,
                                'ctl00$objMasterPageContent$txt_sQuickDestinationZipCode$txt': zipcode2,
                                'ctl00$objMasterPageContent$cboSKUs':'1624',
                                'ctl00$objMasterPageContent$txt_sOrrDescription$txt':'motor',
                                'ctl00$objMasterPageContent$txt_nNoOfItems$txt':'1',
                                'ctl00$objMasterPageContent$txt_LineItemHandlingUnits$txt':'1',
                                'ctl00$objMasterPageContent$cmbPackaging$cbo':'120',
                                'ctl00$objMasterPageContent$txt_nOrrWeight$txt': weight,
                                'ctl00$objMasterPageContent$cbo_nWeuIDShort':'10',
                                'ctl00$objMasterPageContent$cbo_sOrrRateClass$cbo':'50',
                                'ctl00$objMasterPageContent$cbo_nLeuIDShort':'10',
                                'ctl00$objMasterPageContent$txt_nOrrLength$txt':'',
                                'ctl00$objMasterPageContent$txt_nOrrWidth$txt':'',
                                'ctl00$objMasterPageContent$txt_nOrrHeight$txt':'',
                                'ctl00$objMasterPageContent$txt_sOrrNMFC$txt':'',
                                'ctl00$objMasterPageContent$txt_sOrrMarks$txt':'',
                                'ctl00$objMasterPageContent$CollapsiblePanelExtender1_ClientState':'true',
                                'ctl00$objMasterPageContent$cbo_nWeuIDEst':'10',
                                'ctl00$objMasterPageContent$cbo_nLeuIDEst':'10',
                                'ctl00$objMasterPageContent$txt_nEstWeight$txt':'',
                                'ctl00$objMasterPageContent$txt_nEstLength$txt':'',
                                'ctl00$objMasterPageContent$txt_nEstWidth$txt':'',
                                'ctl00$objMasterPageContent$txt_nEstHeight$txt':'',
                                'ctl00$objMasterPageContent$txt_sEstimatedClass$txt':'',
                                'ctl00$objMasterPageContent$cmdAdd':'Add Line Item',
                                'ctl00$objMasterPageContent$hid_nRowNo':'',
                                'ctl00$objMasterPageContent$hid_sOrrSKU':'',
                                'ctl00$objMasterPageContent$hid_nZorBitvalue':'4608',
                                'ctl00$objMenu$txt_sQuickOriginZipCode$txt': zipcode1,
                                'ctl00$objMenu$txt_sQuickDestinationZipCode$txt': zipcode2,
                                'ctl00$objMenu$ShipmentType':'rbl_DomesticLTL',
                                'ctl00$objMenu$txt_sTrackingNo$txt':'',
                                'hid_nPopupLevel':'0',
                                'hid_nMasterID':'0',
                                'hid_nFkMasterID':'0',
                                'hid_sFkMasterColumn':'',
                                'hid_bLockMasterField':'False',
                                'hid_bShowNewButton':'True',
                                'hid_bExpectReturnData':'False',
                                'hid_bEditMode':'False',
                                'hid_bShowDeleteButton':'True',
                                  }, allow_redirects=True,  # headers={'Referer': post_url,
                                                            #        'Origin': 'http://idcusa.trinnos.com',
                                                             #       'Host': 'idcusa.trinnos.com'}
                                 )


        resp = self.session.post('http://www.efstms.com/IDCUSA/App_Efreightsolutions/OrderProcess/frmStep2.aspx', data={
                                        '__VIEWSTATE': view_state,
                                        '__EVENTTARGET':'',
                                        '__EVENTARGUMENT':'',
                                        'ctl00$objMasterPageContent$txt_sQuickOriginZipCode$txt': zipcode1,
                                        'ctl00$objMasterPageContent$txt_sQuickDestinationZipCode$txt': zipcode2,
                                        'ctl00$objMasterPageContent$cboSKUs':'1624',
                                        'ctl00$objMasterPageContent$txt_sOrrDescription$txt':'',
                                        'ctl00$objMasterPageContent$txt_nNoOfItems$txt':'1',
                                        'ctl00$objMasterPageContent$txt_LineItemHandlingUnits$txt':'',
                                        'ctl00$objMasterPageContent$cmbPackaging$cbo':'0',
                                        'ctl00$objMasterPageContent$txt_nOrrWeight$txt': weight,
                                        'ctl00$objMasterPageContent$cbo_nWeuIDShort':'10',
                                        'ctl00$objMasterPageContent$cbo_sOrrRateClass$cbo':'50',
                                        'ctl00$objMasterPageContent$cbo_nLeuIDShort':'10',
                                        'ctl00$objMasterPageContent$txt_nOrrLength$txt':'',
                                        'ctl00$objMasterPageContent$txt_nOrrWidth$txt':'',
                                        'ctl00$objMasterPageContent$txt_nOrrHeight$txt':'',
                                        'ctl00$objMasterPageContent$txt_sOrrNMFC$txt':'',
                                        'ctl00$objMasterPageContent$txt_sOrrMarks$txt':'',
                                        'ctl00$objMasterPageContent$CollapsiblePanelExtender1_ClientState':'true',
                                        'ctl00$objMasterPageContent$cbo_nWeuIDEst':'10',
                                        'ctl00$objMasterPageContent$cbo_nLeuIDEst':'10',
                                        'ctl00$objMasterPageContent$txt_nEstWeight$txt':'',
                                        'ctl00$objMasterPageContent$txt_nEstLength$txt':'',
                                        'ctl00$objMasterPageContent$txt_nEstWidth$txt':'',
                                        'ctl00$objMasterPageContent$txt_nEstHeight$txt':'',
                                        'ctl00$objMasterPageContent$txt_sEstimatedClass$txt':'',
                                        'ctl00$objMasterPageContent$cmdNext':'Next >>',
                                        'ctl00$objMasterPageContent$hid_nRowNo':'',
                                        'ctl00$objMasterPageContent$hid_sOrrSKU':'',
                                        'ctl00$objMasterPageContent$hid_nZorBitvalue':'4608',
                                        'ctl00$objMenu$txt_sQuickOriginZipCode$txt': zipcode1,
                                        'ctl00$objMenu$txt_sQuickDestinationZipCode$txt': zipcode2,
                                        'ctl00$objMenu$ShipmentType':'rbl_DomesticLTL',
                                        'ctl00$objMenu$txt_sTrackingNo$txt':'',
                                        'hid_nPopupLevel':'0',
                                        'hid_nMasterID':'0',
                                        'hid_nFkMasterID':'0',
                                        'hid_sFkMasterColumn':'',
                                        'hid_bLockMasterField':'False',
                                        'hid_bShowNewButton':'True',
                                        'hid_bExpectReturnData':'False',
                                        'hid_bEditMode':'False',
                                        'hid_bShowDeleteButton':'True',
                                        })


        results = ''
        x = html.fromstring(resp.content)
        # x = etree.fromstring(resp.content)
        try:
            table1 = x.xpath(".//table[@id='objMasterPageContent_gvCarrierServiceLevel']")[0]
        except IndexError:
            return ''
        garbage = table1.xpath(".//td[.//input]")
        for bad in garbage:
            bad.drop_tree()

        garbage = table1.xpath(".//th[not(span)]")
        for bad in garbage:
            bad.drop_tree()

        results = html.tostring(table1)
        # results1 = html.tostring(table1)
        results1 = html.clean.clean_html(results)

        return results1


    def get_freight(self, zipcode1, zipcode2, weight, date):
        results = self.get_estimate(zipcode1, zipcode2, weight, date)
        x = html.fromstring(results)
        price = x.xpath(".//span[contains(@id,'objMasterPageContent_gvCarrierServiceLevel_lblTotalPrice')]/text()")[-1].strip()
        return self.clean_results(price)

if __name__ == '__main__':
    scraper = IdcScraper()
    # print scraper.get_availability('AEM2238-4')
    print scraper.get_estimate(91406, 90023, 500)
