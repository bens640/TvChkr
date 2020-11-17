from django.contrib import admin
from .models import Profile, Group, Membership

admin.site.register(Profile)
admin.site.register(Group)
admin.site.register(Membership)