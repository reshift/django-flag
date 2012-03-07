Flag for Django
=========

Flag is a flexible flagging system

Using this app, one can provide flags to any object, just on the basis of template tags. No configuration of existing models and views required.

Some possibilities include bookmarks, marking important, friends, or flag as offensive.
Flags may be per-user, meaning that each user can mark an item individually, or global, meaning that the item is either marked or it is not marked, and any user who changes that, changes it for everyone.

Installation
------------
- Run 'pip install https://github.com/hub-nl/nl.hub.django.app.flag/tarball/master'
- Add flag urls to your urls file: url(r'flag/', include('flag.urls'))
- Add '{% load flag_tags %}' to the top of your template

Usage
-----

Create a flag type from admin site, for example "bookmark"

Available settings
------------------

DEFAULT_FLAG_TYPE_ID: The ID of default flag type to be used in the project

Available tags
--------------
  
Renders a form with flag checkboxes for the provided object. Override template: 'flag/form.html' for modifying the look.
It also supports multiple flag types.
    
    {% render_flag form of object for flag_type %}
    {% render_flag form of object for flag_type flag_type flag_type %}
    
Flag URL tgat that returns the endpoint url for a flag

    <a href="{% flag_url of game for wishlist  %}">I want this game for christmas</a>

Tag to reveive flags based on given variables.
[object] and [user] variables are optional

    {% get_flag flags for flag_type of [object] user [user] as variable %}

Available endpoints
--------------

You can also create your own form or link and point it to: "<hostname>/flag/[action]/[ftype_slug]/?content_type=[content_type]&object_pk=[object_pk]"

example:

    http://127.0.0.1:8000/flag/flag/wishlist/?content_type=38&object_pk=1
    
Or to unflag:

    http://127.0.0.1:8000/flag/unflag/wishlist/?content_type=38&object_pk=1

The endpoint supports AJAX request and will return a succes variable in JSON set to True or False. I also passes along the serialized Flag type object.

TODO

- Base flag submit on django url function? 
- Prevent link/object spoofing (maybe add a selection to flagtype for wich models it should be active?)

Author: Sjoerd Arendsen
HUB online