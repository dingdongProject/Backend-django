from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from circle.models import Circle, MemberShip
from circle.serializers import UserSerializer, CircleSerializer, MemberShipSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth.models import UserManager

class SignUp(APIView):
    def post(self, request, format=None):
        username = request.data['username']
        password = request.data['password']
        print(username, password)
        user = User.objects.create_user(username=username, email=None, password=password)
        print('user', user)
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data, safe=False)

class UserList(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class MemberShipList(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        username = request.data['username']
        circlename = request.data['circle']
        isAdmin = request.data['isAdmin']
        try:
            user = User.objects.get(username=username)
            circle = Circle.objects.get(name=circlename)
            membership = MemberShip.objects.get(user=user, circle=circle)
            if membership:
                return JsonResponse({"success": False, "result": "already Exist"}, safe=False)
            membership = MemberShip.objects.create(user=user, circle=circle, isAdmin=isAdmin)
            if membership:
                return JsonResponse({"success": True, "joined": circle.name, "user": user.username, "isAdmin": isAdmin}, safe=False)
            return JsonResponse({"success": False}, safe=False)
        except:
            return JsonResponse({"success": False}, safe=False)


class UserDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, name, format=None):
        user = self.get_object(username=name)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class UserCircles(APIView):
    def get(self, request, name, format=None):
        user = User.objects.get(username=name)
        membership = MemberShip.objects.filter(user=user)
        circles = [{"name": member.circle.name, "isAdmin": member.isAdmin} for member in membership]
        return JsonResponse({"circles": circles}, safe=False)

class CircleList(APIView):
    def get(self, request, format=None):
        circles = Circle.objects.all()
        serializer = CircleSerializer(circles, many=True)
        return JsonResponse(serializer.data, safe=False)

class CircleDetail(APIView):

    def get(self, request, name, format=None):
        circle = Circle.objects.get(name=name)
        serializer = CircleSerializer(circle)
        return JsonResponse(serializer.data, safe=False)

class CircleMembers(APIView):

    def get(self, request, name, format=None):
        circle = Circle.objects.get(name=name)
        membership = MemberShip.objects.filter(circle=circle)
        members = [{"name": member.user.username, "isAdmin": member.isAdmin} for member in membership]
        return JsonResponse({"members": members}, safe=False)
