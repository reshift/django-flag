from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.contenttypes.models import ContentType
from flag.models import *
from flag.forms import *
from django.utils import simplejson
from django.core import serializers
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.forms.models import model_to_dict

@csrf_protect
@require_POST
def submit(request):
  '''
  The submissions of flag forms will be handled here.
  '''
  #print request.POST.getlist('flags')
  #print request.POST
  form = FlagForm(request)    
  success = False

  if form.is_valid():
    # Get ftype for later reference
    #ftypes = form.instance.ftype
    
    # Delete if flag is not set
    flag = form.save()
      
    success = True
    redirect = request.REQUEST.get('next', request.META.get('HTTP_REFERER'))  
  else:
    print form.errors
    redirect = '/'
    
  if not request.is_ajax() or request.POST.get('ajax', False):
    return HttpResponseRedirect(redirect)
  else:
    data = {}
    data['success'] = str(success)
    data['ftype'] = model_to_dict(ftype)
    
    if flag is not None:
      data['object'] = model_to_dict(flag)

    return HttpResponse(simplejson.dumps(data), mimetype='application/javascript')