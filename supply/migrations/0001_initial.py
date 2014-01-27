# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Brand'
        db.create_table(u'supply_brand', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'supply', ['Brand'])

        # Adding model 'Location'
        db.create_table(u'supply_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['supply.Brand'])),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('city_state', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('zip', self.gf('django.db.models.fields.CharField')(default='', max_length=10)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('phone', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('timezone', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('timediff', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2)),
        ))
        db.send_create_signal(u'supply', ['Location'])

        # Adding model 'Product'
        db.create_table(u'supply_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['supply.Brand'])),
            ('mro_id', self.gf('django.db.models.fields.IntegerField')()),
            ('part_number', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('weight', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=7, decimal_places=2)),
            ('updated', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal(u'supply', ['Product'])


    def backwards(self, orm):
        # Deleting model 'Brand'
        db.delete_table(u'supply_brand')

        # Deleting model 'Location'
        db.delete_table(u'supply_location')

        # Deleting model 'Product'
        db.delete_table(u'supply_product')


    models = {
        u'supply.brand': {
            'Meta': {'object_name': 'Brand'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'supply.location': {
            'Meta': {'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['supply.Brand']"}),
            'city_state': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'phone': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'timediff': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'zip': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'})
        },
        u'supply.product': {
            'Meta': {'object_name': 'Product'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['supply.Brand']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mro_id': ('django.db.models.fields.IntegerField', [], {}),
            'part_number': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'weight': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '2'})
        }
    }

    complete_apps = ['supply']