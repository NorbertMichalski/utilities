# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'UploadProduct.url'
        db.alter_column(u'tools_uploadproduct', 'url', self.gf('django.db.models.fields.URLField')(max_length=150))

    def backwards(self, orm):

        # Changing field 'UploadProduct.url'
        db.alter_column(u'tools_uploadproduct', 'url', self.gf('django.db.models.fields.URLField')(max_length=200))

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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '150', 'blank': 'True'})
        },
        u'tools.uploadproduct': {
            'Meta': {'object_name': 'UploadProduct'},
            'csv_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '150', 'blank': 'True'})
        }
    }

    complete_apps = ['tools']