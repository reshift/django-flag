from django.contrib import admin
from django import forms
from flag.models import *

admin.site.register(Flag, admin.ModelAdmin)