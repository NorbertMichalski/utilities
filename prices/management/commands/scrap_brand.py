from django.core.management.base import BaseCommand, CommandError
from django.core import management
from prices.models import Product, Brand, Competitor, Result, Archive
from scrapers import TemcoScraper, SqoneScraper, GlobalindustrialScraper, WalkeremdScraper, ElectricmotorwholesaleScraper, MotoragentsScraper
from scrapers import AlliedelecScraper, DigikeyScraper, PlccenterScraper, TranscatScraper, NewarkScraper
from time import sleep
import datetime

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, brand_name, *args, **options):
        competitors = Competitor.objects.filter(brand__name=brand_name)
        brand = Brand.objects.get(name=brand_name)

        for competitor in competitors:
            management.call_command('scrap_competitor', competitor.name.capitalize(), brand_name.capitalize())


        self.stdout.write('Successfully finished')
