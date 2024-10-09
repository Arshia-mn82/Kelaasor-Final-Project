from django.contrib.admin import register, ModelAdmin
from .models import *


@register(Task)
class TaskAdmin(ModelAdmin):
    pass


@register(GroupTask)
class GroupTaskAdmin(ModelAdmin):
    pass


@register(SingleTask)
class SingleTaskAdmin(ModelAdmin):
    pass


@register(ScoreBarSingle)
class ScoreBarSignleAdmin(ModelAdmin):
    pass


@register(ScoreBarGroup)
class ScoreBarGroupAdmin(ModelAdmin):
    pass
