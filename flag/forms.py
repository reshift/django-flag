from django import forms
from django.forms import ModelForm
from flag.models import *
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError 
from django.forms.models import modelformset_factory, BaseModelFormSet
from django.forms.formsets import BaseFormSet, formset_factory
from django.utils import simplejson

'''
class FlagSimpleForm(FlagForm):
'''   

class FlagForm(forms.Form):
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
      
    super(FlagForm, self).__init__(data=data, initial=initial, *args, **kwargs)
    
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
    
  '''
  def clean(self):
    data = self.cleaned_data
    if "password1" in data and "password2" in data and data["password1"] != data["password2"]:
      raise forms.ValudationError("Passwords must be same")
  '''