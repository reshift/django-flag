from django.conf.urls.defaults import patterns, include, url
from flag.views import *

urlpatterns = patterns('',    
  url(r'^submit/$', 'flag.views.submit', name = 'flag-submit'),
  url(r'^flag/(?P<ftype>[a-zA-Z0-9-_]+)/(?P<ct>\d+)/(?P<pk>[^\/]+)/(?P<token>[a-zA-Z0-9-_]+)/$', 'flag.views.flag', {'action': 'flag'}, name='flag_flag'),
  url(r'^unflag/(?P<ftype>[a-zA-Z0-9-_]+)/(?P<ct>\d+)/(?P<pk>[^\/]+)/(?P<token>[a-zA-Z0-9-_]+)/$', 'flag.views.flag', {'action': 'unflag'}, name='flag_unflag'),
)