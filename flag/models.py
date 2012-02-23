from django.core.urlresolvers import reverse
from django.db import models
from flag.managers import FlagManager
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class Flag(models.Model):
  user = models.ForeignKey(User, verbose_name=_('user'))
  name = models.CharField(max_length=255, help_text='The machine-name for this flag.')
  timestamp = models.DateTimeField(auto_now=True)
  
  content_type   = models.ForeignKey(ContentType,
          verbose_name=_('content type'),
          related_name="content_type_set_for_%(class)s")
  object_pk      = models.TextField(_('object ID'))
  content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")
  
  objects = FlagManager()
  
  def get_flag_url(self):
    return "/flag/set_flag?name=" + str(self.name) + "&object_pk=" + str(self.object_pk) + "&content_type=" + str(self.content_type.id)

class FlagCounts(models.Model):
  flag = models.ForeignKey('Flag', null=False)
  
  content_type   = models.ForeignKey(ContentType,
          verbose_name=_('content type'),
          related_name="content_type_set_for_%(class)s")
  object_pk      = models.TextField(_('object ID'))
  content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")
  
  class Meta:
    db_table = 'flag_counts'