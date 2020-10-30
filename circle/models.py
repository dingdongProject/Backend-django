from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Circle(models.Model):
    name = models.CharField(max_length=100, default='circle')
    explanation = models.CharField(max_length=100, default='Circle Explaination')

    def __str__(self):
        return self.name

class MemberShip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    circle = models.ForeignKey('Circle', on_delete=models.CASCADE)
    isAdmin = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username + " " + self.circle.name