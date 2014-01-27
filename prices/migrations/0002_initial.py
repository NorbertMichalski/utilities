# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Competitor'
        db.create_table(u'prices_competitor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_scrap', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal(u'prices', ['Competitor'])

        # Adding model 'Brand'
        db.create_table(u'prices_brand', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'prices', ['Brand'])

        # Adding M2M table for field competitor on 'Brand'
        m2m_table_name = db.shorten_name(u'prices_brand_competitor')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('brand', models.ForeignKey(orm[u'prices.brand'], null=False)),
            ('competitor', models.ForeignKey(orm[u'prices.competitor'], null=False))
        ))
        db.create_unique(m2m_table_name, ['brand_id', 'competitor_id'])

        # Adding model 'Product'
        db.create_table(u'prices_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prices.Brand'])),
            ('mro_id', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('part_number', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('mro_price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=2)),
            ('updated', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal(u'prices', ['Product'])

        # Adding unique constraint on 'Product', fields ['mro_id', 'part_number']
        db.create_unique(u'prices_product', ['mro_id', 'part_number'])

        # Adding model 'Result'
        db.create_table(u'prices_result', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prices.Product'])),
            ('competitor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prices.Competitor'])),
            ('price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=2)),
            ('scraped', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal(u'prices', ['Result'])

        # Adding model 'Archive'
        db.create_table(u'prices_archive', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prices.Product'])),
            ('competitor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prices.Competitor'])),
            ('price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=2)),
            ('scraped', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal(u'prices', ['Archive'])


    def backwards(self, orm):
        # Removing unique constraint on 'Product', fields ['mro_id', 'part_number']
        db.delete_unique(u'prices_product', ['mro_id', 'part_number'])

        # Deleting model 'Competitor'
        db.delete_table(u'prices_competitor')

        # Deleting model 'Brand'
        db.delete_table(u'prices_brand')

        # Removing M2M table for field competitor on 'Brand'
        db.delete_table(db.shorten_name(u'prices_brand_competitor'))

        # Deleting model 'Product'
        db.delete_table(u'prices_product')

        # Deleting model 'Result'
        db.delete_table(u'prices_result')

        # Deleting model 'Archive'
        db.delete_table(u'prices_archive')


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
            'mro_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'mro_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '2'}),
            'part_number': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'})
        },
        u'prices.result': {
            'Meta': {'object_name': 'Result'},
            'competitor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['prices.Competitor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '2'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['prices.Product']"}),
            'scraped': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'})
        }
    }

    complete_apps = ['prices']