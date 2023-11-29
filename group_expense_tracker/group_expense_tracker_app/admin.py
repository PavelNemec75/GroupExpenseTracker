from django.contrib import admin # noqa F401

# Register your models here.

from .models import Posts
admin.site.register(Posts)
