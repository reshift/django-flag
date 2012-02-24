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
  form = FlagForm(request)    
  success = False
  
  if form.is_valid():
    # Get ftype for later reference
    ftype = form.instance.ftype
    
    # Delete if instance is found
    if form.instance.id:
      flag = form.instance.delete()
    else:  
      flag = form.save()
      
    success = True
    redirect = request.REQUEST.get('next', request.META.get('HTTP_REFERER'))   
  else: 
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

'''
DEPRICIATED
@csrf_protect
def setFlag(request):
  delete = False
  
  # Get our values
  if request.method == 'POST':
    data = request.POST.copy()
  else:
    data = request.GET.copy()
  
  #if is_valid_access_token(request):
  #  print "valdiated"
  #else:
  #  print "Not valdiated"
  
  # Load type
  ctype = ContentType.objects.get(id=data['content_type'])
  
  # Build our filter
  kwargs = {
    'content_type': ctype,
    'object_pk': data['object_pk'],
    'name': data['name'] 
  }
  
  # Add user to filer
  if 'glob' not in data:
    kwargs['user'] = request.user
  
  # First check if exists otherwise go on and create
  try:
    flag = Flag.objects.get(**kwargs)
    flag.delete()
    delete = True
  except Flag.DoesNotExist:
    flag = Flag(**kwargs)
    flag.save()
    delete = False
  
  if(request.is_ajax()):
    flag = Flag.objects.filter(id=flag.id)
    data = serializers.serialize("json", flag)
    return HttpResponse(data, status=200, content_type="text/javascript")
  else:
    next = data.get("next", request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(next)
'''    