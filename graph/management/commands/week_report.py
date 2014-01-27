from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMessage
from graph.models import OverviewStat, OverviewGraph
from prices.models import Brand, Result
import datetime
import csv


def send_email(text, weekly=True):
    if weekly:
        subject = "weekly report"
    else:
        subject = "daily report"
    email = EmailMessage(subject, text, 'reports@shopmro.com',
                          #['stats.infographics@gmail.com', 'symbiotech3@gmail.com' ])
                           ['mmenashe@mechdrives.com', 'stats.infographics@gmail.com',
                           'mmenashe@gmail.com', 'symbiotech3@gmail.com' ])
    email.content_subtype = "html"
    email.send(fail_silently=False)


def weekly_stats(graph_pk, date):
    stats = OverviewStat.objects.filter(graph=graph_pk).order_by('-date')
    current_week = date.isocalendar()[1] - 1
    print "current_week %d" %current_week
    weekly_money, weekly_price, weekly_rank, weekly_visits, weekly_sales = 0, 0, 0, 0, 0
    counter = 1
    for stat in stats:
        week = stat.date.isocalendar()[1]
        if week == current_week:
            print stat.date
            weekly_money += float('%.2f' %stat.get_money())
            weekly_price += float('%.2f' %(stat.get_price()/10,))
            weekly_rank += stat.get_rank()
            weekly_visits += stat.get_visits()
            weekly_sales += stat.get_sales()
            counter += 1
    return weekly_visits, weekly_sales, weekly_money, int(weekly_rank/counter)


def detect_changes(date, time_interval=7):
    last_week = date - datetime.timedelta(days=time_interval)
    # initialize
    brands = Brand.objects.all()
    counter = {'All':0}
    for brand in brands:
        counter[brand.name] = 0
    # count the changes of prices
    all_results = Result.objects.all().filter(scraped__gte=last_week, scraped__lt=date).prefetch_related('product')
    for result in all_results:
        if result.changed:
            brand_name = result.product.brand.name
            counter[brand_name] += 1
    # total number results/brand
    total = {}
    for brand in brands:
        total[brand.name] = Result.objects.all().filter(scraped__gte=last_week, scraped__lt=date)\
                            .filter(product__brand__name=brand.name).count()
    for brand in brands:
        counter[brand.name] = "%d/%d" %(counter[brand.name], total[brand.name])
    return counter


class HtmlTable(object):
    content = ''
    
    def __init__(self, date=None, weekly=True):
        self.content = self.write_header(date, weekly)
    
    def write_row(self, data):
        row = '<tr>'
        for result in data:
            row += '<td>%s</td>' %result
        row += '</tr>'
        self.content += row
    
    def write_header(self, date=None, weekly=True):
        if not date:
            date = datetime.date.today()
        last_week = date - datetime.timedelta(days=7)
        if weekly:
            text = "<br><br><p>Week of %s to %s.</p><br><br>" %(last_week.strftime("%m/%d/%Y"), date.strftime("%m/%d/%Y"))
        else:
            text = "<br><br><p>Day report of %s.</p><br><br>" %date.strftime("%m/%d/%Y")
        text += '''<table  border="1" cellpadding="5" style="border-collapse: collapse;">
                    <thead>
                    <tr>
                    <th>Brand</th>
                    <th>Total<br>visits</th>
                    <th>Average<br>visits</th>
                    <th>Total<br>sales</th>
                    <th>Average<br>sales</th>
                    <th>Prices<br> changed</th>
                    <th># Prices<br>changed</th>
                    <th>Average<br>rank</th>
                    </tr>
                    </thead>
                    <tbody>'''
        return text

    def write_footer(self):
        self.content += '</tbody></table>'
   
        
class Command(BaseCommand):

    def handle(self, *args, **options):
        today = datetime.date.today()
        
        table = HtmlTable(today)
        counter = detect_changes(today)
        print counter
        sales, visits = [], []
        prices_changed, rank_changed = False, False
        
        # get all brands
        graphs = OverviewGraph.objects.all()[:5]
        for graph in graphs:
            try:
                counter[graph.brand]
            except KeyError:
                continue
            if str(counter[graph.brand]).split('/')[0] is not '0':
                prices_changed = 'Yes'
            else:
                prices_changed = 'No'
            # get the week statistics
            weekly_visits, weekly_sales, weekly_money, weekly_rank = weekly_stats(graph.pk, today)
            data = [graph.brand, weekly_visits, weekly_visits/5, weekly_sales,
                    weekly_sales/5, prices_changed, counter[graph.brand], weekly_rank,
                    ]
            if graph.brand == 'All':
                total_sales = weekly_money
                data = ['All brands', weekly_visits, weekly_visits/5, weekly_sales,
                        weekly_sales/5, '', '', weekly_rank,]
            table.write_row(data)
        table.write_row([])
        data = ['Total profit', total_sales]
        table.write_row(data)
        data = ['Average day profit', '%.2f' %(total_sales/5,)]
        table.write_row(data)
        table.write_footer()
        #write to file
        f = open("/home5/shopmroc/utilities/reports/week_report.txt", 'r+')
        file_content = f.read()
        f.seek(0,0)
        f.write(table.content + '\n' + file_content)
        f.close()
        f = open("/home5/shopmroc/utilities/reports/week_report.txt", 'r')
        file_content = f.read()
        send_email(file_content)
