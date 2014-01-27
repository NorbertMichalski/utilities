# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UploadProduct.successfully_updated'
        db.add_column(u'tools_uploadproduct', 'successfully_updated',
                      self.gf('django.db.models.fields.IntegerField')(default=0, blank=True),
                      keep_default=False)

        # Adding field 'UploadProduct.failed_entries'
        db.add_column(u'tools_uploadproduct', 'failed_entries',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'UpdatePrice.successfully_updated'
        db.add_column(u'tools_updateprice', 'successfully_updated',
                      self.gf('django.db.models.fields.IntegerField')(default=0, blank=True),
                      keep_default=False)

        # Adding field 'UpdatePrice.failed_entries'
        db.add_column(u'tools_updateprice', 'failed_entries',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'UploadProduct.successfully_updated'
        db.delete_column(u'tools_uploadproduct', 'successfully_updated')

        # Deleting field 'UploadProduct.failed_entries'
        db.delete_column(u'tools_uploadproduct', 'failed_entries')

        # Deleting field 'UpdatePrice.successfully_updated'
        db.delete_column(u'tools_updateprice', 'successfully_updated')

        # Deleting field 'UpdatePrice.failed_entries'
        db.delete_column(u'tools_updateprice', 'failed_entries')


    models = {
        u'tools.proxy': {
            'Meta': {'object_name': 'Proxy'},
            'address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'tools.updateprice': {
            'Meta': {'object_name': 'UpdatePrice'},
            'csv_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'failed_entries': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'successfully_updated': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '150', 'blank': 'True'})
        },
        u'tools.uploadproduct': {
            'Meta': {'object_name': 'UploadProduct'},
            'csv_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'failed_entries': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'successfully_updated': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '150', 'blank': 'True'})
        }
    }

    complete_apps = ['tools']