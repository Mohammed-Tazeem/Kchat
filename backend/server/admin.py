from django.contrib import admin

from .models import *

admin.site.register(Category)
admin.site.register(Server)
admin.site.register(Channel)

# Register your models here.
