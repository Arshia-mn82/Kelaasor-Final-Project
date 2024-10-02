from django.db import models

class FileAnswer(models.Model):
    answer = models.FileField()
    single_task = models.ForeignKey('task_app.SingleTask', on_delete=models.CASCADE , null=True, blank=True)
    group_task = models.ForeignKey('task_app.GroupTask', on_delete=models.CASCADE , null=True, blank=True)
    
class JudgeAnswer(models.Model):
    answer = models.BooleanField()
    single_task = models.ForeignKey('task_app.SingleTask', on_delete=models.CASCADE , null=True, blank=True)
    group_task = models.ForeignKey('task_app.GroupTask', on_delete=models.CASCADE , null=True, blank=True)
    
    
class TextAnswer(models.Model):
    answer = models.TextField()
    single_task = models.ForeignKey('task_app.SingleTask', on_delete=models.CASCADE , null=True, blank=True)
    group_task = models.ForeignKey('task_app.GroupTask', on_delete=models.CASCADE , null=True, blank=True)
    