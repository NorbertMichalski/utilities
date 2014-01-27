# -*- coding: utf-8 -*-

import requests
from lxml import html
from datetime import datetime


class EfileScraper(object):
    HEADERS = {'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                             ' (KHTML, like Gecko) Chrome/27.0.1453.73 Safari/537.36'),
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset':'utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding':'gzip,deflate,sdch',
                'Accept-Language':'it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4',
                'Connection':'keep-alive',
                'Content-Type':'application/x-www-form-urlencoded',
                # 'Referer': '',
                # 'Origin': '',
                # 'Host': ''
                }

    def __init__(self, *args, **kwargs):
        self.session = requests.Session()
        self.session.headers = self.HEADERS


    def get_permit(self, tax_num):
        self.session.get('https://efile.boe.ca.gov/boewebservices/verification.jsp?action=SALES')
        resp = self.session.post('https://efile.boe.ca.gov/boewebservices/servlet/BOEVerification',
                                 data={ 'account': tax_num,
                                        'Submit':'Submit Request'
                                        })
        x = html.fromstring(resp.content)
        # extract data
        valid = x.xpath(".//span[contains(@style, 'color: black')]/text() \
                         | .//span[contains(@style, 'color: red')]/text()")
        owner = x.xpath(".//td[contains(text(),'Owner Name:')]/following-sibling::td/text()")
        name = x.xpath(".//td[contains(text(),'Business Name:')]/following-sibling::td/text()")
        address = x.xpath(".//td[contains(text(),'Address:')]/following-sibling::td/text()")
        city = x.xpath(".//td[contains(text(),'Address:')]/following::tr[1]/td[2]/text()")
        state = x.xpath(".//td[contains(text(),'Address:')]/following::tr[2]/td[2]/text()")
        start_date = x.xpath(".//td[contains(text(),'Start Date:')]/following-sibling::td/text() \
                         | .//td[contains(text(),'Closed')]/following-sibling::td/text()")
        #print valid, owner, name, address, city, state, start_date
        output_dict = {'permit_no': tax_num, 'valid': valid,
                        'owner': owner, 'bussiness_name': name,
                        'address': address, 'city': city,
                        'state': state, 'start_date': start_date
                        }
        #clean results
        for key in output_dict:
            if output_dict[key]:
                output_dict[key] = output_dict[key][0].strip()
                if key is 'start_date':
                    output_dict[key] = datetime.strptime(output_dict[key], '%m/%d/%Y')
            else:
                output_dict[key] = ''
        return output_dict

if __name__ == '__main__':
    scraper = EfileScraper()
    # print scraper.get_permit('16626796')
    print scraper.get_permit('97785786')
    print scraper.get_permit('97285643')
