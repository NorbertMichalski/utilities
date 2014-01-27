from django.core.management.base import BaseCommand, CommandError
from prices.models import Product, Brand, Competitor, Result, Archive
from scrapers import TemcoScraper, SqoneScraper, GlobalindustrialScraper, WalkeremdScraper, ElectricmotorwholesaleScraper, MotoragentsScraper
from scrapers import AlliedelecScraper, DigikeyScraper, PlccenterScraper, TranscatScraper, NewarkScraper, WbdsScraper, MotionindustriesScraper
from scrapers import KscdirectScraper, WilliamsonScraper
from time import sleep
from datetime import date
import datetime

yesterday = datetime.date.today() - datetime.timedelta(days=1)
today = datetime.date.today()

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, competitor_name, brand_name, *args, **options):
        brand = Brand.objects.get(name=brand_name)
        competitor = Competitor.objects.get(name=competitor_name)
        
        if competitor_name.capitalize() == 'Kscdirect':
            return
        if competitor_name.capitalize() == 'Plccenter':
            scraper = PlccenterScraper(brand_name.capitalize())
        else:
            scraper = eval(str(competitor.name.capitalize()) + 'Scraper()')

        previous_results = Result.objects.filter(product__brand=brand, competitor=competitor).exclude(scraped=yesterday).exclude(scraped=today).prefetch_related('product')
        for existing_result in previous_results:
            print existing_result.product
            price = scraper.get_price(existing_result.product.part_number)
            if price == 0:
                continue
            self.stdout.write('%s with price %s' % (existing_result.product.part_number, price))

            archive = Archive(product=existing_result.product, competitor=competitor, price=existing_result.price, scraped=existing_result.scraped)
            archive.save()
            print price, existing_result.price
            existing_result.scraped = date.today()
            if float(price) == float(existing_result.price):
                existing_result.changed = False
                existing_result.save()
                print 'price not changed'
                continue

            existing_result.price = price
            existing_result.changed = True
            if float(existing_result.product.mro_price) < float(price):
                existing_result.is_cheaper = False
            else:
                existing_result.is_cheaper = True
                existing_result.product.is_cheaper = True
            existing_result.save()
            print 'succesfully updated product and archive'
