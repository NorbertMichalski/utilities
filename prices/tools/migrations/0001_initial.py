# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Proxy'
        db.create_table(u'tools_proxy', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('port', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'tools', ['Proxy'])

        # Adding model 'QuickScan'
        db.create_table(u'tools_quickscan', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('search_brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prices.Brand'])),
            ('search_product', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'tools', ['QuickScan'])


    def backwards(self, orm):
        # Deleting model 'Proxy'
        db.delete_table(u'tools_proxy')

        # Deleting model 'QuickScan'
        db.delete_table(u'tools_quickscan')


    models = {
        u'prices.brand': {
            'Meta': {'object_name': 'Brand'},
            'competitor': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['prices.Competitor']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'prices.competitor': {
            'Meta': {'object_name': 'Competitor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_scrap': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'tools.proxy': {
            'Meta': {'object_name': 'Proxy'},
            'address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'tools.quickscan': {
            'Meta': {'object_name': 'QuickScan'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'search_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['prices.Brand']"}),
            'search_product': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['tools']