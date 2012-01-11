import datetime
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from twittersync.managers import TwitterAccountManager, TwitterStatusManager


class TwitterAccount(models.Model):
    screen_name = models.CharField(
        _('Twitter Account'),
        max_length=125,
        help_text=_('Screen name of the Twitter account to sync.'),
    )
    is_active = models.BooleanField(
        _('Active?'),
        default=True,
        help_text=_('Mark this account enabled for syncing?'),
    )

    date = models.DateTimeField(_('Date Added'), default=datetime.datetime.now)
    updated = models.DateTimeField(
        _('Last Updated'),
        default=datetime.datetime.now,
    )

    objects = models.Manager()
    active = TwitterAccountManager()

    class Meta:
        ordering = ('screen_name',)
        verbose_name = 'Twitter Account'
        verbose_name_plural = 'Twitter Accounts'
    
    def __unicode__(self):
        return u'Twitter Account: %s' % self.screen_name

    @property
    def twitter_url(self):
        return u'http://twitter.com/%s' % self.screen_name
    
    def save(self, *args, **kwargs):
        if self.id:
            self.updated = datetime.datetime.now()
        super(TwitterAccount, self).save(*args, **kwargs)


class TwitterStatus(models.Model):
    status_id = models.CharField(max_length=50)
    author = models.ForeignKey(TwitterAccount, related_name='tweets')
    content = models.CharField(max_length=255)
   
    created_date = models.DateTimeField(_('Created At'))
    date = models.DateTimeField(default=datetime.datetime.now)

    objects = TwitterStatusManager()

    class Meta:
        get_latest_by = 'created_date'
        ordering = ('-created_date',)
        verbose_name = 'Twitter Status'
        verbose_name_plural = 'Twitter Statuses'

    def __unicode__(self):
        return u'%i' % self.id

    @property
    def url(self):
        return u'http://twitter.com/%s/statuses/%s' % (
                                self.author.screen_name, self.status_id)
