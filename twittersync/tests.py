from django.conf import settings
from django.utils import unittest
from django.test.client import Client

from twittersync.helpers import TwitterSyncHelper
from twittersync.models import TwitterAccount, TwitterStatus


class MockResponse(object):
    def __init__(self, status, data=None):
        self.status = status
        self.code = status
        self.data = data

    def info(self):
        return self

    def read(self):
        if self.data is None:
            return ''
        data, self.data = self.data, None
        return data


class TestBase(unittest.TestCase):
    def setUp(self):
        self._old_send_request = TwitterSyncHelper.send_request
        TwitterSyncHelper.send_request = self._send_request
        self.client = Client()
        self.responses = []
        self.requests = []

    def tearDown(self):
        TwitterSyncHelper.send_request = self._old_send_request

    def _send_request(self, latest=None):
        self.requests.append((latest,))
        return self.responses.pop()


class TwitterSyncTest(TestBase):
    def test_new_tweets(self):
        # Taken from http://dev.twitter.com/console
        tweet_json = '''[
  {
    "coordinates": null,
    "favorited": false,
    "created_at": "Tue Nov 09 20:42:19 +0000 2010",
    "truncated": false,
    "id_str": "2098682128244736",
    "in_reply_to_user_id_str": null,
    "text": "Loonnnggggg day!",
    "contributors": null,
    "id": 2098682128244736,
    "in_reply_to_status_id_str": null,
    "retweet_count": null,
    "geo": null,
    "retweeted": false,
    "in_reply_to_user_id": null,
    "in_reply_to_screen_name": null,
    "user": {
      "profile_background_tile": false,
      "name": "Peter Sanchez",
      "profile_sidebar_border_color": "C6E2EE",
      "profile_sidebar_fill_color": "DAECF4",
      "profile_image_url": "http:\/\/a0.twimg.com\/profile_images\/67635284\/img1_normal.jpg",
      "location": "Los Angeles, CA",
      "created_at": "Thu Apr 17 17:51:56 +0000 2008",
      "follow_request_sent": false,
      "id_str": "14423585",
      "profile_link_color": "1F98C7",
      "favourites_count": 0,
      "url": "http:\/\/www.petersanchez.com",
      "contributors_enabled": false,
      "utc_offset": -28800,
      "id": 14423585,
      "listed_count": 10,
      "profile_use_background_image": true,
      "profile_text_color": "663B12",
      "protected": false,
      "followers_count": 4771,
      "lang": "en",
      "notifications": false,
      "profile_background_color": "C6E2EE",
      "time_zone": "Pacific Time (US & Canada)",
      "verified": false,
      "geo_enabled": false,
      "description": "Entrepreneur, Internet Marketer, Software Engineer, Copywriter and Internet Junkie. How do ya like that?",
      "friends_count": 5197,
      "statuses_count": 3,
      "profile_background_image_url": "http:\/\/a1.twimg.com\/profile_background_images\/3271040\/bgimage.jpg",
      "show_all_inline_media": false,
      "following": true,
      "screen_name": "petersanchez"
    },
    "source": "web",
    "place": null,
    "in_reply_to_status_id": null
  },
  {
    "coordinates": null,
    "favorited": false,
    "created_at": "Tue Nov 09 08:04:40 +0000 2010",
    "truncated": false,
    "id_str": "1908014869118976",
    "in_reply_to_user_id_str": null,
    "text": "New Blog Post: NorthWoods Inn - Hallows Eve 2010: On Hallows Eve 2010 I went to dinner at the NorthWoods Inn res... http:\/\/bit.ly\/9VFsEo",
    "contributors": null,
    "id": 1908014869118976,
    "in_reply_to_status_id_str": null,
    "retweet_count": null,
    "geo": null,
    "retweeted": false,
    "in_reply_to_user_id": null,
    "in_reply_to_screen_name": null,
    "user": {
      "profile_background_tile": false,
      "name": "Peter Sanchez",
      "profile_sidebar_border_color": "C6E2EE",
      "profile_sidebar_fill_color": "DAECF4",
      "profile_image_url": "http:\/\/a0.twimg.com\/profile_images\/67635284\/img1_normal.jpg",
      "location": "Los Angeles, CA",
      "created_at": "Thu Apr 17 17:51:56 +0000 2008",
      "follow_request_sent": false,
      "id_str": "14423585",
      "profile_link_color": "1F98C7",
      "favourites_count": 0,
      "contributors_enabled": false,
      "url": "http:\/\/www.petersanchez.com",
      "utc_offset": -28800,
      "id": 14423585,
      "profile_use_background_image": true,
      "listed_count": 10,
      "profile_text_color": "663B12",
      "protected": false,
      "followers_count": 4772,
      "lang": "en",
      "notifications": false,
      "verified": false,
      "profile_background_color": "C6E2EE",
      "geo_enabled": false,
      "time_zone": "Pacific Time (US & Canada)",
      "description": "Entrepreneur, Internet Marketer, Software Engineer, Copywriter and Internet Junkie. How do ya like that?",
      "friends_count": 5197,
      "profile_background_image_url": "http:\/\/a1.twimg.com\/profile_background_images\/3271040\/bgimage.jpg",
      "statuses_count": 2,
      "following": true,
      "show_all_inline_media": false,
      "screen_name": "petersanchez"
    },
    "source": "web",
    "place": null,
    "in_reply_to_status_id": null
  },
  {
    "coordinates": null,
    "favorited": false,
    "created_at": "Tue Nov 09 00:25:36 +0000 2010",
    "truncated": false,
    "id_str": "1792487194632192",
    "in_reply_to_user_id_str": null,
    "text": "I'm in the pursuit of happiness and I know....",
    "contributors": null,
    "id": 1792487194632192,
    "in_reply_to_status_id_str": null,
    "retweet_count": null,
    "geo": null,
    "retweeted": false,
    "in_reply_to_user_id": null,
    "in_reply_to_screen_name": null,
    "user": {
      "profile_background_tile": false,
      "name": "Peter Sanchez",
      "profile_sidebar_border_color": "C6E2EE",
      "profile_sidebar_fill_color": "DAECF4",
      "profile_image_url": "http:\/\/a0.twimg.com\/profile_images\/67635284\/img1_normal.jpg",
      "location": "Los Angeles, CA",
      "created_at": "Thu Apr 17 17:51:56 +0000 2008",
      "follow_request_sent": false,
      "id_str": "14423585",
      "profile_link_color": "1F98C7",
      "favourites_count": 0,
      "contributors_enabled": false,
      "url": "http:\/\/www.petersanchez.com",
      "utc_offset": -28800,
      "id": 14423585,
      "profile_use_background_image": true,
      "listed_count": 10,
      "profile_text_color": "663B12",
      "protected": false,
      "followers_count": 4771,
      "lang": "en",
      "notifications": false,
      "profile_background_color": "C6E2EE",
      "verified": false,
      "geo_enabled": false,
      "time_zone": "Pacific Time (US & Canada)",
      "description": "Entrepreneur, Internet Marketer, Software Engineer, Copywriter and Internet Junkie. How do ya like that?",
      "profile_background_image_url": "http:\/\/a1.twimg.com\/profile_background_images\/3271040\/bgimage.jpg",
      "friends_count": 5197,
      "statuses_count": 3,
      "following": false,
      "show_all_inline_media": false,
      "screen_name": "petersanchez"
    },
    "source": "web",
    "place": null,
    "in_reply_to_status_id": null
  }
]
'''
        # Clear out all tweets first
        TwitterAccount.objects.all().delete()
        TwitterStatus.objects.all().delete()

        account = TwitterAccount.objects.create(
            screen_name='testuser',
            is_active=True,
        )
        self.assertEquals(TwitterAccount.objects.count(), 1)

        self.responses.append(MockResponse(200, data=tweet_json))
        TwitterSyncHelper(account).sync_twitter_account()
        self.assertEquals(TwitterStatus.objects.count(), 3)
