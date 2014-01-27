# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'OverviewStat.money'
        db.add_column(u'graph_overviewstat', 'money',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=2),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'OverviewStat.money'
        db.delete_column(u'graph_overviewstat', 'money')


    models = {
        u'graph.overviewgraph': {
            'Meta': {'ordering': "['id']", 'object_name': 'OverviewGraph'},
            'brand': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'graph.overviewstat': {
            'Meta': {'object_name': 'OverviewStat'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'graph': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['graph.OverviewGraph']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'money': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '2'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '6', 'decimal_places': '2'}),
            'rank': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'}),
            'sales': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'visits': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['graph']