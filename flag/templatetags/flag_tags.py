from django import template
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib import comments
from django.utils.encoding import smart_unicode
from flag.forms import *

register = template.Library()

class ResultsForObjectNode(template.Node):
  def __init__(self, obj, flagged_label, unflagged_label):
    self.obj = template.Variable(obj)
    self.flagged_label = flagged_label
    self.unflagged_label = unflagged_label

  def render(self, context):
    try:
      obj = self.obj.resolve(context)
    except template.VariableDoesNotExist:
      return ''
    
    form = FlagForm(instance=obj)
    return render_to_string('flag/form.html', {"form" : form, "flag" : obj, 'flagged_label' : self.flagged_label, 'unflagged_label' : self.unflagged_label}, context_instance=context)

@register.tag
def render_flag_form(parser, token):
    bits = list(token.split_contents())

    obj = bits[2] # Flag object
    flagged_label = bits[3].strip('"')
    unflagged_label = bits[4].strip('"')
  
    return ResultsForObjectNode(obj, flagged_label, unflagged_label)