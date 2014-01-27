# coding: utf-8
from lxml import etree
from lxml import objectify
from datetime import datetime
import requests
import os


def clean_namespaces(root):
    for elem in root.getiterator():
        i = elem.tag.find('}')
        if i >= 0:
            elem.tag = elem.tag[i+1:]
    objectify.deannotate(root, cleanup_namespaces=True)
    return root


class DHLClient(object):
    
    urls = {"test": "https://xmlpitest-ea.dhl.com/XMLShippingServlet",
            "production":"https://xmlpi-ea.dhl.com/XMLShippingServlet"
            }
    
    def __init__(self, debug=True):
        self.site_id = 'MROsupply' 
        self.password = 'R8LYEt9hFO'
        if not debug:
            self.URL = self.urls["production"]
        else:
            self.URL = self.urls["test"]
        this_dir = os.path.dirname(os.path.realpath(__file__))
        self.xsd_dir = os.path.join(this_dir, 'xsd')
        self.xml_dir = os.path.join(this_dir, 'xml')
        
    
    def authenticate(self, message=''):
        '''Create header with the login info. Return lxml objectify instance''' 
        request = objectify.Element('Request')
        header = objectify.SubElement(request, "ServiceHeader")
        header.MessageTime = datetime.today().strftime('%Y-%m-%dT%H:%M:%S%z')
        #header.MessageReference = message
        header.SiteID = self.site_id
        header.Password = self.password
        return request
    
    
    def insert_items(self, items):
        '''Takes all items and creates appropiate xml tags for them.
        Return lxml objectify instance.'''
        pieces = objectify.Element('Pieces')
        for index, item in enumerate(items):
            piece = objectify.SubElement(pieces, "Piece")
            piece.PieceID = index + 1
            if item.weight < 154:
                piece.PackageTypeCode = 'BOX'
            else:
                piece.PackageTypeCode = 'PAL'
            if item.height and item.legth and item.width:
                piece.Height = item.height
                piece.Depth = item.length
                piece.Width = item.width
            piece.Weight = item.weight
        return pieces 
    
    
    def transmit_request(self, xml):
        '''Use requests library to transmit the xml. Return xml string response.'''
        resp = requests.post(self.URL, data=xml.encode('utf-8', 'xmlcharrefreplace'))
        return resp.text
    
    
    def read_schema(self, file_name):
        '''Read xsd file and create from it schema used to verify responses.
         Return parser object.'''
        xsd_file_path = os.path.join(self.xsd_dir, file_name)
        f = open(xsd_file_path, 'rb')
        schema = etree.XMLSchema(file=f)
        parser = objectify.makeparser(schema=schema)
        return parser
    
    
    def objectify_xml(self, file_name):
        '''Read xml file and create from it tree object structure. Return object.''' 
        xml_file_path = os.path.join(self.xml_dir, file_name)
        doc = objectify.parse(xml_file_path)
        root = doc.getroot()
        self.orig_nsmap = root.nsmap
        root = clean_namespaces(root)
        return root
    
    
    def reconstruct_xml(self, root, schema):
        '''Apply appropiate namespaces, nsmap and prefix to the provided object.
         Return lxml Element.'''
        new_root = etree.Element("{http://www.dhl.com}" + root.tag, nsmap=self.orig_nsmap)
        new_root.set("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation", schema)
        new_root[:] = [ el for el in root.iterchildren() ]
        return new_root

    
    def is_dutiable(self, from_country, to_country):
        '''Check if duty taxes are required. Return lxml objectify instance if so.'''
        free_trade = ['US', 'ME', 'CA', 'IL', 'JO', 'AU', 'CL', 'SG', 'BH', 'MA', 'OM',
                      'PE', 'PA', 'CO', 'KR' ]
        if from_country is 'US' and to_country in free_trade:
            return None
        else:
            dutiable = objectify.Element('Dutiable')
            dutiable.DeclaredCurrency = 'USD'
            # need to figure it out
            dutiable.DeclaredValue = '0.00'
            return dutiable
        
    
    def rate(self, packages, shipper, recipient):
        '''Get all available services and their prices. Return dictionary.'''
        # location details
        root = self.objectify_xml("Quote_Request.xml")
        quote = root.GetQuote
        quote.Request = self.authenticate()
        quote.From.CountryCode = shipper.country
        quote.From.Postalcode = shipper.zip
        quote.To.CountryCode = recipient.country
        quote.To.Postalcode = recipient.zip
        # delivery and product details
        quote.BkgDetails.PaymentCountryCode = shipper.country
        quote.BkgDetails.Date = datetime.today().strftime('%Y-%m-%d')
        quote.BkgDetails.ReadyTime = 'PT10H21M'
        dutiable = self.is_dutiable(shipper.country, recipient.country) 
        if not dutiable:
            quote.BkgDetails.IsDutiable = 'N'
            quote.remove(quote.Dutiable)
        else:
            quote.BkgDetails.IsDutiable = 'Y'
            quote.Dutiable = dutiable
        quote.BkgDetails.Pieces = self.insert_items(packages)
        # prepare request
        objectify.deannotate(root, xsi_nil=True, cleanup_namespaces=True)
        root = self.reconstruct_xml(root, "http://www.dhl.com DCT-req.xsd ")
        request_string = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='utf-8')
        print request_string
        resp = self.transmit_request(request_string)
        #print resp
        # response processing
        parser = self.read_schema("DCT-Response.xsd")
        root = objectify.fromstring(str(resp), parser)
        root = clean_namespaces(root)
        try:
            all_results = [ el for el in root.GetQuoteResponse.BkgDetails.iterchildren(tag='QtdShp') ]
        # this means the response contains an error
        except AttributeError as e:
            print e
            error_message = root.GetQuoteResponse.Note.Condition.ConditionData
            return {'status': 'Error', 'info': error_message}
        # results processing
        info = []
        for result in all_results:
            prices = {'WeightCharge':result.WeightCharge}
            try:
                prices.update({i.GlobalServiceName:i.ChargeValue \
                             for i in result.getchildren() if i.tag == 'QtdShpExChrg'})
            except AttributeError:
                    pass
            total_cost = result.ShippingCharge
            if total_cost:
                info.append({
                        'service': result.ProductShortName,
                        'service_code': result.GlobalProductCode,
                        'package': 'BOX',
                        'total_cost': total_cost,
                        'prices': prices,
                        'currency': result.CurrencyCode
                    })
        #request_string = etree.tostring(root, pretty_print=True)
        #print request_string
        quotes = {'status': 'Success', 'info': info}
        return quotes      
    
    
    def tracking(self, aws_numbers_list):
        '''Get shipping status info about the mentioned AWS numbers. Return list.'''
        root = self.objectify_xml("Tracking_Request.xml")
        root.Request = self.authenticate()
        for number in aws_numbers_list:
            awb_number = objectify.SubElement(root, "AWBNumber")
            awb_number._setText(number)
        root.LevelOfDetails = "ALL_CHECK_POINTS"
        # prepare request
        objectify.deannotate(root, xsi_nil=True, cleanup_namespaces=True)
        root = self.reconstruct_xml(root, "http://www.dhl.com TrackingRequestKnown.xsd")
        request_string = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='utf-8')
        print request_string
        resp = self.transmit_request(request_string)
        # there's an error of invalid schema for missing password and invalid date
        # add these when response in not properlly formated
        resp = resp.replace("</SiteID>", "</SiteID>\n<Password>000000000</Password>")
        resp = resp.replace("<ShipmentDate/>", "<ShipmentDate>2011-03-31T18:47:00</ShipmentDate>")
        print resp
        # response processing
        parser = self.read_schema("TrackingResponse.xsd")
        root = objectify.fromstring(str(resp), parser)
        root = clean_namespaces(root)
        all_results = [ el for el in root.iterchildren(tag='AWBInfo') ]
        tracking_info = {}
        for result in all_results:
            info = []
            try:
                all_events = [ el for el in result.ShipmentInfo.iterchildren(tag='ShipmentEvent') ]
            except AttributeError:
                continue
            for event in all_events:
                info.append({
                        'date': event.Date,
                        'time': event.Time,
                        'event': event.ServiceEvent.Description,
                        'location': event.ServiceArea.Description,
                        })
            tracking_info.update({result.AWBNumber: info})
        if tracking_info:
            resp = {'status': 'Success', 'info': tracking_info}
        else:
            resp = {'status': 'Error', 'info': 'No Shipments Found'}
        return resp
