import urllib2
import datetime
from django.conf import settings
from django.http import QueryDict
from django.core.management.base import NoArgsCommand
from twittersync.models import TwitterAccount
from twittersync.helpers import TwitterSyncHelper


class Command(NoArgsCommand):
    help = 'Sync all active Twitter account streams.'

    def handle_noargs(self, **options):
        for account in TwitterAccount.active.all():
            TwitterSyncHelper(account).sync_twitter_account()
