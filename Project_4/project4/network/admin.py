from django.contrib import admin
from .models import User, Post,Following_System

admin.site.register(Post)
admin.site.register(User)
admin.site.register(Following_System)