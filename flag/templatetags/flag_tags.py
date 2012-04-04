from django import template
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib import comments
from django.utils.encoding import smart_unicode
from flag.forms import *
from flag.models import *
from django.core.urlresolvers import reverse
import md5

register = template.Library()

class ResultsForObjectNode(template.Node):
  def __init__(self, obj, ftype):
    self.obj = template.Variable(obj)
    self.ftype = ftype

  def render(self, context):
    try:
      obj = self.obj.resolve(context)
    except template.VariableDoesNotExist:
      return ''
    
    content_type, object_pk = ContentType.objects.get_for_model(obj), obj.pk
    
    try:
      flag = Flag.objects.filter_by_obj_client(request=context['request'], obj=obj)
      action = "unflag"
    except Flag.DoesNotExist:
      action = "flag"
    
    #token = md5.new(settings.SECRET_KEY + self.ftype + content_type.id + object_pk).hexdigest()
    token = md5.new(settings.SECRET_KEY + str(content_type.id) + str(object_pk)).hexdigest()
    return reverse('flag-flag', args=[action, self.ftype]) + "?content_type=" + str(content_type.id) + "&object_pk=" + str(object_pk) + "&token=" + str(token)

@register.tag
def flag_url(parser, token):
  bits = list(token.split_contents())
  obj = bits[2] # Flag object
  ftype = bits[4]

  return ResultsForObjectNode(obj, ftype)

class ResultsForFlags(template.Node):
  def __init__(self, ftype, variable, obj=None, user=None): 
    self.obj = obj
    if obj is not None:
      self.obj = template.Variable(obj)
    
    self.user = user
    if user is not None:
      self.user = template.Variable(user)
        
    self.ftype = ftype
    self.variable = variable

  def render(self, context):
    if not context['request'].user.is_authenticated():
      return ""
    
    kwargs = {
      'ftype__slug': self.ftype,
    }
    
    # Get user object
    if self.user is not None:
      try:
        user = self.user.resolve(context)
        kwargs['user'] = user
      except template.VariableDoesNotExist:
        pass
    else:
      kwargs['user'] = context['request'].user
    
    # Get object
    if self.obj is not None:
      try:
        obj = self.obj.resolve(context)
        bookmark_type = ContentType.objects.get_for_model(obj)
        kwargs['content_type__pk'] = bookmark_type.id
        kwargs['object_pk'] = obj.id
      except template.VariableDoesNotExist:
        pass
    
    flags = Flag.objects.filter(**kwargs)

    context[self.variable] = flags
    return ''

@register.tag
def get_flag(parser, token):
  '''
  {% get_flag flags for flag_type of [object] user [user] as variable %}
  '''
  
  bits = list(token.split_contents())
  ftype = bits[3] # Flag object
  obj = None
  user = None
  variable = "flags"

  for k, v in enumerate(bits):
    if v == 'of':
      obj = bits[k+1]
    
    if v == 'user' and user is None:
      user = bits[k+1]
    
    if v == 'as':
      variable = bits[k+1]  

  return ResultsForFlags(ftype, variable, obj, user)

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

        self.ftypes = []
        for type in ftypes:
          self.ftypes.append(parser.compile_filter(type))
        
        self.ftypes = FlagType.objects.filter(slug__in=ftypes)
      else:
        raise template.TemplateSyntaxError("Argument #%d in %r tag must be 'for' (valuation type) or 'as' (variable name)" % (4+shift, tokens[0+shift]))

  def get_method(self, method):
    return self.methods.get(method, None)
  
  def render(self, context):
    if not context['request'].user.is_authenticated():
      return ""
    
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
    if(len(self.ftypes) == 1):
      context['flag_form'] = FlagForm(request=context['request'], obj=self.obj.resolve(context), ftype=self.ftypes[0])
      template_search_list = [
        "flag/%s/form.html" % self.ftypes[0],
        "flag/form.html"
      ]
      return render_to_string(template_search_list, context)
    else:
      context['flag_form'] = FlagMultiForm(request=context['request'], obj=self.obj.resolve(context), ftypes=self.ftypes)
      return render_to_string('flag/multiform.html', context)
    
  methods['form'] = form

def do_render_flag(parser, token):
  return FlagRenderNode(parser, token)
  
register.tag('render_flag', do_render_flag)    