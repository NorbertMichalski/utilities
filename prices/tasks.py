from celery import task
from prices.models import Product, Brand, Competitor, Result, Archive
from scrapers.scrapers import TemcoScraper, SqoneScraper, GlobalindustrialScraper, WalkeremdScraper, ElectricmotorwholesaleScraper, MotoragentsScraper
from scrapers.scrapers import AlliedelecScraper, DigikeyScraper, PlccenterScraper, TranscatScraper, NewarkScraper, KscdirectScraper, WilliamsonScraper
from scrapers.scrapers import MotionindustriesScraper, WbdsScraper
from email_templates import EmailSender
import datetime
import csv


scrapers = {'Motionindustries': MotionindustriesScraper(), 'Temco': TemcoScraper(), 'Sqone': SqoneScraper(), 'Wbds': WbdsScraper(),
            'Globalindustrial': GlobalindustrialScraper(), 'Walkeremd': WalkeremdScraper(),
            'Electricmotorwholesale': ElectricmotorwholesaleScraper(), 'Motoragents': MotoragentsScraper(),
            'Alliedelec': AlliedelecScraper(), 'Digikey': DigikeyScraper(), 'Williamson': WilliamsonScraper(),
            'Transcat': TranscatScraper(), 'Newark': NewarkScraper(), 'Kscdirect': KscdirectScraper(),
            #'Plccenter': PlccenterScraper(),
            }

yesterday = datetime.date.today() - datetime.timedelta(days=1)
today = datetime.date.today()

@task
def scrap_competitor(*args, **kwargs):
    try:
        competitor_name = args[0]
        brand_name = args[1]
    except:
        pass
    brand = Brand.objects.get(name=brand_name)
    competitor = Competitor.objects.get(name=competitor_name)
    if competitor_name.capitalize() == 'Plccenter':
        return
    if competitor_name.capitalize() == 'Kscdirect':
        return
    else:
        #scraper = eval(str(competitor.name.capitalize()) + 'Scraper()')
        scraper = scrapers[competitor.name.capitalize()]
    
    
    previous_results = Result.objects.filter(product__brand=brand, competitor=competitor).exclude(scraped=today).prefetch_related('product')
    for existing_result in previous_results:
        print existing_result.product
        price = scraper.get_price(existing_result.product.part_number)
        if price == 0:
            continue
        print '%s with price %s' % (existing_result.product.part_number, price)

        archive = Archive(product=existing_result.product, competitor=competitor, price=existing_result.price, scraped=existing_result.scraped)
        archive.save()
        print price, existing_result.price
        existing_result.scraped = datetime.date.today()
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

@task
def scrap_brand(*args, **kwargs):
    try:
        brand_name = args[0]
    except:
        pass
    competitors = Competitor.objects.filter(brand__name=brand_name)
    brand = Brand.objects.get(name=brand_name)

    for competitor in competitors:
        scrap_competitor.delay(competitor.name.capitalize(), brand_name.capitalize())


    print 'Successfully finished'

@task
def prices_cheaper_check(*args, **kwargs):
    all_results = Result.objects.all().prefetch_related('product')
    brands = Brand.objects.all()
    files = []
    counter = {}
    for brand_name in brands:
        f = open('/home5/shopmroc/utilities/reports/%s_cheaper.csv' % brand_name, 'wb')
        writer = csv.writer(f, dialect='excel')
        data = ['Brand', 'Competitor', 'MRO id', 'Part Number', 'Our Price', 'Their Price' ]
        writer.writerow(data)
        f.close()
        counter[brand_name.name] = 0
    for result in all_results:
        if result.is_cheaper:
            product_id = result.product
            if not product_id.is_cheaper:
                product_id.is_cheaper = True
                product_id.save()
            mro_id = result.product.mro_id
            part_number = result.product.part_number
            competitor = result.competitor.name
            brand = result.product.brand.name
            price = result.price
            mro_price = result.product.mro_price

            f = open('/home5/shopmroc/utilities/reports/%s_cheaper.csv' % brand, 'ab')
            writer = csv.writer(f, dialect='excel')
            data = [brand, competitor, mro_id, part_number, mro_price, price ]
            writer.writerow(data)
            f.close()
            counter[brand] += 1
    for brand in brands:
        EmailSender(brand.name, 'cheaper', counter[brand.name])

@task
def prices_changes_check(*args, **kwargs):
    all_results = Result.objects.all().prefetch_related('product')
    brands = Brand.objects.all()
    files = []
    counter = {}
    for brand in brands:
        f = open('/home5/shopmroc/utilities/reports/%s_changes.csv' % brand.name, 'wb')
        writer = csv.writer(f, dialect='excel')
        data = ['Brand', 'Competitor', 'MRO id', 'Part Number', 'MRO Price', 'New Price',
                'Date Scraped', 'Old Price', 'Previous Date', 'Percentage Change' ]
        writer.writerow(data)
        f.close()
        counter[brand.name] = 0
    for result in all_results:
        if result.changed:
            product_id = result.product
            competitor_id = result.competitor
            mro_id = result.product.mro_id
            part_number = result.product.part_number
            competitor = result.competitor.name
            brand = result.product.brand.name
            price = result.price
            old_price = result.previous_price()
            mro_price = result.MRO_price()
            previous_date = result.previous_date()
            date = result.scraped
            percentage_changed = result.percentage_change()

            f = open('/home5/shopmroc/utilities/reports/%s_changes.csv' % brand, 'ab')
            writer = csv.writer(f, dialect='excel')
            data = [brand, competitor, mro_id, part_number,mro_price, price, date, old_price, previous_date, percentage_changed ]
            writer.writerow(data)
            f.close()
            counter[brand] += 1
    for brand in brands:
        EmailSender(brand.name, 'changes', counter[brand.name])