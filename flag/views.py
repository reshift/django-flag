from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.contenttypes.models import ContentType
from flag.models import *
from django.contrib.auth.models import User
from django.utils import simplejson
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.template.loader import render_to_string
from django.views.generic import ListView
import md5

@login_required
def flag(request, ftype, ct, pk, token, action=None):
  success = False

  if request.method == 'POST':
    data = request.POST.copy()
  else:
    data = request.GET.copy()
    
  # Security check
  token_check = md5.new(settings.SECRET_KEY + str(ct) + str(pk)).hexdigest()

  if token_check != token:
    return HttpResponseForbidden()
  
  # Load type
  ctype = ContentType.objects.get(id=ct)
  
  # Get Flag Type
  ftype = FlagType.objects.get(slug=ftype)
  
  # Build our query filter
  kwargs = {
    'content_type': ctype,
    'object_pk': pk,
    'ftype': ftype,
  }
  
  kwargs['user'] = request.user
  
  # Execute, either set a flag or remove it
  #print action
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