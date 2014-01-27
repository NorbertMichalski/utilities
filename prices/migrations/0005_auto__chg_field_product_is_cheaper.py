# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Product.is_cheaper'
        db.alter_column(u'prices_product', 'is_cheaper', self.gf('django.db.models.fields.BooleanField')())

    def backwards(self, orm):

        # Changing field 'Product.is_cheaper'
        db.alter_column(u'prices_product', 'is_cheaper', self.gf('django.db.models.fields.NullBooleanField')(null=True))

    models = {
        u'prices.archive': {
            'Meta': {'object_name': 'Archive'},
            'competitor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['prices.Competitor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '2'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['prices.Product']"}),
            'scraped': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'})
        },
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
        u'prices.product': {
            'Meta': {'ordering': "['mro_id']", 'unique_together': "(('mro_id', 'part_number'),)", 'object_name': 'Product'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['prices.Brand']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_cheaper': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mro_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'mro_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '2'}),
            'part_number': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'})
        },
        u'prices.result': {
            'Meta': {'object_name': 'Result'},
            'changed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'competitor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['prices.Competitor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_cheaper': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '2'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['prices.Product']"}),
            'scraped': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'})
        }
    }

    complete_apps = ['prices']