# Create your views here.
# Create your views here.
# from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.context_processors import csrf
from datetime import datetime
from resale_cert.models import InputForm, Reseller
from scrapper.efile import EfileScraper


def index(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        # return HttpResponse(form.cleaned_data)
        if form.is_valid():
            permit_number = form.cleaned_data['permit_number']
            scraper = EfileScraper()
            output = scraper.get_permit(permit_number)
            reseller = Reseller()
            reseller.write_output(output)

            context = {'owner': output['owner'], 'status':output['valid']}
            return render(request, 'resale_cert/index.html', context)

        else:
            context = {'info': 'The data introduced is not valid.'}
            return render(request, 'resale_cert/index.html', context)
    else:
        form = InputForm()
        context = {'results': ''}
        return render(request, 'resale_cert/index.html', context)

