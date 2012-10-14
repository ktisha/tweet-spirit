from django.conf.urls.defaults import patterns, include, url
from site_part.tweet_spirit.views import search, search_response

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


urlpatterns = patterns('',
    ('^search/$', search),
    ('^search/test*$', search_response),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':'./media/'}),
)
