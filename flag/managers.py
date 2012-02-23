from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode

class FlagManager(models.Manager):
  #def get_query_set(self):
    #return self.get_query_set().filter(self.model, self.instance)
  
  def for_user(self, user):
    self.get_query_set().filter(user=user)
    return self
  
  def get_flag(self, name, model, user):
    self.for_model(model)
    self.for_user(user)
    self.filter(name=name)
    return self  
  
  def for_model(self, model):
    ct = ContentType.objects.get_for_model(model)
    self.get_query_set().filter(content_type=ct)
    if isinstance(model, models.Model):
      self = self.filter(object_pk=force_unicode(model._get_pk_val()))
    
    return self 