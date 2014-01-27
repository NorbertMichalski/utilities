from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMessage
from graph.models import OverviewStat, OverviewGraph
from prices.models import Brand, Result
import datetime
import csv


def send_email(table):
    subject = "weekly report"
    body = "<p>This is the weekly statistics report.</p><br><br>"
    body += table
    email = EmailMessage(subject, body, 'reports@shopmro.com',
                          ['mmenashe@mechdrives.com', 'stats.infographics@gmail.com', 'symbiotech3@gmail.com' ])
    email.content_subtype = "html"
    email.send(fail_silently=False)


def weekly_stats(graph_pk):
    stats = OverviewStat.objects.filter(graph=graph_pk).order_by('-date')
    current_week = stats[0].date.isocalendar()[1]
    weekly_money, weekly_price, weekly_rank, weekly_visits, weekly_sales = 0, 0, 0, 0, 0
    counter = 1
    for stat in stats:
        week = stat.date.isocalendar()[1]
        if week != current_week:
            break
        weekly_money += float('%.2f' %stat.get_money())
        weekly_price += float('%.2f' %(stat.get_price()/10,))
        weekly_rank += stat.get_rank()
        weekly_visits += stat.get_visits()
        weekly_sales += stat.get_sales()
        counter += 1
    return weekly_visits, weekly_sales, weekly_money, int(weekly_rank/counter)


def write_row(data):
    row = '<tr>'
    for result in data:
        row += '<td>%s</td>' %result
    row += '</tr>'
    return row


class Command(BaseCommand):

    def handle(self, *args, **options):
        # creta html table header
        table = '''<table  border="1" cellpadding="5" style="border-collapse: collapse;">
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
        # count the changes of prices
        brands = Brand.objects.all()
        counter = {'All':0}
        for brand in brands:
            counter[brand.name] = 0
        all_results = Result.objects.all().prefetch_related('product')
        for result in all_results:
            if result.changed:
                brand_name = result.product.brand.name
                counter[brand_name] += 1
        print counter
        sales, visits = [], []
        prices_changed, rank_changed = False, False
        # if not monday get last moday's report
        today = datetime.date.today()
        week_day = today.weekday() 
        if week_day:
            today = today - datetime.timedelta(days=week_day)
        print today
        # get all brands
        graphs = OverviewGraph.objects.all()[:5]
        for graph in graphs:
            try:
                counter[graph.brand]
            except KeyError:
                continue
            if counter[graph.brand]:
                prices_changed = 'Yes'
            else:
                prices_changed = 'No'
            # get the week statistics
            weekly_visits, weekly_sales, weekly_money, weekly_rank = weekly_stats(graph.pk)
            data = [graph.brand, weekly_visits, weekly_visits/5, weekly_sales,
                    weekly_sales/5, prices_changed, counter[graph.brand], weekly_rank,
                    ]
            if graph.brand == 'All':
                total_sales = weekly_money
                data = ['All brands', weekly_visits, weekly_visits/5, weekly_sales,
                        weekly_sales/5, '', '', weekly_rank,]
            table += write_row(data)
        table += write_row([])
        data = ['Total profit', total_sales]
        table += write_row(data)
        data = ['Average day profit', '%.2f' %(total_sales/5,)]
        table += write_row(data)
        table += '</tbody></table>'
        send_email(table)
