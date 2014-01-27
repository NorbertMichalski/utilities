# coding: utf-8
import re


class Package(object):
    def __init__(self, weight, length=None, width=None, height=None, value=0,
                 require_signature=False, reference=u''):
        self.weight = weight
        self.length = length
        self.width = width
        self.height = height
        self.value = value
        self.require_signature = require_signature
        self.reference = reference


class Address(object):
    def __init__(self, zip, country, name='', address='', city='', state='', address2='',
                 phone='', email='', is_residence=True, company_name=''):
        self.company_name = company_name or ''
        self.name = name or ''
        self.address1 = address or ''
        self.address2 = address2 or ''
        self.city = city or ''
        self.state = state or ''
        self.zip = re.sub('[^\w]', '', unicode(zip).split('-')[0]) if zip else ''
        self.country = country or ''
        self.phone = re.sub('[^0-9]*', '', unicode(phone)) if phone else ''
        self.email = email or ''
        self.is_residence = is_residence or False



def get_country_code(country):
    lookup = {
        'us': 'US',
        'usa': 'US',
        'united states': 'US',
    }

    return lookup.get(country.lower(), country)
