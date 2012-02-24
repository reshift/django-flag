from django import forms
from django.forms import ModelForm
from flag.models import *
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

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
      initial['object_pk']    = obj.pk
      initial['ftype']        = ftype
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
  
  def get_instance(self, request, obj=None, ftype=None, *args, **kwargs):
    '''
    Returns instance according to the object and request (user,
    session). Needs either object or content_type, object_pk as
    arguments as does `get_by_obj_client`
    '''

    if ftype.global_flag:
      flag = Flag.objects.filter_for_obj(obj, *args, **kwargs)
      
      if flag:
        instance = flag[0]
      else:
        instance = None  
        
    else:
      instance = Flag.objects.get_by_obj_client(request, obj, *args, **kwargs)

    return instance

  def get_instance_by_post_data(self, request, *args, **kwargs):
    '''
    Returns instance according to the post data from request        
    '''
    ftype = FlagType.objects.get(id=request.POST['ftype'])
    ct = ContentType.objects.get_for_id(request.POST['content_type'])
    obj = ct.get_object_for_this_type(pk=request.POST['object_pk'])

    instance = self.get_instance(request, obj=obj, ftype=ftype)     
    return instance
  
  def save(self, *args, **kwargs):
     '''
     Saves the model with the request variable. 
     '''        
     flag = super(FlagForm, self).save(commit=False, *args, **kwargs)
     flag.save(self.request)        
     
     return flag
  '''
  def clean(self):
    cleaned_data = super(FlagForm, self).clean()
    print self.flag .user
    if not self.user.is_authenticated():
      print "great"
      raise forms.ValidationError('Anonymous flags are not allowed.')
    
    return cleaned_data
  '''
  class Meta:
    model = Flag
    fields = ('content_type', 'object_pk', 'ftype')