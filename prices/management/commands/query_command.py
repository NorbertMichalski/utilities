from django.core.management.base import BaseCommand, CommandError
from prices.models import Product, Brand, Competitor, Result, Archive
from scrapers import TemcoScraper, SqoneScraper, GlobalindustrialScraper, WalkeremdScraper, ElectricmotorwholesaleScraper, MotoragentsScraper
from scrapers import AlliedelecScraper, DigikeyScraper, PlccenterScraper, TranscatScraper, NewarkScraper, WbdsScraper, MotionindustriesScraper
from time import sleep

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, brand_name, *args, **options):
        competitors = Competitor.objects.filter(brand__name=brand_name)
        brand = Brand.objects.get(name=brand_name)
        all_products = Product.objects.filter(brand=brand).select_related()
        for competitor in competitors:
            print 'now scraping ' + str(competitor.name.capitalize())
            scraper = eval(str(competitor.name.capitalize()) + 'Scraper()')
            for product in all_products:

                try:
                    existing_result = Result.objects.get(product=product, competitor=competitor)
                    print 'already zere'
                    continue

                except:
                    sleep(1)
                    price = scraper.get_price(product.part_number)
                    self.stdout.write('%s with price %s' % (product.part_number, price))
                    if price != 0:
                        result = Result()
                        result.product = product
                        result.competitor = competitor
                        result.price = price
                        if product.mro_price < price:
                            result.is_cheaper = False
                        else:
                            result.is_cheaper = True
                            product.is_cheaper = True
                        result.save()
                        print 'inserted new product'

        self.stdout.write('Successfully finished')


