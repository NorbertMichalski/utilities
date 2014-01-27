import sys, logging
import mechanize
import cookielib
from bs4 import BeautifulSoup
from urllib import quote
import re

login = {
        'UserName': 'mark1983',
        'Password': 'msais1234',
       }


headers = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4'),
            ('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8'),
            ('Accept', '*/*'),
            ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'),
            # ('Accept-Encoding','gzip,deflate,sdch'),
            ('Accept-Language', 'en-US,en;q=0.8'),
            ('Connection', 'keep-alive'),

           ]

logging.basicConfig(filename='martinSprocket_error.log',
                    format=('%(asctime)s -- line:%(lineno)3d'
                    ' -- %(levelname)s -- \n\t %(message)s'),
                    filemode='a', level=logging.DEBUG)


def setHeaders(browser, headers):
    for header in headers:
        browser.addheaders.append(header)
    # print br.addheaders


def loginMartins(br, login):
    response = br.open('https://btweb.martinsprocket.com/customermenu/Login.aspx?AppCode=OrderStatus')
    br.select_form(nr=0)
    br.form['txtEmail'] = login['UserName']
    br.form['txtPassword'] = login['Password']
    response = br.submit()
    code = response.read()

def searchCode(br, code):
    searchUrl = 'https://btweb.martinsprocket.com/OrderStatus/Default.aspx'
    br.open(searchUrl)
    br.select_form(nr=0)
    br.form['txtPONum'] = code
    response = br.submit(name='butPO', label='Go')
    link_expresion = re.compile('^OrderStatusDetail.aspx')
    try:
        trackingLink = br.find_link(url_regex=link_expresion)
    except mechanize._mechanize.LinkNotFoundError:
        logging.error('order not found')
        trackingNumber = 'NOT FOUND'
        return trackingNumber
    response = br.follow_link(trackingLink)
    html = response.read()
    soup = BeautifulSoup(html)
    try:
        trackingNumber = soup.find('td', {'title':'Click on tracking number to link to the carrier site'}).a.text
    except Exception as e:
        logging.error(e)
        trackingNumber = 'NOT FOUND'
    logging.info(trackingLink)
    logging.info(trackingNumber)
    return trackingNumber


def getOrderStatus(br, codes):
    trackingNumbers = []
    if codes == []:
        return 'You didn\'t paste any content.'
    trackingNumbers = []
    for code in codes :
        logging.debug(code)
        print code
        tracking_number = searchCode(br, code)
        trackingNumbers.append(tracking_number)
    return trackingNumbers

def search_codes(codes):
    # initialize mechanize
    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.set_handle_robots(False)
    setHeaders(br, headers)
    loginMartins(br, login)
    tracking_codes = getOrderStatus(br, codes)
    logging.debug(tracking_codes)
    return tracking_codes

if __name__ == "__main__":
    codes = ['S1166274', 'BAUBAU', 'S1166899', 'S1166625', 'S1166344', 'CACA']
    print search_codes(codes)

