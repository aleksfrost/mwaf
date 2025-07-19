from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Users(AbstractUser):
    USERNAME_FIELD = 'username'  # Поле для аутентификации
    REQUIRED_FIELDS = ['email']  # Обязательные поля при создании пользователя

    password = models.CharField(unique=False, blank=True, null=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


class Answer(models.Model):
    user = models.ForeignKey("Users", on_delete=models.PROTECT)
    question = models.ForeignKey("Question", on_delete=models.PROTECT)
    value = models.IntegerField(unique=False, blank=False, null=False)
    passed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'answers'


class Question(models.Model):
    question = models.CharField(unique=True, blank=False, null=False)
    anchor = models.ForeignKey("Anchor", on_delete=models.PROTECT)
    quiz = models.ForeignKey("Quiz", on_delete=models.PROTECT)

    class Meta:
        managed = True
        db_table = 'questions'


class Quiz(models.Model):
    quiz = models.CharField(unique=True, blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'quizes'

class Importance(models.Model):
    value = models.IntegerField(unique=True, blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'importance'

class Anchor(models.Model):
    anchor = models.CharField(unique=True, blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'anchors'