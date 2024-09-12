from django.contrib import admin
from .models import Profile
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_role', 'name', 'lab_type')
    search_fields = ('user__username', 'name')
    list_filter = ('user_role', 'lab_type')