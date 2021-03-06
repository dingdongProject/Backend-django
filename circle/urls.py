from django.urls import path
from circle import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('ping', views.Ping.as_view()),
    path('signup', views.SignUp.as_view()),
    path('login',  views.LogIn.as_view()),
    path('user', views.UserMine.as_view()),
    path('user/circles', views.UserCircles.as_view()),
    path('users/<slug:name>', views.UserDetail.as_view()),
    path('membership', views.MemberShipList.as_view()),
    path('circles', views.CircleList.as_view()),
    path('circleInfo/<slug:code>', views.CircleInfo.as_view()),
    path('circles/<slug:name>', views.CircleDetail.as_view()),
    path('circles/<slug:name>/members', views.CircleMembers.as_view()),
    path('circles/<slug:circle>/boards', views.BoardList.as_view()),
    path('circles/<slug:circle>/gallery', views.GalleryDetail.as_view()),
    path('circles/<slug:circle>/notices', views.NoticeList.as_view()),
    path('circles/<slug:circle>/schedules', views.ScheduleList.as_view()),
    path('schedules', views.ScheduleList.as_view()),
    #path('schedules/<slug:circle>', views.ScheduleList.as_view()),
    path('board/<int:pk>', views.BoardDetail.as_view()),
    path('board/<int:pk>/post', views.PostList.as_view()),
    path('post/<int:pk>/read', views.ReadMarking.as_view()),
    path('post/<int:pk>/comment', views.CommentList.as_view()),
    path('post/<int:pk>/comment/<int:comment_pk>', views.CommentDetail.as_view()),
    path('request', views.MakeRequest.as_view()),
    path('respond', views.ProcessRequest.as_view()),
    path('circlesearch/<slug:search>', views.CircleSearch.as_view()),
    path('main', views.MainPage.as_view())
]