Flags APP
=========

Flags is a flexible flagging system

Using this app, one can provide flags for any model. Some possibilities include bookmarks, marking important, friends, or flag as offensive.
Flags may be per-user, meaning that each user can mark an item individually, or global, meaning that the item is either marked or it is not marked, and any user who changes that, changes it for everyone.

Usage
-----

**View**

Set the correct flag object in your view to generate the form.

Example:
    
*get_flag([name], [object], [user])*
    
    your_model_object = get_object_or_404(Model.objects.all(), id=1)
    user = request.user
    flag_wishlist = Flag.objects.for_model(your_model_object).filter(user=request.user, name='wishlist').get()

**Template**

Render the flag form in your template.
you can use the provided form template tag, but this is not necesarry.


Example:

*{% render_flag_form for [object] [flagged_label] [unflagged_label]  %}*
    
    {% render_flag_form for flag_wishlist "Remove from wishlist" "Add to wishlist" %}


Author: Sjoerd Arendsen
HUB online