from django.conf import settings
from django.contrib import admin
from twittersync.models import TwitterAccount, TwitterStatus


class TwitterAccountAdmin(admin.ModelAdmin):
    list_display = ('screen_name', 'account_url', 'date', 'is_active',)
    list_editable = ('is_active',)
    fields = ('screen_name', 'is_active',)

    def account_url(self, obj):
        return obj.twitter_url
    account_url.short_description = 'Twitter URL'


class TwitterStatusAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'created_date',)
    fields = ('author', 'status_id', 'content', 'created_date', 'date')
    readonly_fields = (
        'author', 'status_id', 'content', 'created_date', 'date',
    )

    def has_add_permission(self, *args, **kw):
        return False


admin.site.register(TwitterAccount, TwitterAccountAdmin)
admin.site.register(TwitterStatus, TwitterStatusAdmin)
