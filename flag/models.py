from django.core.urlresolvers import reverse
from django.db import models
from flag.managers import *
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import md5

class FlagType(models.Model):
  '''
  The flag type model.
  ''' 
  title         = models.CharField(_('title'), max_length=255, help_text='A short, descriptive title for this flag.')
  slug          = models.SlugField(_('slug'), max_length=50, help_text='The machine-name for this flag. It may be up to 50 characters long and may only contain lowercase letters, underscores, and numbers. It will be used in URLs and in all API calls.')
  global_flag   = models.BooleanField(default=0, verbose_name='Global flag', help_text='If checked, flag is considered "global" and each object is either flagged or not. If unchecked, each user has individual flags on content.')
  label         = models.CharField(max_length=255, blank=True, null=True, help_text='The text for the "flag this" link for this flag.')
  unflag_label  = models.CharField(max_length=255, blank=True, null=True, help_text='The text for the "unflag this" link for this flag.')
  description   = models.TextField(blank=True, null=True)
  
  objects = FlagTypeManager()

  def __unicode__(self):
    return self.title.title()

  def flag_queryset(self):
    return self.flag_set.all()
  
class Flag(models.Model):
  '''
  The flag model.
  ''' 
  ftype           = models.ForeignKey(FlagType, verbose_name=_('type'), related_name='flags')
  user            = models.ForeignKey(User, verbose_name=_('user'))
  timestamp       = models.DateTimeField(auto_now=True)
  content_type    = models.ForeignKey(ContentType, verbose_name=_('content type'), related_name="content_type_set_for_%(class)s")
  object_pk       = models.CharField(_('object ID'), max_length=200)
  content_object  = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")
  #flag            = models.BooleanField(default=0)
  
  objects = FlagManager()

  def get_label(self):
    if self.pk:
      return self.ftype.unflag_label
    else:
      return self.ftype.label
  
  def get_absolute_url(self):
    try:
      content_object_url = self.content_object.get_absolute_url()
    except:
      content_object_url = None
        
    if content_object_url:            
      return content_object_url
    else:
      return '/'

  class Meta:
    unique_together = ("content_type", "object_pk", "user", "ftype")

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
  token = md5.new(settings.SECRET_KEY + str(content_type.id) + str(object_pk)).hexdigest()
  return token

'''
class FlagCounts(models.Model):
  flag           = models.ForeignKey('Flag', null=False)
  content_type   = models.ForeignKey(ContentType, verbose_name=_('content type'), related_name="content_type_set_for_%(class)s")
  object_pk      = models.TextField(_('object ID'))
  content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")
'''  