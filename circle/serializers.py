from rest_framework import serializers
from circle.models import Circle, MemberShip, DUser, Schedule, Board, Post, Comment, PostImage

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
        model = Post
        fields = ['id', 'board', 'title', 'content']

class PostSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'owner']

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['image']