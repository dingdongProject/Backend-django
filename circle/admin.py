from django.contrib import admin
# Register your models here.
from circle.models import Circle, MemberShip, DUser, Schedule, Board, Post, Read, Comment, PostImage, Tag, CircleTag, Request

admin.site.register(Circle)
admin.site.register(DUser)
admin.site.register(MemberShip)
admin.site.register(Schedule)
admin.site.register(Board)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Read)
admin.site.register(PostImage)
admin.site.register(Tag)
admin.site.register(CircleTag)
admin.site.register(Request)