from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template.loader import render_to_string
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
from django.views.decorators.cache import never_cache
from flag.utils import generate_unflag_url, generate_flag_url
import hashlib

@login_required
@never_cache
def flag(request, ftype, ct, pk, token, action=None):
  success = False

  if request.method == 'POST':
    data = request.POST.copy()
  else:
    data = request.GET.copy()
    
  # Security check
  token_check = hashlib.md5(settings.SECRET_KEY + str(ct) + str(pk)).hexdigest()
  
  response = data.get('response', 'json')

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
  if action == "flag":
    try:
      flag = Flag.objects.get_or_create(**kwargs)
      success = True
      state = 'flagged'
    except Flag.DoesNotExist:
      success = False
      
  elif action == "unflag":
    try:
      flag = Flag.objects.get(**kwargs)
      flag.delete()
      success = True
      state = 'unflagged'
    except Flag.DoesNotExist:
      state = 'unflagged'
  
  # Add some extra info
  ftype.unflag_url = generate_unflag_url(user=request.user, obj=flag.content_object, ftype=ftype.slug)
  ftype.flag_url = generate_flag_url(user=request.user, obj=flag.content_object, ftype=ftype.slug)
 
  if(request.is_ajax()):
    if response == 'html':
      output = render_to_string('flag/flag.html', {'user': request.user, 'flag': ftype}, context_instance=RequestContext(request))
      return HttpResponse(output)
    else:  
      data = {}
      data['success'] = str(success)
      data['state'] = str(state)
      data['ftype'] = model_to_dict(ftype)
      return HttpResponse(simplejson.dumps(data), content_type="text/javascript")
  else:
    next = data.get("next", request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(next)