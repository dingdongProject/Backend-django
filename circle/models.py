from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

class DUser(User):
    picture = models.URLField('picture')

    def __str__(self):
        return self.username


class Circle(models.Model):
    name = models.CharField(max_length=100, default='circle')
    explanation = models.CharField(max_length=100, default='Circle Explaination')
    picture = models.URLField('picture', default="htttp://none.com")

    def __str__(self):
        return self.name

class MemberShip(models.Model):
    user = models.ForeignKey(DUser, on_delete=models.CASCADE)
    circle = models.ForeignKey('Circle', on_delete=models.CASCADE)
    isAdmin = models.BooleanField(default=False)
    isActive = models.BooleanField(default=False)
    dateJoined = models.DateField(default=datetime.date.today())
    def __str__(self):
        return self.user.username + " " + self.circle.name

class Schedule(models.Model):
    circle = models.ForeignKey('Circle', on_delete=models.CASCADE)
    date = models.DateField()
    content = models.CharField(max_length=500, default='None')

class Board(models.Model):
    circle = models.ForeignKey('Circle', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='None')
    memberWrite = models.BooleanField(default=True)
    def __str__(self):
        return self.circle.name + " " + self.name

class Post(models.Model):
    board = models.ForeignKey('Board', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='None')
    content = models.CharField(max_length=1000, default='None')
    owner = models.ForeignKey('Duser', on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    content = models.CharField(max_length=1000, default='None')
    owner = models.ForeignKey('Duser', on_delete=models.CASCADE)

class Read(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey('Duser', on_delete=models.CASCADE)
    hasRead = models.BooleanField(default=False)


