from django.core.management.base import BaseCommand, CommandError
from prices.models import Product, Brand, Competitor, Result, Archive
from scrapers import TemcoScraper, SqoneScraper, GlobalindustrialScraper, WalkeremdScraper, ElectricmotorwholesaleScraper, MotoragentsScraper
from scrapers import AlliedelecScraper, DigikeyScraper, PlccenterScraper, TranscatScraper, NewarkScraper, WbdsScraper, MotionindustriesScraper
from time import sleep
from datetime import date


class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        all_results = Result.objects.all().prefetch_related()
        for result in all_results:
            mro_price = result.product.mro_price
            price = result.price
            if float(mro_price < price):
                result.is_cheaper = False
                result.save()
                product = result.product
                product.is_cheaper = False
                product.save()
                print 'not cheaper', mro_price,price
            else:
                result.is_cheaper = True
                result.save()
                product = result.product
                product.is_cheaper = True
                product.save()
                print 'cheaper', mro_price, price