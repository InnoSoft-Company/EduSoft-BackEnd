from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.contrib import admin
from .models import *

User = get_user_model()

class UserAdmin(BaseUserAdmin):
  def save_model(self, request, obj, form, change):
    obj.username, obj.email = obj.username.lower(), obj.email.lower()
    super().save_model(request, obj, form, change)

admin.site.register(User, UserAdmin)
admin.site.register(OAuth)