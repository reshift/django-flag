from django.conf.urls.defaults import patterns, include, url
from flag.views import *

urlpatterns = patterns('',    
  url(r'^submit/$', 'flag.views.submit', name = 'flag-submit'),
)