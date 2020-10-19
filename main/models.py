from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


class User(AbstractUser):
    username = None
    last_login = None
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True, db_index=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Rule(models.Model):
    rule = models.CharField(max_length=256)


class News(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    header = models.CharField(max_length=100)
    sub_header = models.CharField(max_length=50)
    image = models.ImageField()
    teaser = models.CharField(max_length=320)
    full_text = models.CharField(max_length=10000)


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    comment = models.IntegerField(default=0)
    author = models.CharField(max_length=20)
    date_added = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=10000)

