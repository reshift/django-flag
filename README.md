Flag for Django
=========

Flag is a flexible flagging system

Using this app, one can provide flags to any object, just on the basis of template tags. No configuration of existing models and views required.

Some possibilities include bookmarks, marking important, friends, or flag as offensive.
Flags may be per-user, meaning that each user can mark an item individually, or global, meaning that the item is either marked or it is not marked, and any user who changes that, changes it for everyone.

Usage
-----

Create a flag type from admin site, for example "bookmark"


Available tags
--------------
    
    {% render_flag form of object for flag_type %}

Renders the flag form for the provided object. Override template: 'flag/form.html' for modifying the look.

Author: Sjoerd Arendsen
HUB online