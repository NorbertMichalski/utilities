# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UploadProduct'
        db.create_table(u'tools_uploadproduct', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('csv_file', self.gf('django.db.models.fields.FilePathField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('uploaded_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 2, 0, 0))),
        ))
        db.send_create_signal(u'tools', ['UploadProduct'])

        # Adding model 'UpdatePrice'
        db.create_table(u'tools_updateprice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('csv_file', self.gf('django.db.models.fields.FilePathField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('uploaded_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 2, 0, 0))),
        ))
        db.send_create_signal(u'tools', ['UpdatePrice'])


    def backwards(self, orm):
        # Deleting model 'UploadProduct'
        db.delete_table(u'tools_uploadproduct')

        # Deleting model 'UpdatePrice'
        db.delete_table(u'tools_updateprice')


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
            'csv_file': ('django.db.models.fields.FilePathField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 0, 0)'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'tools.uploadproduct': {
            'Meta': {'object_name': 'UploadProduct'},
            'csv_file': ('django.db.models.fields.FilePathField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 0, 0)'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['tools']