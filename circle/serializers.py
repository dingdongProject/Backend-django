from rest_framework import serializers
from circle.models import Circle, MemberShip
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CircleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circle
        fields = [ 'name', 'explanation']


class MemberShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberShip
        fields = ['user', 'circle', 'isAdmin']

