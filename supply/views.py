from django.shortcuts import render, get_object_or_404
from django.core.context_processors import csrf
from django.http import HttpResponse
from supply.models import Location, Brand, InputForm, Product

import json
from scripts.baldor import BaldorScraper
from scripts.bando import BandoScraper
from scripts.boston import BostonScraper
from scripts.dodge import DodgeScraper
from scripts.gates import GatesScraper
from scripts.leeson import LeesonScraper
from scripts.martin import MartinScraper
from scripts.maska import MaskaScraper
from scripts.mrc import MrcScraper
from scripts.nachi import NachiScraper
from scripts.nexen import NexenScraper
from scripts.redlion import RedlionScraper
from scripts.weg import WegScraper
from geolocation import Locate
import logging

logger = logging.getLogger(__name__)


def change_keys(dict):
    new_dict = {}
    for key in dict:
        found_location = Location.objects.filter(slug=key)[0].city_state
        found_location = str(found_location.split(',')[0].capitalize() + found_location.split(',')[1].upper())
        new_dict[found_location] = dict[key]
    return new_dict

def index(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            codes1 = form.cleaned_data['codes']
            logger.debug(codes1)
            if codes1.find(',') != -1:
                codes = codes1.split(',')
            elif codes1.find('\r\n') != -1:
                codes = codes1.split('\r\n')
            else:
                codes = ['', ]
                codes.append(codes1)

            logger.debug(codes)

            company = form.cleaned_data['company']
            zip_code = form.cleaned_data['zipcode'].strip()
            your_location = form.cleaned_data['yourlocation']
            try:
                origin_location = list(eval(your_location))
            except Exception as e:
                print e
                origin_location = False

            name = company.capitalize()
            scraper = eval(name + 'Scraper()')
            output_data = []
            weights = {}
            coordinates = {}
            local_time = {}
            distance = {}
            warehouse_zip = {}
            city_states = {}
            for code in codes:
                if code == '':
                    continue
                availability = scraper.get_availability(code.strip())
                try:
                    #weight = Product.objects.filter(brand__name=company.lower(), part_number=code.strip())[0].weight
                    weight = Product.objects.filter(part_number=code.strip())[0].weight
                except IndexError:
                    weight = 0
                for location, value in availability.items():
                    if value == 0 or location.encode('UTF-8', errors='ignore') == '':
                        del availability[location]
                    else:
                        if not location in coordinates:
                            location_handler = Locate()
                            lat, long = location_handler.search_location(company, location)
                            coordinates[location] = list((lat, long))
                            local_time[location] = location_handler.get_local_time(location)
                            city_states[location] = location_handler.get_city_state(location)
                            if zip_code != '' and origin_location:
                                distance[location] = location_handler.distance(origin_location, list((lat, long)))
                                warehouse_zip[location] = location_handler.get_zip(lat, long)
                output = json.dumps(availability)
                output_data.append((str(code), output))
                weights[code] = weight

            context = {'info': 'Done. The results are sorted by distance.', 'locations': output_data, 'coordinates': json.dumps(coordinates),
                       'local_time':local_time, 'distances':distance, 'your_location':your_location[1:-1], 'zip_code':zip_code,
                       'your_location':your_location, 'warehouse_zip':warehouse_zip, 'weights':weights, 'city_states':city_states}
            return render(request, 'supply/index.html', context)

        else:
            context = {'info': 'You didn\'t introduced any data.'}
            return render(request, 'supply/index.html', context)
    else:
        form = InputForm()
        context = {'info': 'Please insert data.'}
        return render(request, 'supply/index.html', context)


def baldor_availability(request, part_number):
    if request.method == 'GET':
        scraper = BaldorScraper()
        availability = scraper.get_availability(part_number)
        output = json.dumps(availability)
        return HttpResponse(output)


def calculate_distances(request):
    if request.method == 'GET':
        address = request.GET.get('address', '')
        warehouses = Location.objects.filter(brand__name='Baldor')
        location_handler = Locate()
        lat, long = location_handler.geolocate(address)
        distances = {}
        for location in warehouses:
            warehouse_lat = location.latitude
            warehouse_long = location.longitude
            distances[location.slug] = location_handler.distance(list((lat, long)), list((warehouse_lat, warehouse_long)))

        output = json.dumps(distances)
        return HttpResponse(output)
    
def calculate_distances1(request):
    if request.method == 'GET':
        brand = request.GET.get('brand', '')
        address = request.GET.get('address', '')
        warehouses = Location.objects.filter(brand__name=brand.lower())
        location_handler = Locate()
        lat, long = location_handler.geolocate(address)
        distances = {}
        for location in warehouses:
            warehouse_lat = location.latitude
            warehouse_long = location.longitude
            distances[location.slug] = location_handler.distance(list((lat, long)), list((warehouse_lat, warehouse_long)))

        output = json.dumps(distances)
        return HttpResponse(output)    
    
def get_weight(request):
    if request.method == 'GET':
        part_number = request.GET.get('part_number', '').strip()
        try:
            weight = Product.objects.get(part_number=part_number).weight
            weight = float(weight)
        except Exception as e:
            weight = 0
        output = json.dumps({'part_number': part_number, 'weight': weight})
        return HttpResponse(output)