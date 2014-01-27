from django.core.management.base import BaseCommand, CommandError
from prices.models import Product, Brand, Competitor, Result, Archive
from scrapers import TemcoScraper, SqoneScraper, GlobalindustrialScraper, WalkeremdScraper, ElectricmotorwholesaleScraper, MotoragentsScraper
from scrapers import AlliedelecScraper, DigikeyScraper, PlccenterScraper, TranscatScraper, NewarkScraper, WbdsScraper, WilliamsonScraper
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
                sleep(1)
                price = scraper.get_price(product.part_number)
                self.stdout.write('%s with price %s' % (product.part_number, price))
                try:
                    existing_result = Result.objects.get(product=product, competitor=competitor)
                    archive = Archive(product=product, competitor=competitor, price=existing_result.price, scraped=existing_result.scraped)
                    if price == existing_result.price:
                        exiting_result.changed = False
                        existing_result.save()
                        print 'price not changed'
                        continue

                    existing_result.price = price
                    existing_result.changed = True
                    if product.mro_price < price:
                        existing_result.is_cheaper = False
                    else:
                        existing_result.is_cheaper = True
                        product.is_cheaper = True
                    existing_result.save()
                    print 'succesfully updated product and archive'

                except:
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


'''
class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, brand_name, competitor_name, *args, **options):
        competitor = Competitor.objects.get(name=competitor_name)
        brand = Brand.objects.get(name=brand_name)
        all_products = Product.objects.select_related().filter(brand=brand)
        print 'scrapers.' + str(competitor.name.capitalize()) + 'Scraper()'
        scraper = eval(str(competitor.name.capitalize()) + 'Scraper()')
        for product in all_products:
            sleep(2)
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

        self.stdout.write('Successfully finished')
'''
