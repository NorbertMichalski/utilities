from django.db import models
from django.template.loader import render_to_string
from prices.models import Product, Result
from scrapers import ClickyScraper, RankScraper, OrderScraper, CashScraper
import datetime

# Create your models here.

class OverviewGraph(models.Model):
    brand = models.CharField(max_length=50, unique=True)
    
    class Meta:
        ordering = ['id']
    
    def __unicode__(self):
        return self.brand
    
    def chart(self):
        graph_pk = self.pk % 5
        if graph_pk == 0:
            graph_pk = 5
        stats = OverviewStat.objects.filter(graph=graph_pk).order_by('date')
        title = self.__unicode__().capitalize() + ' Statistics'
        prices = []
        ranks = []
        all_sales = []
        all_visits = []
        dates = []
        money = []
        if 'weekly' in self.brand:
            current_week = stats[0].date.isocalendar()[1]
            weekly_money, weekly_price, weekly_rank, weekly_visits, weekly_sales = 0, 0, 0, 0, 0
            counter = 1
            for stat in stats:
                week = stat.date.isocalendar()[1]
                if week != current_week:
                    if self.brand == 'All weekly':
                        money.append(float('%.2f' %weekly_money))
                    prices.append(float('%.2f' %(weekly_price/counter, )))
                    ranks.append(float('%.2f' %(weekly_rank/counter, )))
                    dates.append(stat.get_date())
                    all_visits.append(weekly_visits)
                    all_sales.append(weekly_sales)
                    current_week = week
                    counter = 1
                    weekly_money, weekly_price, weekly_rank, weekly_visits, weekly_sales = 0, 0, 0, 0, 0
                    continue
                if self.brand == 'All weekly':
                    weekly_money += float('%.2f' %(stat.get_money()/10,))
                weekly_price += float('%.2f' %(stat.get_price()/10,))
                weekly_rank += stat.get_rank()
                weekly_visits += stat.get_visits()
                weekly_sales += stat.get_sales()
                counter += 1
        else:
            for stat in stats:
                if stat.is_weekend():
                    continue
                if self.brand == 'All':
                    money.append(float('%.2f' %(stat.get_money()/10,)))
                prices.append(float('%.2f' %(stat.get_price()/10,)))
                ranks.append(stat.get_rank())
                dates.append(stat.get_date())
                all_visits.append(stat.get_visits())
                all_sales.append(stat.get_sales())
        
        data = { 'title' : '"' + title + '"',
                 'dates' : dates,
                 'prices' : prices,
                 'ranks' : ranks,
                 'sales' : all_sales, 
                 'visits' : all_visits,
                 'dates' : dates,
                 'money' : money,
                 }
        return render_to_string('admin/graph/overviewgraph/chart.html', data )
    chart.allow_tags = True
    
    def week_chart(self):
        stats = OverviewStat.objects.filter(graph=self.pk).order_by('date')
        title = self.__unicode__().capitalize() + ' Statistics'
        prices = []
        ranks = []
        all_sales = []
        all_visits = []
        dates = []
        money = []
        if 'weekly' in self.brand:
            current_week = stats[0].date.isocalendar()[1]
            weekly_money, weekly_price, weekly_rank, weekly_visits, weekly_sales = 0, 0, 0, 0, 0
            for stat in stats:
                week = stat.date.isocalendar()[1]
                counter = 1
                if week != current_week:
                    if 'All' in self.brand:
                        money.append(weekly_money)
                    prices.append(float('%.2f' %(weekly_price/counter, )))
                    ranks.append(float('%.2f' %(weekly_rank/counter, )))
                    dates.append(stat.get_date())
                    all_visits.append(weekly_visits)
                    all_sales.append(weekly_sales)
                    current_week = week
                    counter = 1
                    weekly_money, weekly_price, weekly_rank, weekly_visits, weekly_sales = 0, 0, 0, 0, 0
                if 'All' in self.brand:
                    weekly_money += float('%.2f' %(stat.get_money()/10,))
                weekly_price = float('%.2f' %(stat.get_price()/10,))
                weekly_rank += stat.get_rank()
                weekly_visits += stat.get_visits()
                weekly_sales = stat.get_sales()
            
            data = { 'title' : '"' + title + '"',
                     'dates' : dates,
                     'prices' : prices,
                     'ranks' : ranks,
                     'sales' : all_sales, 
                     'visits' : all_visits,
                     'dates' : dates,
                     'money' : money,
                     }
        return render_to_string('admin/graph/overviewgraph/chart.html', data )
    week_chart.allow_tags = True


class OverviewStat(models.Model):
    graph = models.ForeignKey(OverviewGraph)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    rank = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    visits = models.IntegerField(default=0)
    sales = models.IntegerField(default=0)
    money = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    date = models.DateField('date last updated', default=datetime.date.today)

    class Meta:
        unique_together = ("graph", "date")
    
    def get_price(self):
        return float(self.price)
    
    def get_rank(self):
        return float(self.rank)
    
    def get_date(self):
        return self.date.strftime("%Y-%m-%d")
    
    def is_weekend(self):
        if self.date.weekday()==5 or self.date.weekday()==6:
            return True
        return False
    
    def get_sales(self):
        return int(self.sales)
    
    def get_visits(self):
        return int(self.visits)

    def get_money(self):
        return float(self.money)
    
    def __unicode__(self):
        return self.get_date() + ' ' + str(self.graph)
    
    def update_price(self):
        brand_name = self.graph.brand.lower()
        if brand_name == 'all':
            all_products = Product.objects.all().count()
            cheaper_results = Product.objects.all().filter(is_cheaper=True).count()
        else:
            all_products = Product.objects.filter(brand__name=brand_name).count()
            cheaper_results = Product.objects.filter(brand__name=brand_name,
                                                is_cheaper=True).count()
        ratio = 100 - float(cheaper_results)/float(all_products) * 100
        print 'market share', brand_name, ratio
        self.price = '%.2f' %ratio
        
    def update_visits(self, date=datetime.date.today()):
        brand_name = self.graph.brand.lower()
        scraper = ClickyScraper()
        visits = scraper.brand_visits(brand_name, date)
        print 'visits', brand_name, visits
        self.visits = visits
        
    def update_rank(self, date=datetime.date.today()):
        brand_name = self.graph.brand.lower()
        scraper = RankScraper()
        rank = scraper.get_rank(brand_name)
        print 'rank', brand_name, rank
        if rank:
            self.rank = float(rank)
        
        
    def update_sales(self, date=datetime.date.today()):
        brand_name = self.graph.brand.lower()
        scraper = OrderScraper()
        sales = scraper.get_sales(brand_name, date)
        print 'sales', brand_name, sales
        self.sales = sales
    
    def update_money(self, date=datetime.date.today()):
        brand_name = self.graph.brand.lower()
        scraper = CashScraper()
        sales = scraper.get_money(date)
        print 'sales', brand_name, sales
        self.money = sales