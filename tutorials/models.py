from django.db import models
from django.core import urlresolvers
from utilities.settings import MEDIA_ROOT
import requests
import os

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=200)
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Edit Tutorials"
    
    def __unicode__(self):
        return self.category_name
    
    def number_tutorials(self):
        no_steps = Tutorial.objects.filter(category=self).count()
        return no_steps
    
    def tutorials_contained(self):
        titles = []
        links = []
        results = []
        lessons = Tutorial.objects.filter(category=self)
        for lesson in lessons:
            links.append(lesson.get_changeform_url())
            titles.append(lesson.tutorial_title)
        for title, link in zip(titles, links):
            #result = '<a href="%s" target="_blank">%s</a>' %(link, title)
            result = '<li><a href="%s" target="_blank"><b style="font-size:12px;">%s</b></a></li>' %(link, title)
            results.append(result)
        wrapper = '<ul>%s</ul>' %(''.join(results),)
        return wrapper
    tutorials_contained.allow_tags = True
    
    #customize the output for the view table
    def category(self):
        return '<b>%s</b>' %self.category_name
    category.allow_tags = True
    
class Tutorial(models.Model):
    tutorial_title = models.CharField(max_length=200)
    category = models.ForeignKey(Category)
    order_number = models.IntegerField(max_length=3)
    
    class Meta:
        ordering = ['category', 'order_number']
        unique_together = ('category', 'order_number')
    
    def __unicode__(self):
        return self.tutorial_title
    
    def number_steps(self):
        no_steps = Step.objects.filter(tutorial=self).count()
        return no_steps
    
    def get_category(self):
        return self.category
    
    # get the change link of the current object
    def get_changeform_url(self):
        if self.id:
            # Replace "myapp" with the name of the app containing
            # your Certificate model:
            changeform_url = urlresolvers.reverse(
                'admin:tutorials_tutorial_change', args=(self.id,)
            )
            return changeform_url
        return ''
    
    # customize the link
    def changeform_link(self):
        changeform_url = self.get_changeform_url()
        return u'<a href="%s" target="_blank">Edit the content of this tutorial</a>' % changeform_url
    changeform_link.allow_tags = True
    changeform_link.short_description = 'Link to corresponding tutorial'   # omit column header

    def save(self):
        pass
        super(Tutorial, self).save()

class Step(models.Model):
    tutorial = models.ForeignKey(Tutorial)
    image = models.ImageField(upload_to='tutorials', blank = True, null=True)
    image_url = models.URLField(max_length=200, blank = True, null=True)
    caption = models.CharField(max_length=300)
    notes = models.TextField(blank = True, null=True)
    
    def step_image(self):
        return image_url + ' ' + image
    
    def __unicode__(self):
        return self.caption
    
    def save(self):
        if self.download_image():
            self.image = self.download_image()
        super(Step, self).save()
    
    def download_image(self):
        if not self.image_url:
            return
        try:
            image_file_name = self.image_url.split('/')[-1]
        except Exception as e:
            print e
            return
        image_path = MEDIA_ROOT + 'tutorials/' + image_file_name
        print image_path
        if not os.path.exists(image_path):
            r = requests.get(self.image_url)
            if r.status_code == 200:
                with open(image_path, 'wb') as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
        return image_path
        
# the proxy models used to fake our admin views    
class TutorialView(Tutorial):
    class Meta:
        proxy = True
        verbose_name = "Tutorial"
        verbose_name_plural = "View Tutorials"
        ordering = ['category', 'order_number']
        
    # get the change link of the current object
    def get_changeform_url(self):
        if self.id:
            # Replace "myapp" with the name of the app containing
            # your Certificate model:
            changeform_url = urlresolvers.reverse(
                'admin:tutorials_tutorialview_change', args=(self.id,)
            )
            return changeform_url
        return ''
    
    # customize the link
    def changeform_link(self):
        changeform_url = self.get_changeform_url()
        return u'<a href="%s" target="_blank">View the content of this tutorial</a>' % changeform_url
    changeform_link.allow_tags = True
    changeform_link.short_description = 'Link to view corresponding tutorial'   # omit column header
    
class StepView(Step):
    class Meta:
        proxy = True
    
class CategoryView(Category):
    class Meta:
        proxy = True
        verbose_name = "Tutorial"
        verbose_name_plural = "View Tutorials"
    
    # output in one td a list with all the category's tutorials
    def tutorials_contained(self):
        titles = []
        links = []
        results = []
        lessons = TutorialView.objects.filter(category=self)
        for lesson in lessons:
            links.append(lesson.get_changeform_url())
            titles.append(lesson.tutorial_title)
        for title, link in zip(titles, links):
            #result = '<a href="%s" target="_blank"><b style="font-size:12px;">%s</b></a><br>' %(link, title)
            result = '<li><a href="%s" target="_blank"><b style="font-size:12px;">%s</b></a></li>' %(link, title)
            results.append(result)
        #return ''.join(results)
        wrapper = '<ul>%s</ul>' %(''.join(results),)
        return wrapper
    tutorials_contained.allow_tags = True
    
