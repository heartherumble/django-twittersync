import urllib2
import datetime
import twittersync
from django.conf import settings
from django.http import QueryDict
from dateutil.parser import parse
from twittersync.models import TwitterAccount, TwitterStatus

# Switch to AnyJson?
try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        from django.utils import simplejson as json


version = twittersync.__version__

class TwitterSyncHelper(object):
    def __init__(self, account):
        self.account = account

    def build_url(self, qdict):
        return 'http://api.twitter.com/1/statuses/user_timeline.json?%s' % \
                                                              qdict.urlencode()

    def send_request(self, latest=None):
        qdict = QueryDict('', mutable=True)
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'django-twittersync/%s' % version)]
        qdict['screen_name'] = self.account.screen_name
        qdict['trim_user'] = 'true'
     
        if latest is not None:
            qdict['since_id'] = latest.status_id

        return opener.open(self.build_url(qdict))

    def _get_proper_date(self, c_date):
        ''' Stupid helper to work around MySQL not able to 
            handle timezones.
            Ref: https://docs.djangoproject.com/en/1.3/ref/databases/#datetime-fields
            XXX: Find a proper fix! Maybe just catch ValueError ?
        '''
        dbs = [x['ENGINE'].split('.')[-1] for x in settings.DATABASES.values()]
        if 'mysql' in dbs:
            return datetime.datetime.now()
        return c_date

    def save_status_update(self, result):
        return TwitterStatus.objects.get_or_create(
            status_id=result['id_str'],
            author=self.account,
            content=result['text'],
            created_date=self._get_proper_date(parse(result['created_at'])),
        )

    def sync_twitter_account(self):
        # If previous updates exist, only get newer tweets
        try:
            latest = self.account.tweets.latest()
        except TwitterStatus.DoesNotExist:
            latest = None

        try:
            res = self.send_request(latest)
        except urllib2.HTTPError:
            # Twitter often gives 503 errors when the 
            # API is overwhelmed.
            pass
        else:
            results = json.load(res)
            for result in results:
                self.save_status_update(result)
