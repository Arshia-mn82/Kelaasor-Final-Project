from django.contrib.admin import ModelAdmin, register
from .models import *


@register(PublicClass)
class PublicClassAdmin(ModelAdmin):
    pass


@register(PrivateClass)
class PrivateClassAdmin(ModelAdmin):
    pass
