from django.conf.urls.defaults import patterns, include, url
from flag.views import *

urlpatterns = patterns('',    
  url(r'^submit/$', 'flag.views.submit', name = 'flag-submit'),
  url(r'^([a-zA-Z0-9-_]+)/([a-zA-Z0-9-_]+)/$', 'flag.views.flag', name = 'flag-flag'),
)