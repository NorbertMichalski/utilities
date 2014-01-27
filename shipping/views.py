# Create your views here.
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.context_processors import csrf
from datetime import datetime
import json

from shipping.models import InputForm, InternationalForm
from UPS_scraper import UpsScraper
from IdcUsa import IdcScraper
from ups.client import UPSClient
from ups.model import Address, Package
from dhl.client import DHLClient


def index(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        # return HttpResponse(form.cleaned_data)
        if form.is_valid():
            zipcode1 = form.cleaned_data['zipcode1']
            zipcode2 = form.cleaned_data['zipcode2']
            weight = form.cleaned_data['weight']
            date1 = form.cleaned_data['date1']
            carrier = form.cleaned_data['carrier']
            if carrier == 'UPS':
                scraper = UpsScraper()
                # print scraper.get_availability('AEM2238-4')
                results = scraper.get_estimate(zipcode1, zipcode2, weight, date1)
                if results == '':
                    context = {'info': 'The UPS website is down. Please try again later.'}
                    return render(request, 'shipping/index.html', context)

            if carrier == 'IDC':
                #scraper = IdcScraper()
                #results = scraper.get_estimate(zipcode1, zipcode2, weight)
                context = {'info': 'The IDC_USA service is not available.'}
                return render(request, 'shipping/index.html', context)

            context = {'results':results, 'info':'Done. These are all the results.', 'zipcode1':zipcode1, 'zipcode2':zipcode2, 'weight':weight, 'date1':date1.strftime('%m/%d/%Y')}
            return render(request, 'shipping/index.html', context)

        else:
            context = {'info': 'The data introduced is not valid.'}
            return render(request, 'shipping/index.html', context)
    else:
        form = InputForm()
        context = {'results': ''}
        return render(request, 'shipping/index.html', context)


def estimate(request):
    today = datetime.today()
    # date = today.strftime('%m/%d/%Y')
    if request.method == 'GET':
        zipcode1 = request.GET.get('zipcode1', '')
        zipcode2 = request.GET.get('zipcode2', '')
        weight = request.GET.get('weight', 0)
        if float(weight) == 0:
            weight = 0.9
            
        if float(weight) > 150:
            scraper = UpsScraper()
            ups_result = scraper.get_freight_estimate(zipcode1, zipcode2, weight)
            scraper = IdcScraper()
            idc_result = scraper.get_freight(zipcode1, zipcode2, weight, today)
            output = 'UPS Next Day Air:<br>$%s<br>FedEx Freight:<br>$%s' %(ups_result, idc_result)
        else:
            scraper = UpsScraper()
            ups_result = scraper.get_ups_ground(zipcode1, zipcode2, weight, today)
            scraper = IdcScraper()
            idc_result = scraper.get_freight(zipcode1, zipcode2, weight, today)
            output = 'UPS Ground:<br>$%s<br>FedEx Freight:<br>$%s' %(ups_result, idc_result)
        return HttpResponse(output)



def international(request):
    mro_credentials = { 'username': 'mrosupply_ups',
                        'password': '1o8c9r8al!@#$',
                        'access_license': '6CC3FBEBBDC01626',
                        'shipper_number': '929702'
                        }
    if request.method == 'POST':
        form = InternationalForm(request.POST)
        #return HttpResponse(form.is_valid())
        if form.is_valid():
            from_zipcode = form.cleaned_data['zipcode1']
            to_zipcode = form.cleaned_data['zipcode2']
            from_country = form.cleaned_data['from_country']
            to_country = form.cleaned_data['to_country']
            weight = form.cleaned_data['weight']
            carrier = form.cleaned_data['carrier']
            
            package = [Package(weight)]
            from_address = Address(zip=from_zipcode, country=from_country)
            to_address = Address(zip=to_zipcode, country=to_country)
            
            
            if carrier == 'UPS':
                ups = UPSClient(mro_credentials)
                response = ups.rate(packages=package, packaging_type='02',
                                 shipper=from_address, recipient=to_address)
                content = response["info"]
            else:
                dhl = DHLClient()
                response = dhl.rate(packages=package, shipper=from_address,
                                     recipient=to_address)
                content = response["info"]
            table = "<table><thead><tr><th>Service</th><th>Price</th></tr></thead><tbody>"
            for result in content:
                shipping_method = result["service"]
                price = result["total_cost"]
                table += "<tr><td>%s</td><td>%s</td></tr>" %(shipping_method, price)
            table += "</tbody></table>" 
            context = {'results':table, 'info':'Done. These are all the results.', 'zipcode1':from_zipcode, 'zipcode2':to_zipcode,
                        'weight':weight}
            return render(request, 'shipping/international.html', context)

        else:
            context = {'info': 'The data introduced is not valid.'}
            return render(request, 'shipping/international.html', context)
    else:
        form = InputForm()
        context = {'results': ''}
        return render(request, 'shipping/international.html', context)
    
    
