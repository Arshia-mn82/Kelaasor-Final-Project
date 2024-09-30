from django.db import models
from account_app.models import *
from task_app.models import Task


class PublicClass(models.Model):
    title = models.CharField(max_length=50)
    unique_id = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField(null=True, blank=True)
    start_register_date = models.DateField(null=True, blank=True)
    end_register_date = models.DateField(null=True, blank=True)
    owners = models.ManyToManyField(Account)
    mentors = models.ManyToManyField(Account)
    students = models.ManyToManyField(Account)
    tasks = models.ManyToManyField(Task, null=True, blank=True)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, null=True, blank=True)


class PrivateClass(models.Model):
    PASSWORD = "P"
    INVITATION_LINK = "I"

    security_types = [
        (PASSWORD, "Password"),
        (INVITATION_LINK, "Invitation Link"),
    ]
    title = models.CharField(max_length=50)
    unique_id = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField(null=True, blank=True)
    signup_type = models.CharField(max_length=1, choices=security_types)
    start_register_date = models.DateField(null=True, blank=True)
    end_register_date = models.DateField(null=True, blank=True)
    owners = models.ManyToManyField(Account)
    students = models.ManyToManyField(Account)
    tasks = models.ManyToManyField(Task, null=True, blank=True)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, null=True, blank=True)
    
    

    
