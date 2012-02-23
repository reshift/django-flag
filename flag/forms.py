from django import forms
from django.forms import ModelForm
from flag.models import *

class FlagForm(ModelForm):
  id = forms.IntegerField(required=False, widget=forms.HiddenInput())
  user = forms.IntegerField(required=False, widget=forms.HiddenInput())
  object_pk = forms.IntegerField(required=True, widget=forms.HiddenInput())
  content_type = forms.IntegerField(required=True, widget=forms.HiddenInput())
  name = forms.CharField(required=True, widget=forms.HiddenInput())
  
  class Meta:
    model = Flag