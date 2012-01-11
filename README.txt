django-twittersync
------------------

Very basic application to sync a Twitter account's stream to 
the local storage engine.

There are a few other applications that handle this for you 
but none of them fit my needs, so here we are. The idea behind 
this app is to be very light weight - do one thing and do it well.

There is no need for a Twitter consumer key or token for use with 
this app. It makes use of the public facing (non-auth required) REST 
API. This also means that if the account you are trying to sync is 
setup as private, this app will not sync that account.


Dependencies
------------

This app only depends on the python-dateutil module. You can install 
it like so:

$ sudo pip install python-dateutil

It was written for Python 2.4+ and Django 1.2.3


Install
-------

Basic Install:

  $ python setup.py build
  $ sudo python setup.py install

Alternative Install (Manually):

Place webutils directory in your Python path. Either in your Python 
installs site-packages directory or set your $PYTHONPATH environment 
variable to include a directory where the webutils directory lives.


Use
---
1) Add 'twittersync' to your INSTALLED_APPS

2) Run 'python manage.py syncdb'

3) Add a twitter account via the admin interface

4) Run 'python manage.py sync_twitter_accounts'

There you go. You might want to setup a cron job to run the 
sync_twitter_accounts command (like on step 4) every hour or so.

To display your tweets in a template, simple do something like:

{% load twittersync_tags %}

{% get_latest_tweets "accountname" 5 as "tweets" %}
{% for tweet in tweets %}
  <a href="{{ tweet.url }}">{{ tweet.content }}</a><br />
{% endfor %}

This will grab the last 5 status updated for the twitter account 
"accountname" and place it in the context as the variable named 
"tweets"

Replace "accountname" with the name of the account you want to 
sync. It can be a string or an actual TwitterAccount (model) 
instance.

Replace 5 with the number of updates to fetch. If it's not given 
the template tag will check for the following settings variable:

TWITTERSYNC_LATEST_TWEETS

It will default to 5 if that variable doesn't exist.


That's it! Simple right?

Enjoy.


Copyright & Warranty
--------------------
All documentation, libraries, and sample code are 
Copyright 2010 Peter Sanchez <petersanchez@gmail.com>. The library and 
sample code are made available to you under the terms of the BSD license 
which is contained in the included file, BSD-LICENSE.
