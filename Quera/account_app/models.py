from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    image = models.ImageField()
    phone_number = models.CharField(max_length=12)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} , {self.phone_number}"
    

class Forum(models.Model):
    QUESTION = 'question'
    ANSWER = 'answer'
    COMMENT = 'comment'

    POST_TYPE_CHOICES = [
        (QUESTION, 'Question'),
        (ANSWER, 'Answer'),
        (COMMENT, 'Comment'),
    ]

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES)

    # For answers, this links to the related question
    related_question = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='answers'
    )

    # For comments, this links to the post (either question or answer)
    related_post = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='comments'
    )

    def __str__(self):
        return f"{self.get_post_type_display().title()} by {self.user.username}"

    def is_question(self):
        return self.post_type == self.QUESTION

    def is_answer(self):
        return self.post_type == self.ANSWER

    def is_comment(self):
        return self.post_type == self.COMMENT
