# -*- coding: utf-8 -*-

import requests
from lxml import html
from lxml.html.clean import Cleaner
from lxml import etree
from datetime import datetime, timedelta
import re

class UpsScraper(object):

    HEADERS = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.73 Safari/537.36',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset':'utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding':'gzip,deflate,sdch',
                'Accept-Language':'it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4',
                'Connection':'keep-alive',
                # 'Content-Type':'application/x-www-form-urlencoded',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                # 'X-Requested-With':'XMLHttpRequest',
                # 'Referer': 'https://wwwapps.ups.com/ctc/request?loc=en_US&WT.svl=PNRO_L1',
                # 'Origin': 'https://wwwapps.ups.com',
                # 'Host': 'wwwapps.ups.com'
                }

    def __init__(self, *args, **kwargs):
        self.session = requests.Session()
        self.session.headers = self.HEADERS


    def clean_results(self, price):
        try:
            return float(re.search('[\d\.,]+', price).group(0).replace(',', ''))
        except AttributeError:
            return 0


    def get_estimate(self, zipcode1, zipcode2, weight, date=datetime.now()):
        date = date.strftime('%Y-%m-%d')
        # th pickup date is formated diff
        date_pick = datetime.strptime(date, '%Y-%m-%d').strftime('%m/%d/%Y')
        resp = self.session.get('https://wwwapps.ups.com/ctc/request?loc=en_US&WT.svl=PNRO_L1')
        x = html.fromstring(resp.content)
        # submit the first form
        data={
                                'timeOnlyRts':'false',
                                'ctcModPkgType':'null',
                                'ivrPkgType':'null',
                                'ctcModAccountFlag':'show',
                                'ctcModLoginStatus':'null',
                                'ctcModuleWeight':'null',
                                'ctcModuleWeightType':'null',
                                'importFlag':'',
                                'assume':'',
                                'rtsFlag':'',
                                'destCtyCurrency':'',
                                'destCtyDimUnit':'',
                                'destCtyUom':'',
                                'destCtyUomKey':'',
                                'afcity':'null',
                                'afpostal':'null',
                                'afcountry':'null',
                                'prefCity':'null',
                                'prefPostal':'null',
                                'prefcountry':'null',
                                'addressCountry':'null',
                                'userId':'',
                                'A_Resi':'null',
                                'isResidential':'null',
                                'addressDiffFromBook':'NO',
                                'addressBookCompanyOrName':'',
                                'addresseName':'',
                                'addressLine1':'',
                                'addressLine2':'',
                                'addressLine3':'',
                                'addressCity':'null',
                                'addressZip':'null',
                                'resComDet':'null',
                                'addressBookState':'null',
                                'requestor':'',
                                'taxIndicator':'null',
                                'DeSurInd':'null',
                                'AccNum':'null',
                                'returnURL':'null',
                                'page':'shipping/wwdt/tim(1ent).html',
                                'loc':'en_US',
                                'lanCancelURL':'',
                                'packageLetter':'null',
                                'selectedAccountNumber':'',
                                'selectedAccountClassification':'null',
                                'isSelectedAccountABREnabled':'',
                                'isSelectedAccountGBPalletEnabled':'null',
                                'accImsFlag':'false',
                                'accType':'null',
                                'accSelectedCountry':'null',
                                'jsDisabled':'null',
                                'isAccountSelected':'null',
                                'modDestResidetail':'null',
                                'destRes':'null',
                                'modWeightUnit':'null',
                                'modDimUnit':'null',
                                'modContainer':'null',
                                'modWeight':'null',
                                'modLength':'null',
                                'modWidth':'null',
                                'modHeight':'null',
                                'modDeclValue':'null',
                                'modDropOfChoice':'null',
                                'modPickUpMethod':'null',
                                'modDailyPickUp':'null',
                                'modValueAdded':'null',
                                'modPickUpMethod1':'null',
                                'modPickupAdded':'null',
                                'modRequestor':'null',
                                'modCustomValue':'null',
                                'modSameValue':'null',
                                'isModifyClicked':'null',
                                'modOrigCity':'null',
                                'modOrigZip':'null',
                                'modOrigCountry':'null',
                                'modDestCity':'null',
                                'modDestZip':'null',
                                'modDestCountry':'null',
                                'selectpackaging':'null',
                                'mypacking':'My Packaging',
                                'upsletter':'UPS Letter',
                                'expressbox':'UPS Express Box',
                                'smallbox':'UPS Express Box - Small',
                                'mediumbox':'UPS Express Box - Medium',
                                'largebox':'UPS Express Box - Large',
                                'tube':'UPS Tube',
                                'pack':'UPS Pak',
                                'tenkg':'UPS Worldwide Express 10KG Box',
                                'twentyfivekg':'UPS Worldwide Express 25KG Box',
                                'palletPkgType':'Pallet',
                                'timeOnlyCountries':'AS,AD,AO,AI,AG,AM,AW,BD,BB,BY,BZ,BJ,BT,BW,VG,BN,BF,BI,KH,CM,CV,CF,TD,CG,CK,DJ,DM,GQ,ER,ET,FO,FJ,GF,PF,GA,GM,GE,GL,GD,GP,GU,GN,GW,GY,HT,IS,CI,JM,JO,KI,LA,LB,LS,LR,LI,MK,MG,MW,MV,ML,MH,MQ,MR,FM,MC,MN,MS,MZ,MP,ME,NA,NP,AN,NC,NE,NF,PW,PG,RE,RW,SM,SN,SC,SL,SB,LK,KN,LC,VC,SR,SZ,SY,TJ,TZ,TG,TO,TT,TN,TM,TC,TV,UG,UA,UZ,VU,WF,WS,YE,ZM,ZW',
                                'promoDiscountEligible':'',
                                'billableWeightIndicator':'',
                                'customerClassificationCode':'',
                                'abrEligible':'',
                                'useAcc':'null',
                                'modAccNumIn':'null',
                                'ctcModuleLogin':'null',
                                'quoteTypeQcc':'transitTimeOnly',
                                'origtype':'',
                                'datevalue':'undefined',
                                'noofpackages':'1',
                                'quoteselected':'transitTimeOnly',
                                'nextclicked':'next',
                                'fromaddORcountry':'',
                                'itsQuickquote':'no',
                                'onChangeAccValue':'',
                                'quickQuoteTypePackageLetter':'',
                                'transitTimeSelected':'',
                                'shipmentTypeFreight':'smallORPallet',
                                'origCurrency':'',
                                'usPR':'',
                                'dismissLink':'',
                                'metricUnit':'',
                                'containerSelected':'',
                                'fromCountryChange':'init',
                                'toCountryChange':'init',
                                'ratingQuoteTypeTime':'null',
                                'ratingQuoteTypeDetail':'null',
                                'ratingQuoteTypePackage':'null',
                                'ratingQuoteTypeLetter':'null',
                                'ratingHowWillRetail':'null',
                                'ratingHowWillDriver':'null',
                                'ratingHowWillDotCom':'null',
                                'ratingHowWillOneEight':'null',
                                'ratingDailyPick':'null',
                                'ratingPackType':'null',
                                'ratingDestTypeRes':'null',
                                'ratingOrigTypeRes':'',
                                'ratingDestTypeComm':'null',
                                'preferenceaddresskey':'000',
                                'palletselected':'0',
                                'refreshmod1':'',
                                'js_on':'true',
                                'shipDate': date,
                                'accountPrefpickup':'null',
                                'accountPrefgiveDriver':'null',
                                'palletEligable':'null',
                                'imsStatus':'null',
                                'ipaParameter':'',
                                'shipmenttype':'smallPkg',
                                'inTranslation':'inches',
                                'cmTranslation':'cm.',
                                'lbsTranslation':'lbs.',
                                'kgsTranslation':'kgs.',
                                'quoteType':'transitTimeOnly',
                                'pageRenderName':'',
                                'origCountry':'US',
                                'origCity':'',
                                'origPostal': zipcode1,
                                'origCityHist':'',
                                'origStateHist':'',
                                'origPostalHist': zipcode1,
                                'origLocale':'en_US',
                                'origLocale':'CTC',
                                'origPolDiv3':'',
                                'military':'false',
                                'shipmentType':'smallPkg',
                                'destCountry':'US',
                                'destCity':'',
                                'destPostal': zipcode2,
                                'destCityHist':'',
                                'destStateHist':'',
                                'destPostalHist': zipcode2,
                                'destLocale':'en_US',
                                'destLocale':'CTC',
                                'destPolDiv3':'',
                                'military':'false',
                                'pickerDate': date_pick,
                                'currencyScalar':'',
                                'currencyUnits':'USD',
                                'weight':'1',
                                'weightType':'LBS',
                                'packagesMod1':'1',
                                'recalculateAccessorials':'',
                                'length1':'',
                                'width1':'',
                                'height1':'',
                                'diUnit':'IN',
                                'weight1':'',
                                'shipWeightUnit':'LBS',
                                'packages':'1',
                                'sameValues':'YES',
                                'currency1':'',
                                'pickupMethod1':'1',
                                'accNumIn':'',
                                'pickupMethod':'1',
                                'WWEFMT':'',
                                'WWEFIT':'',
                                'ctc_submit':'10',

        }
        resp = self.session.post('https://wwwapps.ups.com/ctc/results', data=data, allow_redirects=True,
                                 headers={'X-Requested-With': 'XMLHttpRequest',})
        # handle the cases with multiple zips
        print resp.text
        if 'destJSON' in resp.text:
            first_city = resp.text.split('"value":"')[1].split('"')[0]
            print first_city
            data['dest_location'] = first_city
            data['page'] = 'shipping/wwdt/tnc(2err).html'
            resp = self.session.post('https://wwwapps.ups.com/ctc/results', data=data, allow_redirects=True,
                                     headers={'X-Requested-With': 'XMLHttpRequest',})
            print resp.text
        # the second form brings the complete information
        data={
            'timeOnlyRts':'false',
            'ctcModPkgType':'null',
            'ivrPkgType':'null',
            'ctcModAccountFlag':'show',
            'ctcModLoginStatus':'null',
            'ctcModuleWeight':'null',
            'ctcModuleWeightType':'null',
            'importFlag':'',
            'assume':'',
            'rtsFlag':'',
            'destCtyCurrency':'',
            'destCtyDimUnit':'',
            'destCtyUom':'',
            'destCtyUomKey':'',
            'afcity':'null',
            'afpostal':'null',
            'afcountry':'null',
            'prefCity':'null',
            'prefPostal':'null',
            'prefcountry':'null',
            'addressCountry':'null',
            'userId':'',
            'A_Resi':'null',
            'isResidential':'null',
            'addressDiffFromBook':'NO',
            'addressBookCompanyOrName':'',
            'addresseName':'',
            'addressLine1':'',
            'addressLine2':'',
            'addressLine3':'',
            'addressCity':'null',
            'addressZip':'null',
            'resComDet':'null',
            'addressBookState':'null',
            'requestor':'',
            'taxIndicator':'null',
            'DeSurInd':'null',
            'AccNum':'null',
            'returnURL':'null',
            'page':'shipping/wwdt/tim(1ent).html',
            'loc':'en_US',
            'lanCancelURL':'',
            'packageLetter':'null',
            'selectedAccountNumber':'',
            'selectedAccountClassification':'null',
            'isSelectedAccountABREnabled':'',
            'isSelectedAccountGBPalletEnabled':'null',
            'accImsFlag':'false',
            'accType':'null',
            'accSelectedCountry':'null',
            'jsDisabled':'null',
            'isAccountSelected':'null',
            'modDestResidetail':'null',
            'destRes':'null',
            'modWeightUnit':'null',
            'modDimUnit':'null',
            'modContainer':'null',
            'modWeight':'null',
            'modLength':'null',
            'modWidth':'null',
            'modHeight':'null',
            'modDeclValue':'null',
            'modDropOfChoice':'null',
            'modPickUpMethod':'null',
            'modDailyPickUp':'null',
            'modValueAdded':'null',
            'modPickUpMethod1':'null',
            'modPickupAdded':'null',
            'modRequestor':'null',
            'modCustomValue':'null',
            'modSameValue':'null',
            'isModifyClicked':'null',
            'modOrigCity':'null',
            'modOrigZip':'null',
            'modOrigCountry':'null',
            'modDestCity':'null',
            'modDestZip':'null',
            'modDestCountry':'null',
            'selectpackaging':'null',
            'mypacking':'My Packaging',
            'upsletter':'UPS Letter',
            'expressbox':'UPS Express Box',
            'smallbox':'UPS Express Box - Small',
            'mediumbox':'UPS Express Box - Medium',
            'largebox':'UPS Express Box - Large',
            'tube':'UPS Tube',
            'pack':'UPS Pak',
            'tenkg':'UPS Worldwide Express 10KG Box',
            'twentyfivekg':'UPS Worldwide Express 25KG Box',
            'palletPkgType':'Pallet',
            'timeOnlyCountries':'AS,AD,AO,AI,AG,AM,AW,BD,BB,BY,BZ,BJ,BT,BW,VG,BN,BF,BI,KH,CM,CV,CF,TD,CG,CK,DJ,DM,GQ,ER,ET,FO,FJ,GF,PF,GA,GM,GE,GL,GD,GP,GU,GN,GW,GY,HT,IS,CI,JM,JO,KI,LA,LB,LS,LR,LI,MK,MG,MW,MV,ML,MH,MQ,MR,FM,MC,MN,MS,MZ,MP,ME,NA,NP,AN,NC,NE,NF,PW,PG,RE,RW,SM,SN,SC,SL,SB,LK,KN,LC,VC,SR,SZ,SY,TJ,TZ,TG,TO,TT,TN,TM,TC,TV,UG,UA,UZ,VU,WF,WS,YE,ZM,ZW',
            'promoDiscountEligible':'',
            'billableWeightIndicator':'',
            'customerClassificationCode':'',
            'abrEligible':'',
            'useAcc':'null',
            'modAccNumIn':'null',
            'ctcModuleLogin':'null',
            'quoteTypeQcc':'estimateTimeCost.x',
            'origtype':'',
            'datevalue':'undefined',
            'noofpackages':'1',
            'quoteselected':'estimateTimeCost.x',
            'nextclicked':'next',
            'fromaddORcountry':'',
            'itsQuickquote':'no',
            'onChangeAccValue':'',
            'quickQuoteTypePackageLetter':'',
            'transitTimeSelected':'',
            'shipmentTypeFreight':'smallORPallet',
            'origCurrency':'USD',
            'usPR':'true',
            'dismissLink':'',
            'metricUnit':'IN',
            'containerSelected':'',
            'fromCountryChange':'false',
            'toCountryChange':'false',
            'ratingQuoteTypeTime':'null',
            'ratingQuoteTypeDetail':'null',
            'ratingQuoteTypePackage':'null',
            'ratingQuoteTypeLetter':'null',
            'ratingHowWillRetail':'null',
            'ratingHowWillDriver':'null',
            'ratingHowWillDotCom':'null',
            'ratingHowWillOneEight':'null',
            'ratingDailyPick':'null',
            'ratingPackType':'null',
            'ratingDestTypeRes':'null',
            'ratingOrigTypeRes':'',
            'ratingDestTypeComm':'null',
            'preferenceaddresskey':'000',
            'palletselected':'0',
            'refreshmod1':'',
            'js_on':'true',
            'shipDate':date,
            'accountPrefpickup':'null',
            'accountPrefgiveDriver':'null',
            'palletEligable':'null',
            'imsStatus':'null',
            'ipaParameter':'',
            'shipmenttype':'smallPkg',
            'inTranslation':'inches',
            'cmTranslation':'cm.',
            'lbsTranslation':'lbs.',
            'kgsTranslation':'kgs.',
            'quoteType':'estimateTimeCost.x',
            'pageRenderName':'summaryResults',
            'origCountry':'US',
            'origCity':'',
            'origPostal': zipcode1,
            'origCityHist':'',
            'origStateHist':'',
            'origPostalHist': zipcode1,
            'origLocale':'en_US',
            'origLocale':'CTC',
            'origPolDiv3':'',
            'military':'false',
            'shipmentType':'smallPkg',
            'destCountry':'US',
            'destCity':'',
            'destPostal': zipcode2,
            'destCityHist':'',
            'destStateHist':'',
            'destPostalHist': zipcode2,
            'destLocale':'en_US',
            'destLocale':'CTC',
            'destPolDiv3':'',
            'military':'false',
            'pickerDate': date_pick,
            'currencyScalar':'',
            'currencyUnits':'USD',
            'weight':'1',
            'weightType':'LBS',
            'packagesMod1':'1',
            'destPostal': zipcode2,
            'destCity':'',
            'origPostal': zipcode1,
            'origCity':'',
            'recalculateAccessorials':'',
            'container':'02',
            'length1':'',
            'width1':'',
            'height1':'',
            'diUnit':'IN',
            'weight1': weight,
            'shipWeightUnit':'LBS',
            'packages':'1',
            'sameValues':'YES',
            'currency1':'',
            'page':'accessorialModule',
            'origCurrency':'',
            'modValueAdded':'null',
            'currency':'null',
            'signRequiredALL':'DCR',
            'return_label':'ERL',
            'pickupMethod1':'1',
            'page':'accessorialModule',
            'origCurrency':'',
            'modValueAdded':'null',
            'currency':'null',
            'signRequiredALL':'DCR',
            'return_label':'ERL',
            'WWEFMT':'',
            'WWEFIT':'',
            'container':'02',
            'length1':'',
            'width1':'',
            'height1':'',
            'diUnit':'IN',
            'weight1': weight,
            'shipWeightUnit':'LBS',
            'packages':'1',
            'sameValues':'YES',
            'currency1':'',
            'page':'accessorialModule',
            'origCurrency':'',
            'modValueAdded':'null',
            'currency':'null',
            'signRequiredALL':'DCR',
            'return_label':'ERL',
            'pickupMethod1':'1',
            'ctc_second_submit':'10',
                          }
        try:
            data['dest_location'] = first_city
        except Exception as e:
            pass
        resp = self.session.post('https://wwwapps.ups.com/ctc/results', data=data,
                                 allow_redirects=True,
                                 headers={'X-Requested-With': 'XMLHttpRequest',
                                        'Referer': 'https://wwwapps.ups.com/ctc/request?loc=en_US&WT.svl=PNRO_L1',
                                        'Origin': 'https://wwwapps.ups.com',
                                        'Host': 'wwwapps.ups.com',
                                        })

        # print resp.text
        # raw_input()

        results = ''
        x = html.fromstring(resp.content)
        # x = etree.fromstring(resp.content)
        try:
            title = x.xpath(".//div[contains(@class,'secLvl step tableonly clearfix')]//h3")[0].text_content().strip().replace('\n', '').replace('\t', '')
            title = '<h5 style="margin:0 0 5px 0;">' + re.sub(r'[ ]{2,}', ' ', title) + '</h5>'
            print title
            table1 = x.xpath(".//table[@class='dataTable noTableHeader full']")[0]
        except IndexError:
            return ''
        garbage = table1.xpath(".//tr[not (contains(@id,'servicerow'))]")
        for bad in garbage:
            bad.drop_tree()
        garbage = table1.xpath(".//dd/input | .//dt/input")
        for bad in garbage:
            bad.drop_tree()

        # results = html.tostring(table1)
        results1 = html.tostring(table1)
        # results1 = html.clean.clean_html(results)

        return title + results1


    def get_freight_estimate(self, zipcode1, zipcode2, weight, date=datetime.now()):
        date = date.strftime('%m%d%Y')
        # th pickup date is formated diff
        #date_pick = datetime.strptime(date, '%Y-%m-%d').strftime('%m/%d/%Y')
        resp = self.session.get('https://wwwapps.ups.com/fctc/timeandcost?loc=en_US&ActionOriginPair=SeamlessExperience___StartSession&FREIGHT_TYPE=LTL')
        x = html.fromstring(resp.content)
        # submit the first form
        resp = self.session.post('https://wwwapps.ups.com/fctc/processfctcentry?loc=en_US',
                                 data={ 'changeShipFrom':'false',
                                        'changeShipTo':'false',
                                        'redirectToCTC':'false',
                                        'dismissPreferenceLink':'false',
                                        'selectedRatingType':'LTL',
                                        'loc':'en_US',
                                        'original_loc':'en_US',
                                        'accountNumber':'',
                                        'shipFromResidential':'',
                                        'shipToResidential':'',
                                        'freightRatingType':'Air',
                                        'shipFromCountry':'US',
                                        'isShipFromPostalRequired':'true',
                                        'shipFromCity':'',
                                        'shipFromState':'',
                                        'shipFromZip':zipcode1,
                                        'shipToCountry':'US',
                                        'isShipToPostalRequired':'true',
                                        'shipToCity':'',
                                        'shipToState':'',
                                        'shipToZip': zipcode2,
                                        'shipmentDate':date,
                                        'submit_button_next':'Next',
                                      })
        x = html.fromstring(resp.content)
        city1 = x.xpath(".//input[@id='from_city']/@value")
        city2 = x.xpath(".//input[@id='to_city']/@value")
        state1 = x.xpath(".//select[@name='shipFromState']/option[@selected='selected']/@value")
        state2 = x.xpath(".//select[@name='shipToState']/option[@selected='selected']/@value")
        print city1, state1
        print city2, state2
        # second form introducing dimensions and weight
        resp = self.session.post('https://wwwapps.ups.com/fctc/processTimeAndCost?loc=en_US',
                                 data={ 'changeShipFrom':'false',
                                        'changeShipTo':'false',
                                        'backButton':'',
                                        'loc':'en_US',
                                        'original_loc':'en_US',
                                        'shipFromCountry':'US',
                                        'isShipFromPostalRequired':'true',
                                        'shipFromCity': city1,
                                        'shipFromState': state1,
                                        'shipFromZip':zipcode1,
                                        'shipToCountry':'US',
                                        'isShipToPostalRequired':'true',
                                        'shipToCity': city2,
                                        'shipToState': state2,
                                        'shipToZip': zipcode2,
                                        'shipmentDate':date,
                                        'unitOfMeasure':'english',
                                        'numbers1':'1',
                                        'types1':'18',
                                        'lengths1':'39.37',
                                        'widths1':'39.37',
                                        'heights1':'39.37',
                                        'weights1': weight,
                                        'numbers2':'',
                                        'types2':'18',
                                        'lengths2':'',
                                        'widths2':'',
                                        'heights2':'',
                                        'weights2':'',
                                        'numbers3':'',
                                        'types3':'18',
                                        'lengths3':'',
                                        'widths3':'',
                                        'heights3':'',
                                        'weights3':'',
                                        'numbers4':'',
                                        'types4':'18',
                                        'lengths4':'',
                                        'widths4':'',
                                        'heights4':'',
                                        'weights4':'',
                                        'numbers5':'',
                                        'types5':'18',
                                        'lengths5':'',
                                        'widths5':'',
                                        'heights5':'',
                                        'weights5':'',
                                        'declaredValue':'',
                                        'currencyCode':'USD',
                                        'submit_button_next':'Next',
                                      })
        x = html.fromstring(resp.content)
        price = x.xpath(".//a[contains(text(),'UPS Next Day Air')]/following::td[1]/text()")[0].strip()
        return self.clean_results(price)



    def get_ups_ground(self, zipcode1, zipcode2, weight, date):
        results = self.get_estimate(zipcode1, zipcode2, weight, date)
        x = html.fromstring(results)
        price = x.xpath(".//span[contains(@class,'label')]/a[contains(text(),'UPS Ground')]/following::td[2]//strong[1]/text()")[0].strip()
        return self.clean_results(price)


if __name__ == '__main__':
    scraper = UpsScraper()
    # print scraper.get_availability('AEM2238-4')
    #print scraper.get_estimate(99515, 99520, 2)
    print scraper.get_freight_estimate(10280, 90023, 200)
