from django import template
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib import comments
from django.utils.encoding import smart_unicode
from flag.forms import *
from flag.models import *

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
    

class BaseFlagNode(template.Node):
  methods = {}
  '''
  This is the base node for flag app. Inherited by get and render
  template tags. The tags can use the default flag type (pk=1 or
  DEFAULT_FLAG_TYPE_PK setting. The valuation type if required can
  be specified by `for flag_type` as arguments in the tag. 
  '''
  def __init__(self, parser, token, shift=0):
    '''
    Parses tag arguments and provides attributes for future methods.
    '''
    tokens = token.contents.split()
    self.ftype = FlagType.objects.get_type()
    self.as_varname = False
    method = self.get_method(tokens[1])
    if not method:
        raise template.TemplateSyntaxError("%r is not a valid method in %r tag" %(tokens[1], tokens[0]))
    else:
        self.method = method
        if tokens[1]=='choice_count':                
            if len(tokens) < 5 or not tokens[4]=='for_choice':                    
                raise template.TemplateSyntaxError("Fourth argument in %r tag must be 'for_choice'" % tokens[0])
            else:
                self.choice=tokens[5]
            shift+=2
    
    if not tokens[2]=='of':
        raise template.TemplateSyntaxError("Second argument in %r tag must be 'of'" % tokens[0])

    self.obj = parser.compile_filter(tokens[3])
    
    if len(tokens)==4+shift:
        pass
    
    elif len(tokens)>=6+shift:
      if tokens[4+shift]=='for':
        ftypes = tokens[5+shift:len(tokens)]
        self.ftypes = FlagType.objects.filter(slug__in=ftypes)
      else:
        raise template.TemplateSyntaxError("Argument #%d in %r tag must be 'for' (valuation type) or 'as' (variable name)" % (4+shift, tokens[0+shift]))

  def get_method(self, method):
    return self.methods.get(method, None)
  
  def render(self, context):
    result = self.method(self, context)
    
    if self.as_varname:
      context[self.as_varname] = result
      return ''
    else:
      return result

class FlagRenderNode(BaseFlagNode):
  '''
  This nodes render directly through an html template. Templates can be
  overridden at templates/flag/*.html    
  '''
  methods = {}
  def form(self, context):
    from django.forms.formsets import formset_factory
    from django.forms.models import modelformset_factory, inlineformset_factory
    from django.utils.functional import curry
    '''
    Renders the valuation form for the object.
    Override template: 'flag/form.html' for modifying the look.
    '''
    context['flag_form'] = FlagForm(request=context['request'], obj=self.obj.resolve(context), ftypes=self.ftypes)
    
    return render_to_string('flag/form.html', context)
  
  methods['form'] = form

def do_get_flag(parser, token):
  return FlagGetNode(parser, token)

def do_render_flag(parser, token):
  return FlagRenderNode(parser, token)

register.tag('get_flag', do_get_flag)
register.tag('render_flag', do_render_flag)    