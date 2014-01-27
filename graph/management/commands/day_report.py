from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMessage
from graph.models import OverviewStat, OverviewGraph
from prices.models import Brand, Result
import datetime
import csv

from week_report import send_email, detect_changes, HtmlTable


def daily_stats(graph_pk, date):
    stats = OverviewStat.objects.filter(graph=graph_pk).order_by('-date')
    daily_money, daily_price, daily_rank, daily_visits, daily_sales = 0, 0, 0, 0, 0
    counter = 1
    for stat in stats:
        if stat.date == date:
            print stat.date
            daily_money += float('%.2f' %stat.get_money())
            daily_price += float('%.2f' %(stat.get_price()/10,))
            daily_rank += stat.get_rank()
            daily_visits += stat.get_visits()
            daily_sales += stat.get_sales()
            break
    return daily_visits, daily_sales, daily_money, int(daily_rank/counter)

   
        
class Command(BaseCommand):

    def handle(self, *args, **options):
        today = datetime.date.today() - datetime.timedelta(days=1)
        
        table = HtmlTable(today, weekly=False)
        counter = detect_changes(today, 1)
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
            if counter[graph.brand]:
                prices_changed = 'Yes'
            else:
                prices_changed = 'No'
            # get the week statistics
            daily_visits, daily_sales, daily_money, daily_rank = daily_stats(graph.pk, today)
            data = [graph.brand, daily_visits, daily_visits, daily_sales,
                    daily_sales, prices_changed, counter[graph.brand], daily_rank,
                    ]
            if graph.brand == 'All':
                total_sales = daily_money
                data = ['All brands', daily_visits, daily_visits, daily_sales,
                        daily_sales, '', '', daily_rank,]
            table.write_row(data)
        table.write_row([])
        data = ['Total profit', total_sales]
        table.write_row(data)
        data = ['Average day profit', '%.2f' %total_sales]
        table.write_row(data)
        table.write_footer()
        #write to file
        f = open("/home5/shopmroc/utilities/reports/day_report.txt", 'r+')
        file_content = f.read()
        f.seek(0,0)
        f.write(table.content + '\n' + file_content)
        f.close()
        f = open("/home5/shopmroc/utilities/reports/day_report.txt", 'r')
        file_content = f.read()
        send_email(file_content, weekly=False)
