# Create your views here.
# from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.context_processors import csrf
import baldorVip
import bostonGear
import martinSprocket
import json
from scripts.baldor import BaldorScraper
# from scripts.bando import BandoScraper
from scripts.boston import BostonScraper
from scripts.dodge import DodgeScraper
from scripts.gates import GatesScraper
from scripts.leeson import LeesonScraper
from scripts.martin import MartinScraper
from scripts.maska import MaskaScraper
from scripts.mrc import MrcScraper
# from scripts.nachi import NachiScraper
# from scripts.nexen import NexenScraper
from scripts.redlion import RedlionScraper
from scripts.weg import WegScraper

from tracking.models import Shipping, InputForm

def index(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        # return HttpResponse(form.cleaned_data)
        if form.is_valid():
            codes = form.cleaned_data['codes'].split('\r\n')
            company = form.cleaned_data['company']
            if company == 'BaldorVip':
                tracking_numbers = baldorVip.search_codes(codes)
            elif company == 'BostonGear':
                tracking_numbers = bostonGear.search_codes(codes)
            elif company == 'MartinSp':
                tracking_numbers = martinSprocket.search_codes(codes)
            else:
                name = company[0].upper() + company[1:]
                scraper = eval(name + 'Scraper()')
                tracking_numbers = []
                for code in codes:
                    if code == '':
                        continue
                    track_number = scraper.get_tracking(code)
                    tracking_numbers.append(track_number)

            tracking_numbers = '\r\n'.join(tracking_numbers)
            codes = '\r\n'.join(codes)
            context = {'codes':codes, 'company': company, 'tracking': tracking_numbers, 'info':'Done. These are all the results.'}
            return render(request, 'tracking/index.html', context)

        else:
            context = {'info': 'You didn\'t introduced any data.'}
            return render(request, 'tracking/index.html', context)
    else:
        form = InputForm()
        context = {'tracking': ''}
        return render(request, 'tracking/index.html', context)

