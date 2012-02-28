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

Optional:

For out of the box AJAX support, include the js/flag.js file:

    <script type="text/javascript" src="{{STATIC_URL}}js/flag.js"></script>

Usage
-----

Create a flag type from admin site, for example "bookmark"

Available settings
------------------

DEFAULT_FLAG_TYPE_ID: The ID of default flag type to be used in the project

Available tags
--------------
    
    {% render_flag form of object for flag_type %}

Renders the flag form for the provided object. Override template: 'flag/form.html' for modifying the look.
It even supports multiple flag types.

    {% render_flag form of object for flag_type flag_type flag_type %}

Author: Sjoerd Arendsen
HUB online