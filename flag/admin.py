from django.contrib import admin
from django import forms
from flag.models import *

class FlagTypeAdmin(admin.ModelAdmin):
    list_display=('title',)
    prepopulated_fields = {"slug": ("title",)}
'''
class FlagAdmin(admin.ModelAdmin):    
    list_display = ('choice', 'vtype', 'content_object', 'content_type', 'submit_date', 'user', 'session')
    list_filter = ['vtype', 'choice', 'content_type', 'submit_date']
    search_fields = ['user__username', 'user__email', 'content_type__app_label', 'ip_address']
    date_hierarchy = 'submit_date'    
'''
admin.site.register(FlagType, FlagTypeAdmin)

#admin.site.register(Flag, FlagAdmin)
