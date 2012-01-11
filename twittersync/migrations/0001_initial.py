# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TwitterAccount'
        db.create_table('twittersync_twitteraccount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('screen_name', self.gf('django.db.models.fields.CharField')(max_length=125)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('twittersync', ['TwitterAccount'])

        # Adding model 'TwitterStatus'
        db.create_table('twittersync_twitterstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tweets', to=orm['twittersync.TwitterAccount'])),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('twittersync', ['TwitterStatus'])


    def backwards(self, orm):
        
        # Deleting model 'TwitterAccount'
        db.delete_table('twittersync_twitteraccount')

        # Deleting model 'TwitterStatus'
        db.delete_table('twittersync_twitterstatus')


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
            'status_id': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['twittersync']
