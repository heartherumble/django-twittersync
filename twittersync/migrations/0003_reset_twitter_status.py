# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

from twittersync.models import TwitterStatus

class Migration(DataMigration):

    def forwards(self, orm):
        for status in TwitterStatus.objects.all():
            status.save(force_update=True)


    def backwards(self, orm):
        for status in TwitterStatus.objects.all():
            status.published = True
            status.save()


    models = {
        'twittersync.twitteraccount': {
            'Meta': {'ordering': "('screen_name',)", 'object_name': 'TwitterAccount'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'twittersync.twitterstatus': {
            'Meta': {'ordering': "('-created_date',)", 'object_name': 'TwitterStatus'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tweets'", 'to': "orm['twittersync.TwitterAccount']"}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'status_id': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['twittersync']
