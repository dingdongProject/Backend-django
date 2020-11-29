from django.db import models
from django.contrib.auth.models import User
import datetime


class DUser(User):
    picture = models.FileField(default="default.png")

    def __str__(self):
        return self.username


class Circle(models.Model):
    name = models.CharField(max_length=100, default='circle')
    explanation = models.CharField(max_length=100, default='Circle Explaination')
    picture = models.FileField(default="default-circle.png")
    code = models.CharField(max_length=8, default="")

    def __str__(self):
        return self.name
class CircleTag(models.Model):
    circle = models.ForeignKey('Circle', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)
    def __str__(self):
        return self.circle.name + " " + self.tag.name


class Tag(models.Model):
    name = models.CharField(max_length=20, default='')
    def __str__(self):
        return self.name

class MemberShip(models.Model):
    user = models.ForeignKey(DUser, on_delete=models.CASCADE)
    circle = models.ForeignKey('Circle', on_delete=models.CASCADE)
    isAdmin = models.BooleanField(default=False)
    isActive = models.BooleanField(default=True)
    dateJoined = models.DateField(default=datetime.date.today())
    def __str__(self):
        return self.user.username + " " + self.circle.name

class Request(models.Model):
    requester = models.ForeignKey(DUser, on_delete=models.CASCADE)
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE)
    isProcessed = models.BooleanField(default=False)
    def __str__(self):
        return self.requester.username + " " + self.circle.name

class Schedule(models.Model):
    circle = models.ForeignKey('Circle', on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=datetime.datetime.now())
    title = models.CharField(max_length=500, default='None')
    content = models.CharField(max_length=500, default='None')
    def __str__(self):
        return self.circle.name + " " + self.title

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
    created_at = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return self.board.circle.name + " " + self.board.name + " " + self.title

class Read(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey('Duser', on_delete=models.CASCADE)
    hasRead = models.BooleanField(default=False)
    def __str__(self):
        return self.post.title+ " " + self.user.name

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    content = models.CharField(max_length=1000, default='None')
    owner = models.ForeignKey('Duser', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return self.post.title+ " " + self.content

class PostImage(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    image = models.FileField(default="default.png")
    def __str__(self):
        return self.post.title + " image"
