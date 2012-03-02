from django import forms
from django.forms import ModelForm
from flag.models import *
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError 
from django.forms.models import modelformset_factory, BaseModelFormSet
from django.forms.formsets import BaseFormSet, formset_factory
from django.utils import simplejson

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
    #print ftype    
    if request.POST:                       
      data = request.POST
      instance = self.get_instance_by_post_data(request)
    
    super(FlagForm, self).__init__(data=data, initial=initial, instance=instance, *args, **kwargs)
    
  content_type  = forms.ModelChoiceField(queryset=ContentType.objects.all(), widget=forms.HiddenInput)
  object_pk     = forms.CharField(widget=forms.HiddenInput)
  ftype         = forms.ModelChoiceField(queryset=FlagType.objects.all(), widget=forms.HiddenInput)
  
  def get_instance(self, request, obj=None, ftype=None, *args, **kwargs):
    '''
    Returns instance according to the object and request (user,
    session). Needs either object or content_type, object_pk as
    arguments as does `get_by_obj_client`
    '''
    #print ftype
    if ftype.global_flag:
      flag = Flag.objects.filter_for_obj(obj, *args, **kwargs)
      
      if flag:
        instance = flag[0]
      else:
        instance = Flag(ftype=ftype, user=request.user, *args, **kwargs) 
        
    else:
      try:
        instance = Flag.objects.filter_by_obj_client(request=request, obj=obj, ftype=ftype, *args, **kwargs).get()
      except Flag.DoesNotExist:
        instance = Flag(ftype=ftype, user=request.user, *args, **kwargs)
        
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
    
    #flag = super(FlagForm, self).save(commit=False, *args, **kwargs)
    #print flag.values()
    #flag.user = self.request.user
    #print self.instance
    if self.instance.id:
      self.instance.delete()
    else:
      flag = super(FlagForm, self).save(commit=False, *args, **kwargs)
      flag.save()
  
  class Meta:
    model = Flag
    fields = ('content_type', 'object_pk', 'ftype')
  
class FlagMultiForm(forms.Form):
  def __init__(self, request, data=None, initial={}, obj=None, ftypes=None, *args, **kwargs):
    if obj:            
      ctype = ContentType.objects.get_for_model(obj)
      initial['content_type'] = ctype
      initial['object_pk']    = obj.pk
        
    if request.POST:                       
      data = request.POST
      
      if obj is None:
        ct = ContentType.objects.get_for_id(data['content_type'])
        obj = ct.get_object_for_this_type(pk=data['object_pk'])
      
      if ftypes is None:
        if 'ftypes_dict' in data:
          dict = simplejson.loads(force_unicode(data['ftypes_dict']))
          ids = [k for k,v in dict]
          ftypes = list(FlagType.objects.filter(id__in=ids))
    
    self.ftypes = ftypes
    self.request = request
    self.obj = obj
      
    super(FlagMultiForm, self).__init__(data=data, initial=initial, *args, **kwargs)
    
    choices = []
    for ftype in self.ftypes:
      choices.append((ftype.id, ftype.label))
    
    # Get flags for this user/object
    flags = Flag.objects.filter_by_obj_client(request=self.request, obj=self.obj, ftype__in=ftypes).values_list('ftype_id', flat=True)

    self.fields['ftypes'].choices = choices
    self.fields['ftypes'].initial = flags
    self.fields['ftypes_dict'].initial = simplejson.dumps(choices)
  
  content_type  = forms.ModelChoiceField(queryset=ContentType.objects.all(), widget=forms.HiddenInput)
  object_pk     = forms.CharField(widget=forms.HiddenInput)
  ftypes_dict   = forms.CharField(widget=forms.HiddenInput)
  ftypes        = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,required=False,label="")

  def save(self, *args, **kwargs):
    '''
    Because we fake the flag field lets check this on save
    '''
    for ftype in self.ftypes:
      if str(ftype.id) in self.cleaned_data['ftypes']:
        try:
          flag = Flag.objects.filter_by_obj_client(request=self.request, obj=self.obj, ftype=ftype).get()
        except Flag.DoesNotExist:
          flag = Flag.objects.create_for_object(obj=self.obj, user=self.request.user, ftype=ftype)
      else:
        try:
          flag = Flag.objects.filter_by_obj_client(request=self.request, obj=self.obj, ftype=ftype).get()
          flag.delete()
        except Flag.DoesNotExist:
          pass   