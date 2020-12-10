from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from circle.models import Circle, MemberShip, DUser, Board, Post, Read, Comment, PostImage, Schedule,Tag, CircleTag, Request
from circle.serializers import DUserSerializer, CircleSerializer, MemberShipSerializer, BoardSerializer, PostSerializer, CommentSerializer,PostSimpleSerializer, PostImageSerializer, UserImageSerializer, ScheduleSerializer
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
import datetime
import random, string
from django.db.models import Q


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
        try:
            user = DUser.objects.get(username=request.user)
            serializer = DUserSerializer(user)
            circles = get_circle_of_user(user)
            return JsonResponse({"success": True, "user": serializer.data, "circles": circles})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "message": e.__str__()})
    def put(self, request, format=None):
        try:
            user = DUser.objects.get(username=request.user)
            new_name = request.data['name']
            new_email = request.data['email']
            try:
                new_picture = request.data['picture']
            except:
                new_picture = user.picture
            user.email = new_email
            user.username = new_name
            user.picture = new_picture
            user.save()
            serializer = DUserSerializer(user)
            return JsonResponse({"success": True, "user": serializer.data})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "message": e.__str__()})



class MainPage(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        try:
            user = DUser.objects.get(username=request.user)
            memberships = MemberShip.objects.filter(user=user)
            circles = []
            for membership in memberships:
                circles.append(membership.circle)
            notice_board = Board.objects.filter(circle__in=circles, name='Notice')
            notice_posts = Post.objects.filter(board__in=notice_board).order_by('-created_at')
            other_boards = Board.objects.filter(Q(circle__in=circles) & ~Q(name='Notice') & ~Q(name='Gallery'))
            news_posts = Post.objects.filter(board__in=other_boards).order_by('-created_at')
            notice_data =[]
            news_data = []
            for post in notice_posts:
                commentObjects = Comment.objects.filter(post=post)
                images = PostImage.objects.filter(post=post)
                serializer = PostImageSerializer(images, many=True)
                comments = []
                try:
                    read = Read.objects.get(post=post, user=DUser.objects.get(
                        username=request.user)).hasRead if post.check_read else False
                except:
                    read = False
                for comment in commentObjects:
                    comments.append({
                        'content': comment.content,
                        'owner': UserImageSerializer(comment.owner).data,
                        'created_at': comment.created_at
                    })
                notice_data.append({
                    'title' : post.title,
                    'circle': CircleSerializer(post.board.circle).data,
                    'content' :  post.content,
                    'created': post.created_at,
                    'owner': UserImageSerializer(post.owner).data,
                    'id': post.id,
                    'board': post.board.id,
                    'images': serializer.data,
                    'comments': comments,
                    'check_read': post.check_read,
                    'hasRead': read
                })
            for post in news_posts:
                commentObjects = Comment.objects.filter(post=post)
                images = PostImage.objects.filter(post=post)
                serializer = PostImageSerializer(images, many=True)
                Userserializer = DUserSerializer(post.owner)
                comments = []
                for comment in commentObjects:
                    comments.append({
                        'content': comment.content,
                        'owner': UserImageSerializer(comment.owner).data,
                        'created_at': comment.created_at
                    })
                news_data.append({
                    'title': post.title,
                    'circle': CircleSerializer(post.board.circle).data,
                    'content': post.content,
                    'created': post.created_at,
                    'owner': UserImageSerializer(post.owner).data,
                    'id': post.id,
                    'board': post.board.id,
                    'images': serializer.data,
                    'comments': comments,
                    'check_read': post.check_read,
                    'hasRead': Read.objects.get(post=post, user=DUser.objects.get(
                        username=request.user)).hasRead if post.check_read else False
                })
            requestList = []
            for circle in circles:
                membership = MemberShip.objects.get(user=user, circle=circle)
                if membership.isAdmin:
                    requests = Request.objects.filter(circle=circle, isProcessed=False)
                    for request in requests:
                        requestList.append({
                            "requester": DUserSerializer(request.requester).data,
                            "circle": CircleSerializer(request.circle).data,
                            "isProcessed": request.isProcessed,
                            "id": request.id
                        })

            return JsonResponse({"success": True, "notices": notice_data, "news": news_data, "requests": requestList})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "message": e.__str__()})

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
            return JsonResponse({"success": False, "message": e.__str__()})

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
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "message": e.__str__()})


class CircleList(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        circles = Circle.objects.all()
        serializer = CircleSerializer(circles, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, format=None):
        try:
            name = request.data['name']
            explanation = request.data['explanation']
            try: picture = request.data['picture']
            except: picture = ""
            try: tags = request.data['tags'].split(" ")
            except: tags = []
            try: circle = Circle.objects.get(name=name)
            except: circle = False
            if circle:
                return JsonResponse({"success": False, "message": "circle Already Exist"})
            if picture == "":
                circle = Circle.objects.create(name=name, explanation=explanation)
            else:
                circle = Circle.objects.create(name=name, explanation=explanation, picture=picture)
            for tag in tags:
                tagExist = Tag.objects.filter(name=tag)
                if len(tagExist) != 0:
                    CircleTag.objects.create(circle=circle, tag=tagExist[0])
                else:
                    tagObject = Tag.objects.create(name=tag)
                    CircleTag.objects.create(circle=circle, tag=tagObject)
            random.seed = circle.id
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            circle.code = code
            circle.save()
            user = DUser.objects.get(username=request.user)
            MemberShip.objects.create(user=user, circle=circle, isAdmin=True,
                                      isActive=True)
            notice = Board.objects.create(name="Notice", circle=circle, memberWrite=False)
            Board.objects.create(name="Gallery", circle=circle)
            Post.objects.create(title="Welcome To {}".format(name),
                                content="Welcome! Invite members to the page and create new posts!", owner=user, board=notice)
            serializer = CircleSerializer(circle)
            return JsonResponse({"success": True, "circle": serializer.data}, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "message": e.__str__()})

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

class CircleInfo(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, code, format=None):
        try:
            circle = Circle.objects.get(code=code)
            serializer = CircleSerializer(circle)
            return JsonResponse({"success" : True, "circle" :serializer.data})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "message": e.__str__()})



class CircleMembers(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, name, format=None):
        circle = Circle.objects.get(name=name)
        membership = MemberShip.objects.filter(circle=circle)
        members = [{"name": member.user.username, "isAdmin": member.isAdmin} for member in membership]
        return JsonResponse({"members": members}, safe=False)

    def put(self, request, name, format=None):
        try:
            circle = Circle.objects.get(name=name)
            user_name = request.data['name']
            new_isadmin = request.data['isAdmin']
            user = DUser.objects.get(username=user_name)
            membership = MemberShip.objects.get(circle=circle, user=user)
            membership.isAdmin = new_isadmin
            membership.save()
            return JsonResponse({"success": True})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "message": e.__str__()})
class BoardList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, circle, format=None):
        try:
            circle = Circle.objects.get(name=circle)
            boards = Board.objects.filter(circle=circle)
            print(boards)
            boards = [{"id": board.id, "name": board.name, "memberWrite": board.memberWrite} for board in boards]
            return JsonResponse({"success": True, "boards": boards})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "message": e.__str__()})
    def post(self, request, circle, format=None):
        try:
            '''
            if not check_authorization(request.user, circle):
                return JsonResponse({"success": False})
            '''
            circle = Circle.objects.get(name=circle)
            board_name = request.data['name']
            board = Board.objects.create(name=board_name, circle=circle)
            return JsonResponse({"success": True, "board": {"id": board.id, "name": board.name, "memberWrite": board.memberWrite}})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False})

class GalleryDetail(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, circle, format=None):
        try:
            circleObj = Circle.objects.get(name=circle)
            board = Board.objects.get(circle=circleObj, name="Gallery")
            posts = Post.objects.filter(board=board)
            print(posts)
            postImages = PostImage.objects.filter(post=posts[0])
            print(postImages)
            postSerializer = PostImageSerializer(postImages[0])
            return JsonResponse({"success": True, "gallery": postSerializer.data})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "message": e.__str__(), "gallery": {"image":"https://dingdong-bucket.s3.ap-northeast-2.amazonaws.com/default-circle.png"}})

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
            return JsonResponse({"success": False, "message": e.__str__()})

class NoticeList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, circle, format=None):
        try:
            circle = Circle.objects.get(name=circle)
            board = Board.objects.filter(circle=circle, name="Notice")
            posts = Post.objects.filter(board=board[0]).order_by('-created_at')
            data = []
            for post in posts:
                commentObjects = Comment.objects.filter(post=post)
                images = PostImage.objects.filter(post=post)
                serializer = PostImageSerializer(images, many=True)
                comments = []
                for comment in commentObjects:
                    comments.append({
                        'content': comment.content,
                        'owner': UserImageSerializer(comment.owner).data,
                        'created_at': comment.created_at
                    })
                data.append({
                    'title': post.title,
                    'content': post.content,
                    'created': post.created_at,
                    'owner': UserImageSerializer(post.owner).data,
                    'circle': CircleSerializer(circle).data,
                    'id': post.id,
                    'board': post.board.id,
                    'images': serializer.data,
                    'comments': comments,
                    'check_read': post.check_read,
                    'hasRead': Read.objects.get(post=post, user=DUser.objects.get(
                        username=request.user)).hasRead if post.check_read else False
                })
            return JsonResponse({"success": True, "posts": data})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "message": e.__str__()})

class PostList(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, pk, format=None):
        try:
            board = Board.objects.get(id=pk)
            title = request.data['title']
            content = request.data['content']
            checkRead = request.data['check_read']
            if checkRead == "true": checkRead = True
            else: checkRead = False
            print(checkRead)
            images = []
            print(request.FILES.getlist('images[]'))
            print('images', images)
            for image in request.FILES.getlist('images[]'):
                print(image)
                images.append(image)

            print('images', images)
            user = DUser.objects.get(username=request.user)
            post = Post.objects.create(board=board, title=title, content=content, owner=user, check_read=checkRead)
            imageList = []
            for image in images:
                imageItem = PostImage.objects.create(post=post, image=image)
                imageList.append(imageItem)
            print('images', imageList)
            circle = board.circle
            membership = MemberShip.objects.filter(circle=circle)
            members = [member.user for member in membership]
            if checkRead:
                for member in members:
                    if member == user:
                        Read.objects.create(post=post, user=member, hasRead=True)
                    else:
                        Read.objects.create(post=post, user=member)
            images = PostImage.objects.filter(post=post)
            serializer = PostImageSerializer(images, many=True)
            data = {
                'title': post.title,
                'content': post.content,
                'created': post.created_at,
                'owner': UserImageSerializer(post.owner).data,
                'id': post.id,
                'board': post.board.id,
                'images': serializer.data,
                'check_read': checkRead,
                'hasRead': True
            }
            return JsonResponse({"success": True, "post": data})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "message": e.__str__()})

    def get(self, request, pk, format=None):
        try:
            board = Board.objects.get(id=pk)
            print(board)
            posts = Post.objects.filter(board=board).order_by('-created_at')
            print(posts)
            data = []


            for post in posts:
                commentObjects = Comment.objects.filter(post=post)
                images = PostImage.objects.filter(post=post)
                serializer = PostImageSerializer(images, many=True)
                comments = []
                for comment in commentObjects:
                    comments.append({
                        'content': comment.content,
                        'owner': UserImageSerializer(comment.owner).data,
                        'created_at': comment.created_at
                    })
                data.append({
                    'title' : post.title,
                    'content' :  post.content,
                    'created': post.created_at,
                    'owner': UserImageSerializer(post.owner).data,
                    'id': post.id,
                    'board': post.board.id,
                    'images': serializer.data,
                    'comments': comments,
                    'check_read': post.check_read,
                    'hasRead': Read.objects.get(post=post, user=DUser.objects.get(username=request.user)).hasRead if post.check_read else False
                })
                print(data)
            return JsonResponse({"success": True, "post": data})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "message": e.__str__()})




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
            return JsonResponse({"success": False, "message": e.__str__()})
    def get(self, request, pk, format=None):
        try:
            post = Post.objects.get(id=pk)
            reads = Read.objects.filter(post=post)
            data = []
            for read in reads:
                if read.hasRead:
                    data.append({
                        "user": UserImageSerializer(read.user).data,
                        "hasRead": read.hasRead
                    })
            for read in reads:
                if not read.hasRead:
                    data.append({
                        "user": UserImageSerializer(read.user).data,
                        "hasRead": read.hasRead
                    })
            return JsonResponse({"success": True, "list": data})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "message": e.__str__()})
class CommentList(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, pk, format=None):
        try:
            user = DUser.objects.get(username=request.user)
            post = Post.objects.get(id=pk)
            content = request.data['content']
            comment = Comment.objects.create(owner=user, post=post, content=content)
            return JsonResponse({"success": True, 'comment': {
                        'content': comment.content,
                        'owner': UserImageSerializer(comment.owner).data,
                        'created_at': comment.created_at
                    }})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "message": e.__str__()})

    def get(self, pk, format=None):
        try:
            post = Post.objects.get(id=pk)
            comments = Comment.objects.filter(post=post)
            serializer = CommentSerializer(comments, many=True)
            return JsonResponse({"success": True, "comments": serializer.data})

        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "message": e.__str__()})





class CommentDetail(APIView):

    def delete(self, comment_pk, format=None):
        try:
            comment = Comment.objects.get(id=comment_pk)
            comment.delete()


        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "message": e.__str__()})
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
            return JsonResponse({"success": False, "message": e.__str__()})

class ScheduleList(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        try:
            user = DUser.objects.get(username=request.user)
            memberships = MemberShip.objects.filter(user=user)
            circles = []
            for membership in memberships:
                circle = membership.circle
                circles.append(circle)
            schedules = []
            for circle in circles:
                schedule = Schedule.objects.filter(circle=circle)
                serializer = ScheduleSerializer(schedule, many=True)
                schedules.append({'circle': circle.name, 'scheduleList' :serializer.data})
            return JsonResponse({"success": True, 'schedules': schedules})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "message": e.__str__()})

    def post(self, request, format=None):
        try:
            name = request.data['circle']
            title = request.data['title']
            content = request.data['content']
            datetime_str = request.data['datetime']
            date_time_obj = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
            circle = Circle.objects.get(name=name)
            schedule = Schedule.objects.create(circle=circle, datetime=date_time_obj, title=title, content=content)
            serializer = ScheduleSerializer(schedule)
            return JsonResponse({"success": True, 'schedules': serializer.data})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "message": e.__str__()})



class MakeRequest(APIView):
    def post(self, request):
        try:
            circle_code = request.data['code']
            user = DUser.objects.get(username=request.user)
            circle = Circle.objects.get(code=circle_code)
            memberShip = MemberShip.objects.filter(user=user, circle=circle)
            if len(memberShip) != 0:
                return JsonResponse({"success": False, "message": "Already Joined"})
            requestExist = Request.objects.filter(requester=user, circle=circle)
            if len(requestExist) != 0:
                return JsonResponse({"success": False, "message": "Already Made Request"})
            Request.objects.create(requester=user, circle=circle)
            return JsonResponse({"success": True})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "message": e.__str__()})

class ProcessRequest(APIView):
    def post(self, request):
        try:
            request_id= request.data['id']
            accept = request.data['accept']
            requestObj = Request.objects.get(id=request_id)
            if accept:
                MemberShip.objects.create(user=requestObj.requester, circle=requestObj.circle)
            requestObj.isProcessed = True
            requestObj.save()
            return JsonResponse({"success": True})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "message": e.__str__()})


class CircleSearch(APIView):
    def get(self,request, search):
        try:
            if search == 'all':
                circles = Circle.objects.all()
                if len(circles) > 5:
                    circles = circles[:5]
                serializer = CircleSerializer(circles, many=True)
                return JsonResponse({"success": True, "circles": serializer.data})
            circlesNameObjects = Circle.objects.filter(name__startswith=search)
            circlesName = []
            for circle in circlesNameObjects:
                circlesName.append(circle)
            circlesCodeObjects = Circle.objects.filter(code=search)
            circlesCode = []
            for circle in circlesCodeObjects:
                circlesCode.append(circle)
            tags = Tag.objects.filter(name__startswith = search)
            circlesTag =[]
            for tag in tags:
                circle_tags =CircleTag.objects.filter(tag=tag)
                for circle_tag in circle_tags:
                    circlesTag.append(circle_tag.circle)
            serializer = CircleSerializer(circlesName + circlesCode + circlesTag, many=True)
            print(circlesName + circlesCode + circlesTag)
            return JsonResponse({"success": True, "circles": serializer.data})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "message": e.__str__()})



def getReqeusts(user):
    try:
        adminMemberships = MemberShip.objects.filter(user=user, isAdmin=True)
        requestList = []
        for mem in adminMemberships:
            circle = mem.circle
            requests = Request.objects.filter(circle=circle, isProcessed=False)
            for request in requests:
                requestList.append(request)
        return requestList
    except:
        return []


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
        data = dict(serializer.data)
        data['isAdmin'] = m.isAdmin
        circles.append(data)
    print(circles)

    return circles

def get_admin_circle(user):
    membership = MemberShip.objects.filter(user=user)
    circles = []
    for m in membership:
        if m.isAdmin:
            data = dict()
            data['circle'] = m.circle
            circles.append(data)
    print(circles)
    return circles
