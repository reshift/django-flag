from django import template
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib import comments
from django.utils.encoding import smart_unicode
from flag.models import *
from django.core.urlresolvers import reverse
import md5

register = template.Library()

@register.assignment_tag
def flag(ftype, *args, **kwargs):
  '''
    {% flag type user=user obj=obj as flag %}
  '''
  user = kwargs.get('user', None)
  obj = kwargs['obj']

  ftype = FlagType.objects.filter(slug=ftype)[0]
  ftype.unflag_url = generate_unflag_url(user=user, obj=obj, ftype=ftype)
  ftype.flag_url = generate_flag_url(user=user, obj=obj, ftype=ftype)
  #flag = ftype.flags.filter_by_obj_user(obj=obj, user=user)[0]
  # Check if flag is set
  #flag = Flag.objects.filter_by_obj_user(user=user, obj=obj, ftype=ftype)
  try:
    flag = ftype.flags.filter_by_obj_user(obj=obj, user=user)[0]
    ftype.set = True
  except:
    ftype.set = True

  return ftype

@register.assignment_tag
def get_flags(ftype, *args, **kwargs):
  '''
    {% get_flags type user=user as flags %}
  '''
  user = kwargs.get('user', None)
  #obj = kwargs.get('obj', None)

  ftype = FlagType.objects.filter(slug=ftype)[0]

  if user:
    flags = Flag.objects.filter(user=user, ftype=ftype)

  return flags

@register.simple_tag(takes_context=True)
def is_flagged(context, obj, ftype):
  """
  Returns whether or not the user has flagged the given object
  """
  flag = Flag.objects.filter_by_obj_user(user=context['request'].user, obj=obj, ftype__slug=ftype)
  return len(flag) == 1

@register.simple_tag(takes_context=True)
def flag_url(context, obj, ftype):
  return generate_unflag_url(ftype=ftype, user=context['request'].user, obj=obj)

@register.simple_tag(takes_context=True)
def unflag_url(context, obj, ftype):
  return generate_flag_url(ftype=ftype, user=context['request'].user, obj=obj)

