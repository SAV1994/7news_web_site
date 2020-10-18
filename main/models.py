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
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, db_index=True)
    header = models.CharField(max_length=100)
    sub_header = models.CharField(max_length=50)
    image = models.ImageField()
    teaser = models.CharField(max_length=320)
    full_text = models.CharField(max_length=10000)


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, blank=True, db_index=True)
    author = models.CharField(max_length=20, default='Anonymous')
    date_added = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=10000)

    class Meta:
        abstract = True


class CommentLvl1(Comment):
    pass


class CommentLvl2(Comment):
    comment = models.ForeignKey(CommentLvl1, on_delete=models.CASCADE, blank=True, db_index=True)


class CommentLvl3(Comment):
    comment = models.ForeignKey(CommentLvl2, on_delete=models.CASCADE, blank=True, db_index=True)
