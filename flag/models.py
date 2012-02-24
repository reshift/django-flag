from django.core.urlresolvers import reverse
from django.db import models
from flag.managers import *
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class FlagType(models.Model):
  '''
  The flag type model.
  ''' 
  title       = models.CharField(_('title'), max_length=255)
  slug        = models.SlugField(_('slug'), max_length=50)
  global_flag = models.BooleanField(default=0, verbose_name='Global flag')
  description = models.TextField(blank=True, null=True)
  label = models.CharField(max_length=255, blank=True, null=True)
  flagged_label = models.CharField(max_length=255, blank=True, null=True)
  
  objects = FlagTypeManager()

  def __unicode__(self):
    return self.title.title()

  def choice_queryset(self):
    return self.flag_set.all()
  
class Flag(models.Model):
  '''
  The flag model.
  ''' 
  ftype     = models.ForeignKey(FlagType, verbose_name=_('type'))
  user      = models.ForeignKey(User, verbose_name=_('user'))
  timestamp = models.DateTimeField(auto_now=True)
  
  content_type   = models.ForeignKey(ContentType,
          verbose_name=_('content type'),
          related_name="content_type_set_for_%(class)s")
  object_pk      = models.TextField(_('object ID'))
  content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")
  
  objects = FlagManager()
  
  def get_absolute_url(self):
    try:
      content_object_url = self.content_object.get_absolute_url()
    except:
      content_object_url = None
        
    if content_object_url:            
      return content_object_url
    else:
      return '/'
    
  def save(self, request=None, *args, **kwargs):
    '''
    Save method overriden if `request` var is supplied.
    '''
    if request:                                                
      if request.user.is_authenticated():
        self.user = request.user
        
        # Run validate unique again with user
        self.validate_unique()

    return super(Flag, self).save(*args, **kwargs)
 
  class Meta:
    unique_together = ("content_type", "object_pk", "user", "ftype")

class FlagCounts(models.Model):
  flag = models.ForeignKey('Flag', null=False)
  
  content_type   = models.ForeignKey(ContentType, verbose_name=_('content type'), related_name="content_type_set_for_%(class)s")
  object_pk      = models.TextField(_('object ID'))
  content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")