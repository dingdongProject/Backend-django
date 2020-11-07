from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from circle.models import Circle, MemberShip, DUser, Board
from circle.serializers import DUserSerializer, CircleSerializer, MemberShipSerializer, BoardSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth.models import UserManager
from rest_framework.authtoken.models import Token
from rest_framework import mixins
from rest_framework import generics

class SignUp(APIView):
    def post(self, request, format=None):
        username = request.data['username']
        password = request.data['password']
        email = request.data['email']
        user = DUser.objects.create_user(username=username, email=email, password=password)
        token = Token.objects.create(user=user)
        print('user', user)
        return JsonResponse({"token": token.key}, safe=False)


class UserMine(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        user = DUser.objects.get(username=request.user)
        serializer = DUserSerializer(user)
        return JsonResponse(serializer.data, safe=False)


class UserDetail(APIView):
    def get(self, request, name, format=None):
        user = DUser.objects.get(username=name)
        serializer = DUserSerializer(user)
        return JsonResponse(serializer.data)


class UserCircles(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        user = DUser.objects.get(username=request.user)
        print(user)
        membership = MemberShip.objects.filter(user=user)
        print(membership)
        circles = [{"name": member.circle.name, "isAdmin": member.isAdmin} for member in membership]
        return JsonResponse({"circles": circles}, safe=False)

class MemberShipList(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        circlename = request.data['circle']
        isAdmin = request.data['isAdmin']
        try:
            user = DUser.objects.get(username=request.user)
            circle = Circle.objects.get(name=circlename)
            membership = MemberShip.objects.filter(user=user, circle=circle)
            if membership:
                return JsonResponse({"success": False, "result": "already Exist"}, safe=False)
            membership = MemberShip.objects.create(user=user, circle=circle, isAdmin=isAdmin)
            if membership:
                return JsonResponse({"success": True, "joined": circle.name, "user": user.username, "isAdmin": isAdmin}, safe=False)
            return JsonResponse({"success": False}, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"success": False}, safe=False)

    def delete(self, request, format=None):
        try:
            circlename = request.data['circle']
            user = DUser.objects.get(username=request.user)
            circle = Circle.objects.get(name=circlename)
            membership = MemberShip.objects.get(user=user, circle=circle)
            if membership:
                membership.delete()
                return JsonResponse({"success": True})
            return JsonResponse({"success": False})
        except:
            return JsonResponse({"success": False})


class CircleList(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        circles = Circle.objects.all()
        serializer = CircleSerializer(circles, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, format=None):
        name = request.data['name']
        explanation = request.data['explanation']
        try:
            circle = Circle.objects.get(name=name)
        except:
            circle = False
        if circle:
            return JsonResponse({"success": False})
        circle = Circle.objects.create(name=name, explanation=explanation)
        Board.objects.create(name="Notice", circle=circle, memberWrite=False)
        Board.objects.create(name="Gallery", circle=circle)
        MemberShip.objects.create(user=DUser.objects.get(username=request.user), circle=circle, isAdmin=True, isActive=True)
        serializer = CircleSerializer(circle)
        return JsonResponse({"success": False, "circle": serializer.data}, safe=False)

    def delete(self, request, format=None):
        name = request.data['name']
        try:
            circle = Circle.objects.get(name=name)
            circle.delete()
        except:
            return JsonResponse({"success": False})
        return JsonResponse({"success": True}, safe=False)

class CircleDetail(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, name, format=None):
        circle = Circle.objects.get(name=name)
        serializer = CircleSerializer(circle)
        return JsonResponse(serializer.data, safe=False)

class CircleMembers(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, name, format=None):
        circle = Circle.objects.get(name=name)
        membership = MemberShip.objects.filter(circle=circle)
        members = [{"name": member.user.username, "isAdmin": member.isAdmin} for member in membership]
        return JsonResponse({"members": members}, safe=False)

class BoardList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, circle, format=None):
        try:
            circle = Circle.objects.get(name=circle)
            boards = Board.objects.filter(circle=circle)
            print(boards)
            boards = [{"id": board.id, "name": board.name, "memberWrite": board.memberWrite} for board in boards]
            return JsonResponse({"boards": boards})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False})
    def post(self, request, circle, board, format=None):
        try:
            if not check_authorization(request.user, circle):
                return JsonResponse({"success": False})
            circle = Circle.objects.get(name=circle)
            board = Board.objects.create(name=board, circle=circle)
            return JsonResponse({"success": True, "board": {"id": board.id, "name": board.name, "memberWrite": board.memberWrite, "circle": board.circle.name}})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False})


class BoardDetail(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, pk, format=None):
        try:
            board = Board.objects.get(id=pk)
            print(board)
            #Todo: 게시물들도 같이 보내기
            return JsonResponse({"success": True, "board": {"id": board.id, "name": board.name, "memberWrite": board.memberWrite, "circle": board.circle.name}});
        except Exception as e:
            print(e)
            return JsonResponse({"success": False})
    def put(self, request, pk, format=None):
        try:
            board = Board.objects.get(id=pk)
            if not check_authorization(request.user, board.circle.name):
                return JsonResponse({"success": "Fail. UnAuthorized"})
            name = request.data['name']
            board.name = name
            board.save()
            print(board)
            #Todo: 게시물들도 같이 보내기
            return JsonResponse({"success": True, "board": {"id": board.id, "name": board.name, "memberWrite": board.memberWrite, "circle": board.circle.name}});
        except Exception as e:
            print(e)
            return JsonResponse({"success": False})



def check_authorization(user, circle):
    circle = Circle.objects.get(name=circle)
    user = DUser.objects.get(username=user)
    try:
        membership = MemberShip.objects.get(circle=circle, user=user)
        if membership and membership.isAdmin:
            return True
    except:
        return False
    else:
        return False