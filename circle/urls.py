from django.urls import path
from circle import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('signup', views.SignUp.as_view()),
    path('login',  obtain_auth_token),
    path('users/', views.UserList.as_view()),
    path('users/<slug:name>/', views.UserDetail.as_view()),
    path('users/<slug:name>/circles/', views.UserCircles.as_view()),
    path('membership', views.MemberShipList.as_view()),
    path('circles/', views.CircleList.as_view()),
    path('circles/<slug:name>', views.CircleDetail.as_view()),
    path('circles/<slug:name>/members/', views.CircleMembers.as_view())
]