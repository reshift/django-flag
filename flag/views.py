from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.contenttypes.models import ContentType
from flag.models import *
from flag.forms import *
from django.contrib.auth.models import User
from django.utils import simplejson
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.forms.models import model_to_dict
from django.template.loader import render_to_string
from django.views.generic import ListView

@csrf_protect
@require_POST
def submit(request):
  '''
  The submissions of flag forms will be handled here.
  '''
  success = False
  
  if 'ftypes_dict' in request.POST :
    flag_form = FlagMultiForm(request)
  else:
    flag_form = FlagForm(request)

  if flag_form.is_valid():
    flag = flag_form.save()
    success = True
    redirect = request.REQUEST.get('next', request.META.get('HTTP_REFERER'))  
  else:
    redirect = '/'
    
  if not request.is_ajax() or request.POST.get('ajax', False):
    return HttpResponseRedirect(redirect)
  else:
    data = {}
    '''
    data['success'] = str(success)
    data['ftype'] = model_to_dict(ftype)
    
    if flag is not None:
      data['object'] = model_to_dict(flag)
    '''
    
    return HttpResponse(simplejson.dumps(data), mimetype='application/javascript')
    #return HttpResponse(render_to_string('flag/form.html', context_instance=RequestContext(request)))

def flag(request, action=None, ftype=None):  
  success = False

  # Get our values
  if request.method == 'POST':
    data = request.POST.copy()
  else:
    data = request.GET.copy()
  
  # Load type
  ctype = ContentType.objects.get(id=data['content_type'])
  
  # Get Flag Type
  ftype = FlagType.objects.get(slug=ftype)
  
  # Build our query filter
  kwargs = {
    'content_type': ctype,
    'object_pk': data['object_pk'],
    'ftype': ftype,
  }
  
  kwargs['user'] = request.user
  #kwargs['user'] = User.objects.get(id=1) # test
  
  # Execute, either set a flag or remove it
  if action == "flag":
    try:
      flag = Flag.objects.get_or_create(**kwargs)
      success = True 
    except Flag.DoesNotExist:
      success = False
      
  elif action == "unflag":
    try:
      flag = Flag.objects.get(**kwargs)
      flag.delete()
      success = True
    except Flag.DoesNotExist:
      pass

  if(request.is_ajax()):
    data = {}
    data['success'] = str(success)
    data['ftype'] = model_to_dict(ftype)
    return HttpResponse(simplejson.dumps(data), content_type="text/javascript")
  else:
    next = data.get("next", request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(next)