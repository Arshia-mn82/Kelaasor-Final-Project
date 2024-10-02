from django.db import models
from account_app.models import *


class PublicClass(models.Model):
    title = models.CharField(max_length=50)
    unique_id = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField(null=True, blank=True)
    start_register_date = models.DateField(null=True, blank=True)
    end_register_date = models.DateField(null=True, blank=True)
    owners = models.ManyToManyField(Account, related_name="Public_Owners")
    mentors = models.ManyToManyField(Account, related_name="Public_Mentors")
    students = models.ManyToManyField(Account, related_name="Public_Students")
    tasks = models.ManyToManyField("task_app.Task", blank=True)
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
    owners = models.ManyToManyField(Account, related_name="Private_Owners")
    mentors = models.ManyToManyField(Account, related_name="Private_Mentors")
    students = models.ManyToManyField(Account, related_name="Private_Students")
    tasks = models.ManyToManyField("task_app.Task", blank=True)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, null=True, blank=True)
