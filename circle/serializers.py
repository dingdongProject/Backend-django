from rest_framework import serializers
from circle.models import Circle, MemberShip, DUser, Schedule, Board, Post, Comment

class DUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DUser
        fields = ['username', 'picture', 'email']

class CircleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circle
        fields = ['name', 'explanation', 'picture']

class MemberShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberShip
        fields = ['user', 'circle', 'isAdmin', 'isActive', 'dateJoined']

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['circle', 'date', 'content']

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['circle', 'name', 'memberWrite']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model= Post
        fields =['id', 'board', 'title', 'content', 'owner']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'content', 'owner']
