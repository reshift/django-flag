from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.conf import settings
import hashlib

def generate_unflag_url(ftype, user, obj):
  return reverse('flag_unflag', args=(
    ftype,
    ContentType.objects.get_for_model(obj).pk,
    obj.pk,
    flag_generate_token(obj=obj, user=user)
  ))

def generate_flag_url(ftype, user, obj):
  return reverse('flag_flag', args=(
    ftype,
    ContentType.objects.get_for_model(obj).pk,
    obj.pk,
    flag_generate_token(obj=obj, user=user)
  ))

def flag_generate_token(obj, user):
  content_type, object_pk = ContentType.objects.get_for_model(obj), obj.pk
  token = hashlib.md5(settings.SECRET_KEY + str(content_type.id) + str(object_pk)).hexdigest()
  return token