from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, GospelSong, PreacherProfile, PreachingSession

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_preacher', 'is_artist']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(GospelSong)
admin.site.register(PreacherProfile)
admin.site.register(PreachingSession)
