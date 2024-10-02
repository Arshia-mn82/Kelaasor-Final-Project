from django.contrib.admin import register,ModelAdmin
from .models import *

@register(Account)
class AccountAdmin(ModelAdmin):
    pass

@register(Forum)
class ForumAdmin(ModelAdmin):
    pass