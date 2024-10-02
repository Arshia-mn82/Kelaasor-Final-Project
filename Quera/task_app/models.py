from django.db import models
from account_app.models import *
from class_app.models import *
from answer_app.models import FileAnswer,TextAnswer,JudgeAnswer


class ScoreBarSingle(models.Model):
    code_result = models.FloatField()
    clean_code = models.FloatField()


class ScoreBarGroup(models.Model):
    code_result = models.FloatField()
    clean_code = models.FloatField()
    teamwork = models.FloatField()


class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    first_deadline = models.DateField()
    second_deadline = models.DateField(null=True, blank=True)
    submit_limit = models.IntegerField(null=True, blank=True)
    score_bar = models.IntegerField(null=True, blank=True)
    file_answer = models.ForeignKey('answer_app.FileAnswer', on_delete=models.CASCADE)
    judge_answer = models.ForeignKey('answer_app.JudgeAnswer', on_delete=models.CASCADE)
    text_answer = models.ForeignKey('answer_app.TextAnswer', on_delete=models.CASCADE)
    question_bank = models.BooleanField()

    def __str__(self) -> str:
        return self.name


class SingleTask(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    score = models.IntegerField(null=True, blank=True)
    score_bar = models.ForeignKey(
        ScoreBarSingle, on_delete=models.CASCADE, null=True, blank=True
    )
    result = models.FloatField()

    def __str__(self) -> str:
        return (
            f"{self.user.first_name} {self.user.last_name} , {self.user.phone_number}"
        )


class GroupTask(models.Model):
    users = models.ManyToManyField(Account)
    group_name = models.CharField(max_length=50)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    score = models.IntegerField(null=True, blank=True)
    score_bar = models.ForeignKey(
        ScoreBarGroup, on_delete=models.CASCADE, null=True, blank=True
    )
    result = models.FloatField()

    def __str__(self) -> str:
        return self.group_name
