import sys, logging
import mechanize
import urllib
import cookielib
import re
from bs4 import BeautifulSoup

login = {
        'UserName': 'MMENASHE_MDB',
        'Password': 'green444',
       }


headers = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4'),
            ('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8'),
            ('Accept', '*/*'),
            ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'),
            # ('Accept-Encoding','gzip,deflate,sdch'),
            ('Accept-Language', 'en-US,en;q=0.8'),
            ('Connection', 'keep-alive'),

           ]

logging.basicConfig(filename='baldorVip_error.log',
                    format=('%(asctime)s -- line:%(lineno)3d'
                    ' -- %(levelname)s -- \n\t %(message)s'),
                    filemode='a', level=logging.DEBUG)


def setHeaders(browser, headers):
    for header in headers:
        browser.addheaders.append(header)
    # print br.addheaders


def loginBaldorVip(br, login):
    response = br.open('https://www.baldorvip.com')
    br.select_form(nr=1)
    br.form.find_control('ReturnUrl').readonly = False
    br.form['ReturnUrl'] = ''
    br.form['UserName'] = login['UserName']
    br.form['Password'] = login['Password']
    br.form.new_control('hidden', 'X-Requested-With', {'value':'XMLHttpRequest'})
    br.form.fixup()
    br.addheaders.append(('X-Requested-With', 'XMLHttpRequest'))
    response = br.submit()

# there is a javascript redirect after some requests, we have to emulate it in python
def jsRedirect(br):
    response = br.open('https://www.baldorvip.com')


def getOrderStatus(br, codes):
    trackingNumbers = []
    if codes == []:
        return 'You didn\'t paste any content.'
    for code in codes :
        if code == '':
            continue
        logging.debug(code)
        response = br.open('https://www.baldorvip.com/OrderStatus')
        br.select_form(nr=5)
        br.form['PurchaseOrderNumber'] = code
        response = br.submit()
        try:
            redirect = str(response.read()).split("'")[1]
        except IndexError:
            logging.debug(response.read())
            trackingNumbers.append('NOT FOUND!')
            continue
        logging.debug(redirect)
        if redirect == 'desc':
            trackingNumbers.append('DUPLICATES CHECK MANUALLY!')
            continue
        try:
            response = br.open('https://www.baldorvip.com' + redirect)
            html = response.read()
            soup = BeautifulSoup(html)
            trackingElem = soup.find('th', text='Tracking Number')
            logging.debug(trackingElem)
            logging.debug(trackingElem.nextSibling.contents[1].contents[0])
            trackNumber = str(trackingElem.nextSibling.contents[1].contents[0])
            logging.debug(trackNumber)
            trackingNumbers.append(trackNumber)
            logging.debug(trackingNumbers)
        except Exception as e:
            logging.error(e)
            trackingNumbers.append('NOT FOUND!')
    return trackingNumbers

def search_codes(codes):
    # initialize mechanize
    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.set_handle_robots(False)
    setHeaders(br, headers)
    loginBaldorVip(br, login)
    jsRedirect(br)
    tracking_codes = getOrderStatus(br, codes)
    logging.debug(tracking_codes)
    return tracking_codes

if __name__ == "__main__":
    codes = ['S1163533', 'S1164092', 'S1162946', 'P1053941']
    search_codes(codes)

