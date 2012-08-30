from django import template
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib import comments
from django.utils.encoding import smart_unicode
from flag.models import *
from flag.utils import *
from django.core.urlresolvers import reverse
from django.db.models import Q
import md5

register = template.Library()

@register.assignment_tag
def flag(ftype, *args, **kwargs):
  '''
  Returns a object with info the the flagtype and if its set for the provided user
  {% flag type user=user obj=obj as flag %}
  '''
  user = kwargs.get('user', None)
  obj = kwargs['obj']

  ftype = FlagType.objects.filter(slug=ftype)[0]
  ftype.unflag_url = generate_unflag_url(user=user, obj=obj, ftype=ftype.slug)
  ftype.flag_url = generate_flag_url(user=user, obj=obj, ftype=ftype.slug)

  try:
    flag = ftype.flags.filter_by_obj_user(obj=obj, user=user)[0]
    ftype.set = True
  except :
    ftype.set = False

  return ftype

@register.inclusion_tag('flag/flag.html')
def render_flag(ftype, *args, **kwargs):
  '''
  Returns a object with info the the flagtype and if its set for the provided user
  {% render_flag [type] user=user obj=obj %}
  '''
  user = kwargs.get('user', None)
  obj = kwargs['obj']

  ftype = FlagType.objects.filter(slug=ftype)[0]
  ftype.unflag_url = generate_unflag_url(user=user, obj=obj, ftype=ftype.slug)
  ftype.flag_url = generate_flag_url(user=user, obj=obj, ftype=ftype.slug)

  try:
    flag = ftype.flags.filter_by_obj_user(obj=obj, user=user)[0]
    ftype.set = True
  except :
    ftype.set = False
  
  return {'user': user, 'obj': obj, 'flag': ftype}

@register.assignment_tag
def get_flags(ftype, *args, **kwargs):
  '''
    {% get_flags type user=user as flags %}
  '''
  user = kwargs.get('user', None)

  ftype = FlagType.objects.filter(slug=ftype)[0]

  if user:
    flags = Flag.objects.filter(user=user, ftype=ftype)

  return flags

@register.simple_tag()
def flag_count(ftype, list(*objs)):
  """
  Returns flag count for a type
  """
  query = Q()
  for obj in objs:
    content_type, object_pk = ContentType.objects.get_for_model(obj), obj.pk
    query = query | Q(content_type=content_type, object_pk=object_pk)

  return Flag.objects.filter(ftype__slug=ftype).filter(query).count()

@register.simple_tag(takes_context=True)
def is_flagged(context, ftype, obj):
  """
  Returns whether or not the user has flagged the given object
  """
  flag = Flag.objects.filter_by_obj_user(user=context['request'].user, obj=obj, ftype__slug=ftype)
  return len(flag) == 1

@register.simple_tag(takes_context=True)
def flag_url(context, ftype, obj):
  return generate_unflag_url(ftype=ftype, user=context['request'].user, obj=obj)

@register.simple_tag(takes_context=True)
def unflag_url(context, ftype, obj):
  return generate_flag_url(ftype=ftype, user=context['request'].user, obj=obj)
