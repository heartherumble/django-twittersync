from django.conf import settings
from django import template
from twittersync.models import TwitterAccount, TwitterStatus

register = template.Library()


class LatestTweets(template.Node):
    def __init__(self, account, limit, varname):
        self.account = account
        self.limit = limit
        self.varname = varname

    def render(self, context):
        def resolve_or_not(var, context):
            if callable(getattr(var, 'resolve', None)):
                return var.resolve(context)
            return var

        account = resolve_or_not(self.account, context)
        limit = resolve_or_not(self.limit, context)
        varname = resolve_or_not(self.varname, context)

        if not isinstance(account, TwitterAccount):
            try:
                account = TwitterAccount.objects.get(screen_name=account)
            except TwitterAccount.DoesNotExist:
                raise

        context[varname] = account.tweets.all()[:int(limit)]
        return u''


@register.tag
def get_latest_tweets(parser, token):
    ''' Returns the latest tweets stored in the db.

        Run like so:

        {% get_latest_tweets twitter_account_instance 5 as tweets %}

        Will return the last 5 tweets and store in the 
        template context as "tweets"..

        You can also exclude the number requested and 
        the tag will return the value set in 
        settings.TWITTERSYNC_LATEST_TWEETS. If that 
        isn't set, we fall back to 5
    '''
    bits = token.split_contents()
    if len(bits) < 4:
        raise template.TemplateSyntaxError(
            '"%s" tag takes at least 3 arguments' % bits[0]
        )

    limit = None
    try:
        _tag, account, limit, _as, varname = bits
    except ValueError:
        _tag, account, _as, varname = bits

    if limit is None:
        limit = getattr(settings, 'TWITTERSYNC_LATEST_TWEETS', 5)

    try:
        # needed because it may not be passed via the 
        # template token.
        limit = parser.compile_filter(limit)
    except TypeError:
        pass

    return LatestTweets(
        parser.compile_filter(account),
        limit,
        parser.compile_filter(varname),
    )
