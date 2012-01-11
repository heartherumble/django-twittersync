from django.conf import settings
from django.db import models


class TwitterAccountManager(models.Manager):
    def get_query_set(self):
        qs = super(TwitterAccountManager, self).get_query_set()
        return qs.filter(is_active=True)


class TwitterStatusManager(models.Manager):
    def get_query_set(self):
        qs = super(TwitterStatusManager, self).get_query_set()
        return qs.select_related('author')
