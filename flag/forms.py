from django import forms
from django.forms import ModelForm
from flag.models import *
from django.contrib.contenttypes.models import ContentType

class FlagForm(ModelForm):
  def __init__(self, request, data=None, initial={}, obj=None, instance=None, ftype=None, *args, **kwargs):
    '''
    Fills `content_type` and `object_pk` according to object and
    processes `request` data
    '''                    
    self.request = request
    if obj:            
      ctype = ContentType.objects.get_for_model(obj)
      initial['content_type'] = ctype
      initial['object_pk'] = obj.pk
      initial['ftype'] = ftype
      instance = self.get_instance(request, obj=obj, ftype=ftype)
        
    if request.POST:                       
      data = request.POST
      instance = self.get_instance_by_post_data(request)
    
    super(FlagForm, self).__init__(data=data, initial=initial, instance=instance, *args, **kwargs)
    
  content_type  = forms.ModelChoiceField(queryset=ContentType.objects.all(), widget=forms.HiddenInput)
  object_pk     = forms.CharField(widget=forms.HiddenInput)
  ftype         = forms.ModelChoiceField(queryset=FlagType.objects.all(), widget=forms.HiddenInput)
  
  def get_id(self):
    '''
    Returns the id for the html form.
    '''
    ctype = self.data.get('content_type', self.initial.get('content_type','').id)
    object_pk = self.data.get('object_pk', self.initial.get('object_pk',''))
    return "flag_%s_%s" %(ctype, object_pk)
  
  def get_instance(self, request, *args, **kwargs):
    '''
    Returns instance according to the object and request (user,
    session). Needs either object or content_type, object_pk as
    arguments as does `get_by_obj_client`
    '''
    instance = Flag.objects.get_by_obj_client(request, *args, **kwargs)
    
    return  instance

  def get_instance_by_post_data(self, request, *args, **kwargs):
    '''
    Returns instance according to the post data from request        
    '''
    ftype=request.POST['ftype']
    instance = self.get_instance(request,
                         content_type=request.POST['content_type'],
                         object_pk=request.POST['object_pk'],
                         ftype=request.POST['ftype'],
                         *args, **kwargs)
    return instance
  
  def save(self, *args, **kwargs):
     '''
     Saves the model with the request variable. 
     '''        
     flag = super(FlagForm, self).save(commit=False, *args, **kwargs)
     flag.save(self.request)        
     
     return flag
  
  class Meta:
    model = Flag
    fields = ('content_type', 'object_pk', 'ftype')