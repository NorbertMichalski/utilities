# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OverviewGraph'
        db.create_table(u'graph_overviewgraph', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brand', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal(u'graph', ['OverviewGraph'])

        # Adding model 'OverviewStat'
        db.create_table(u'graph_overviewstat', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('graph', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['graph.OverviewGraph'])),
            ('price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=6, decimal_places=2)),
            ('rank', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=5, decimal_places=2)),
            ('visits', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('sales', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal(u'graph', ['OverviewStat'])


    def backwards(self, orm):
        # Deleting model 'OverviewGraph'
        db.delete_table(u'graph_overviewgraph')

        # Deleting model 'OverviewStat'
        db.delete_table(u'graph_overviewstat')


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
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '6', 'decimal_places': '2'}),
            'rank': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'}),
            'sales': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'visits': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['graph']