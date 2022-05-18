from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User
# Register your models here.
# admin.site.unregister(User)
admin.site.register(User)
