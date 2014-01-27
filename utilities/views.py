# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
# from django.shortcuts import render, get_object_or_404

def home(request):
    page = ('<ul><li><a href="/utilities/supply">Supply Check</a></li>'
            '<li><a href="/utilities/tracking">Tracking Numbers</a></li>'
            '<li><a href="/utilities/shipping">Shipping Calculator</a></li>'
            '<li><a href="/utilities/freightsolution">Freight Calculator</a></li>'
            '<li><a href="/utilities/shipping/international">International Shipping</a></li>'
            '<li><a href="/utilities/resale_cert">Resale Certifications</a></li>'
            '<li><a href="admin">Tutorials</a></li></ul>')
    if request.method == 'GET':
       return HttpResponse(page)
