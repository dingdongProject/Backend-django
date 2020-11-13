from django.urls import path
from circle import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('signup', views.SignUp.as_view()),
    path('login',  obtain_auth_token),
    path('user', views.UserMine.as_view()),
    path('user/circles', views.UserCircles.as_view()),
    path('users/<slug:name>', views.UserDetail.as_view()),
    path('membership', views.MemberShipList.as_view()),
    path('circles', views.CircleList.as_view()),
    path('circles/<slug:name>', views.CircleDetail.as_view()),
    path('circles/<slug:name>/members', views.CircleMembers.as_view()),
    path('circles/<slug:circle>/boards', views.BoardList.as_view()),
    path('board/<int:pk>', views.BoardDetail.as_view()),
    path('board/<int:pk>/post', views.PostList.as_view()),
    path('post/<int:pk>/read', views.ReadMarking.as_view()),
    path('post/<int:pk>/comment', views.CommentList.as_view()),
    path('post/<int:pk>/comment/<int:comment_pk>', views.CommentDetail.as_view())

]