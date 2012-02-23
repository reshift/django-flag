from django.conf.urls.defaults import patterns, include, url
from flag.views import *

urlpatterns = patterns('flag.views',    
  url(r'flag/set_flag', 'setFlag'),
)
