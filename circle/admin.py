from django.contrib import admin
# Register your models here.
from circle.models import Circle, MemberShip, DUser, Schedule, Board, Post, Comment, Read


admin.site.register(Circle)
admin.site.register(DUser)
admin.site.register(MemberShip)
admin.site.register(Schedule)
admin.site.register(Board)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Read)