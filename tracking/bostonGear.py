import sys, logging
import mechanize
import cookielib
from bs4 import BeautifulSoup
from urllib import quote

login = {
        'UserName': 'msais',
        'Password': 'larco1898',
       }


headers = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4'),
            ('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8'),
            ('Accept', '*/*'),
            ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'),
            # ('Accept-Encoding','gzip,deflate,sdch'),
            ('Accept-Language', 'en-US,en;q=0.8'),
            ('Connection', 'keep-alive'),

           ]

logging.basicConfig(filename='bostonGear_error.log',
                    format=('%(asctime)s -- line:%(lineno)3d'
                    ' -- %(levelname)s -- \n\t %(message)s'),
                    filemode='a', level=logging.DEBUG)


def setHeaders(browser, headers):
    for header in headers:
        browser.addheaders.append(header)
    # print br.addheaders


def loginBostonGear(br, login):
    response = br.open('https://www.bostongear.com/smartcat/app/smartbuy/sb_logon.asp?dist=true&code=bostongear')
    br.select_form(nr=0)
    br.form.find_control('items').readonly = False
    br.form['items'] = ''
    br.form['txtUserName'] = login['UserName']
    br.form['txtPassword'] = login['Password']
    response = br.submit()
    code = response.read()
    jsRedirect = code.split('sc_OpenLocation("')[1].split('",')[0]
    jsRedirect2 = code.split('SCROLLING=\'auto\' SRC=\'')[1].split('\'>')[0]
    response = br.open('https://www.bostongear.com/smartcat/app/smartbuy/OrdStatBody.asp?vid=0%2C0%2C0%2C0&ordNo=&sdate=&edate=&pono=S1166625&cname=&cnum=&webno=&prtno=&modno=&brand=')


def compose_link(code):
    code = quote(code)
    link_part1 = 'https://www.bostongear.com/smartcat/app/smartbuy/OrdStatBody.asp?vid=0%2C0%2C0%2C0&ordNo=&sdate=&edate=&pono='
    link_part2 = '&cname=&cnum=&webno=&prtno=&modno=&brand='
    return link_part1 + code + link_part2

def compose_link1(code):
    code = quote(code)
    link_part1 = 'https://www.bostongear.com/smartcat/app/smartbuy/ordstatusdetail.asp?ordno='
    return link_part1 + code


def get_order_number(html):
    try:
        order_number = str(html).split('javascript:ShowItems(\'')[1].split('\')')[0]
    except IndexError:
        order_number = 'NOT FOUND'

    return order_number

def get_tracking_number(html):
    soup = BeautifulSoup(html,'lxml')
    try:
        div = soup.find('th', text='Tracking Number')
        tracking_number = div.parent.nextSibling.nextSibling.contents[5].contents[0].contents[0]
    except IndexError:
        return 'NOT FOUND'
    return tracking_number

def getOrderStatus(br, codes):
    trackingNumbers = []
    if codes == []:
        return 'You didn\'t paste any content.'
    trackingNumbers = []
    for code in codes :
        logging.debug(code)
        print code
        link = compose_link(code)
        logging.debug(link)
        response = br.open(link).read()
        order_number = get_order_number(response)
        print order_number
        if order_number != 'NOT FOUND':
            link = compose_link1(order_number)
            logging.debug(link)
            response = br.open(link).read()
            tracking_number = get_tracking_number(response)
        else:
            tracking_number = 'NOT FOUND'
        trackingNumbers.append(tracking_number)
    return trackingNumbers

def search_codes(codes):
    # initialize mechanize
    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.set_handle_robots(False)
    setHeaders(br, headers)
    loginBostonGear(br, login)
    tracking_codes = getOrderStatus(br, codes)
    logging.debug(tracking_codes)
    return tracking_codes

if __name__ == "__main__":
    codes = ['BAUBAU', 'S1166899', 'S1166625', 'S1166344', 'CACA']
    print search_codes(codes)

