# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'QuickScan'
        db.delete_table(u'tools_quickscan')


    def backwards(self, orm):
        # Adding model 'QuickScan'
        db.create_table(u'tools_quickscan', (
            ('search_brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prices.Brand'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('search_product', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'tools', ['QuickScan'])


    models = {
        u'tools.proxy': {
            'Meta': {'object_name': 'Proxy'},
            'address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['tools']