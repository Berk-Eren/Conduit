from django.contrib import admin
from .models import CustomUser, Profile

# Register your models here.
@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']
