from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from network.models import Post,User

# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass

admin.site.register(Post)  # This is valid and works with default settings
