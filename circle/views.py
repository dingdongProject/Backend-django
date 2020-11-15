from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from circle.models import Circle, MemberShip, DUser, Board, Post, Read, Comment
from circle.serializers import DUserSerializer, CircleSerializer, MemberShipSerializer, BoardSerializer, PostSerializer, CommentSerializer
from rest_framework.views import APIView

from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth.models import UserManager
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import mixins
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken



class Ping(APIView):
    def get(self,request):
        return Response({"pong"})

class SignUp(APIView):
    def post(self, request, format=None):
        try:
            username = request.data['username']
            password = request.data['password']
            email = request.data['email']
            user = DUser.objects.create_user(username=username, email=email, password=password)
            return JsonResponse({"success": True})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "message": e.__str__()})

class LogIn(APIView):
    def post(self, request):
        try:
            user = DUser.objects.get(username=request.data['username'])
            serializer = AuthTokenSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            token, created = Token.objects.get_or_create(user=user)
            circles = get_circle_of_user(user)
            return JsonResponse({"success": True ,'token': token.key, "user": DUserSerializer(user).data, "circles": circles})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "message": e.__str__()})

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
        circles = get_circle_of_user(user)
        JsonResponse({"circles": circles}, safe=False)


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
        picture= request.data['picture']
        try:
            circle = Circle.objects.get(name=name)
        except:
            circle = False
        if circle:
            return JsonResponse({"success": False})
        circle = Circle.objects.create(name=name, explanation=explanation, picture=picture)
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

class PostList(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, pk, format=None):
        try:
            board = Board.objects.get(id=pk)
            title = request.data['title']
            content = request.data['content']
            user = DUser.objects.get(username=request.user)
            post = Post.objects.create(board=board, title=title, content=content, owner=user)
            circle = board.circle
            membership = MemberShip.objects.filter(circle=circle)
            members = [member.user for member in membership]
            for member in members:
                Read.objects.create(post=post, user=member)
            serializer = PostSerializer(post)
            return JsonResponse({"success": True, "post": serializer.data})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False})

    def get(self, request, pk, format=None):
        try:
            board = Board.objects.get(id=pk)
            posts = Post.objects.filter(board=board)
            serializer = PostSerializer(posts, many=True)
            return JsonResponse({"success": True, "post": serializer.data})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False})

class ReadMarking(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, pk, format=None):
        try:
            user = DUser.objects.get(username=request.user)
            post = Post.objects.get(id=pk)
            read = Read.objects.get(user=user, post=post)
            read.hasRead = True
            read.save()
            return JsonResponse({"success": True})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False})


class CommentList(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, pk, format=None):
        try:
            user = DUser.objects.get(username=request.user)
            post = Post.objects.get(id=pk)
            content = request.data['content']
            comment = Comment.objects.create(owner=user, post=post, content=content)
            return JsonResponse({"success": True})

        except Exception as e:
            print(e)
            return JsonResponse({"success": False})

    def get(self, pk, format=None):
        try:
            post = Post.objects.get(id=pk)
            comments = Comment.objects.filter(post=post)
            serializer = CommentSerializer(comments, many=True)
            return JsonResponse({"success": True, "comments": serializer.data})

        except Exception as e:
            print(e)
            return JsonResponse({"success": False})





class CommentDetail(APIView):

    def delete(self, comment_pk, format=None):
        try:
            comment = Comment.objects.get(id=comment_pk)
            comment.delete()

        except:
            return JsonResponse({"success": False})
        return JsonResponse({"success": True}, safe=False)




    def put(self, request, comment_pk, format=None):
        try:
            comment = Comment.objects.get(id=comment_pk)
            content = request.data['content']
            comment.content = content
            comment.save()
            return JsonResponse({"success": True, "content": comment.content})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False})


#기능 추가
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

def get_circle_of_user(user):
    membership = MemberShip.objects.filter(user=user)
    circles = []
    for m in membership:
        serializer = CircleSerializer(m.circle)
        data = serializer.data
        circles.append(data)

    return circles
