# coding: utf-8
import urllib
import urlparse
import os
import suds
import logging

from suds.client import Client
from suds.sax.element import Element
from suds.plugin import MessagePlugin

logger = logging.getLogger(__name__)

SERVICES = {
    '01': 'UPS Next Day',
    '02': 'UPS 2nd Day',
    '03': 'UPS Ground',
    '07': 'UPS Worldwide Express',
    '08': 'UPS Worldwide Expedited',
    '11': 'UPS Standard',
    '12': 'UPS 3-day Select',
    '13': 'UPS Next Day Air Saver',
    '14': 'UPS Next Day AM',
    '54': 'UPS Worldwide Express Plus',
    '59': 'UPS 2nd Day AM',
    '65': 'UPS Saver',
}

PACKAGES = {
    '02': 'Custom Packaging',
    '01': 'UPS Letter',
    '03': 'Tube',
    '04': 'PAK',
    '21': 'UPS Express Box',
    '2a': 'Small Express Box',
    '2b': 'Medium Express Box',
    '2c': 'Large Express Box',
}

mro_credentials = {
    'username': 'mrosupply_ups',
    'password': '1o8c9r8al!@#$',
    'access_license': '6CC3FBEBBDC01626',
    'shipper_number': '929702'
}


class UPSError(Exception):
    def __init__(self, fault, document):
        self.fault = fault
        self.document = document
        code = self.document.childAtPath('/detail/Errors/ErrorDetail/PrimaryErrorCode/Code')
        if code:
            code = code.getText()
        else:
            code = fault.detail.Errors.ErrorDetail.PrimaryErrorCode.Code
        text = self.document.childAtPath('/detail/Errors/ErrorDetail/PrimaryErrorCode/Description')
        if text:
            text = text.getText()
        else:
            text = fault.detail.Errors.ErrorDetail.PrimaryErrorCode.Description
        error_text = 'UPS Error %s: %s' % (code, text)

        super(UPSError, self).__init__(error_text)


class FixRequestNamespacePlug(MessagePlugin):
    def marshalled(self, context):
        context.envelope.getChild('Body').getChild('RateRequest').getChild('Request').prefix = 'ns0'


class UPSClient(object):

    def __init__(self, credentials=mro_credentials, weight_unit='LBS', dimension_unit='IN', currency_code='USD', debug=True):
        this_dir = os.path.dirname(os.path.realpath(__file__))
        self.wsdl_dir = os.path.join(this_dir, 'wsdl')
        self.credentials = credentials
        self.weight_unit = weight_unit
        self.dimension_unit = dimension_unit
        self.currency_code = currency_code
        self.debug = debug

    def _add_security_header(self, client):
        security_ns = ('upss', 'http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0')
        security = Element('UPSSecurity', ns=security_ns)

        username_token = Element('UsernameToken', ns=security_ns)
        username = Element('Username', ns=security_ns).setText(self.credentials['username'])
        password = Element('Password', ns=security_ns).setText(self.credentials['password'])
        username_token.append(username)
        username_token.append(password)

        service_token = Element('ServiceAccessToken', ns=security_ns)
        license = Element('AccessLicenseNumber', ns=security_ns).setText(self.credentials['access_license'])
        service_token.append(license)

        security.append(username_token)
        security.append(service_token)

        client.set_options(soapheaders=security)

    def _normalized_country_code(self, country):
        country_lookup = {
            'usa': 'US',
            'united states': 'US',
        }
        return country_lookup.get(country.lower(), country)

    def wsdlURL(self, wsdl_name):
        wsdl_file_path = os.path.join(self.wsdl_dir, wsdl_name)
        # Get the os specific url to deal with windows drive letter
        wsdl_file_url = urllib.pathname2url(wsdl_file_path)
        wsdl_url = urlparse.urljoin('file://', wsdl_file_url)
        return wsdl_url

    def _get_client(self, wsdl):
        wsdl_url = self.wsdlURL(wsdl)

        # Setting prefixes=False does not help
        return Client(wsdl_url, plugins=[FixRequestNamespacePlug()])

    def _create_shipment(self, client, packages, shipper_address,
                         recipient_address, box_shape, service_code, namespace='ns3',
                         create_reference_number=True,
                         can_add_delivery_confirmation=True):
        shipment = client.factory.create('{}:ShipmentType'.format(namespace))

        for i, p in enumerate(packages):
            package = client.factory.create('{}:PackageType'.format(namespace))

            if hasattr(package, 'Packaging'):
                package.Packaging.Code = box_shape
            elif hasattr(package, 'PackagingType'):
                package.PackagingType.Code = box_shape

            if p.length and p.width and p.height:
                package.Dimensions.UnitOfMeasurement.Code = self.dimension_unit
                package.Dimensions.Length = p.length
                package.Dimensions.Width = p.width
                package.Dimensions.Height = p.height

            package.PackageWeight.UnitOfMeasurement.Code = self.weight_unit
            package.PackageWeight.Weight = p.weight

            if can_add_delivery_confirmation and p.require_signature:
                package.PackageServiceOptions.DeliveryConfirmation.DCISType = str(p.require_signature)

            if p.value:
                package.PackageServiceOptions.DeclaredValue.CurrencyCode = self.currency_code
                package.PackageServiceOptions.DeclaredValue.MonetaryValue = p.value

            if create_reference_number and p.reference:
                try:
                    reference_number = client.factory.create('{}:ReferenceNumberType'.format(namespace))
                    reference_number.Value = p.reference
                    package.ReferenceNumber.append(reference_number)
                except suds.TypeNotFound:
                    pass

            shipment.Package.append(package)

        shipfrom_name = shipper_address.name[:35]
        shipfrom_company = shipper_address.company_name[:35]
        shipment.Shipper.Name = shipfrom_company or shipfrom_name
        address_line = [shipper_address.address1]
        if shipper_address.address2:
            address_line.append(shipper_address.address2)
        shipment.Shipper.Address.AddressLine = address_line
        shipment.Shipper.Address.City = shipper_address.city
        shipment.Shipper.Address.PostalCode = shipper_address.zip
        shipper_country = self._normalized_country_code(shipper_address.country)
        shipment.Shipper.Address.CountryCode = shipper_country
        shipment.Shipper.ShipperNumber = self.credentials['shipper_number']

        shipto_name = recipient_address.name[:35]
        shipto_company = recipient_address.company_name[:35]
        shipment.ShipTo.Name = shipto_company or shipto_name
        address_line = [recipient_address.address1]
        if recipient_address.address2:
            address_line.append(recipient_address.address2)
        shipment.ShipTo.Address.AddressLine = address_line
        shipment.ShipTo.Address.City = recipient_address.city
        shipment.ShipTo.Address.PostalCode = recipient_address.zip
        recipient_country = self._normalized_country_code(recipient_address.country)
        shipment.ShipTo.Address.CountryCode = recipient_country

        # Only add states if we're shipping to/from US, PR, or Ireland
        if shipper_country in ( 'US', 'CA', 'IE' ):
            shipment.Shipper.Address.StateProvinceCode = shipper_address.state
        if recipient_country in ( 'US', 'CA', 'IE' ):
            shipment.ShipTo.Address.StateProvinceCode = recipient_address.state

        if recipient_address.is_residence:
            shipment.ShipTo.Address.ResidentialAddressIndicator = ''
        if service_code is not None:
            shipment.Service.Code = service_code
            shipment.Service.Description = 'Service Code'
            shipment.ShipmentServiceOptions = ''

        return shipment

    def rate(self, packages, shipper, recipient, service_code=None, packaging_type='02'):

        client = self._get_client('RateWS.wsdl')
        self._add_security_header(client)
        client.set_options(location='https://onlinetools.ups.com/webservices/Rate')

        request = client.factory.create('ns0:RequestType')
        request.RequestOption = 'Shop' if service_code is None else "Rate"

        classification = client.factory.create('ns2:CodeDescriptionType')
        classification.Code = '00'  # Get rates for the shipper account
        classification.Description = 'Classification'  # Get rates for the shipper account

        pickup = client.factory.create('ns2:PickupType')
        pickup.Code = '01'
        pickup.Description = 'Daily Pickup'

        shipment = self._create_shipment(client, packages, shipper, recipient,
            packaging_type, namespace='ns2', service_code=service_code)
        shipment.ShipmentRatingOptions.NegotiatedRatesIndicator = ''

        try:
            response = client.service.ProcessRate(Request=request, PickupType=pickup,
                CustomerClassification=classification, Shipment=shipment)
            print response
            info = list()
            for r in response.RatedShipment:
                unknown_service = 'Unknown Service: {}'.format(r.Service.Code)
                try:
                    cost = r.NegotiatedRateCharges.TotalCharge.MonetaryValue
                    currency = r.NegotiatedRateCharges.TotalCharge.CurrencyCode
                except AttributeError:
                    cost = r.TotalCharges.MonetaryValue
                    currency = r.TotalCharges.CurrencyCode

                info.append({
                    'service': SERVICES.get(r.Service.Code, unknown_service),
                    'service_code': r.Service.Code,
                    'package': packaging_type,
                    'total_cost': cost,
                    'prices': [i.TotalCharges.MonetaryValue for i in r.RatedPackage],
                    'currency': currency
                })

            response = {'status': response.Response.ResponseStatus.Description, 'info': info}
            return response
        except suds.WebFault as e:
            raise UPSError(e.fault, e.document)
