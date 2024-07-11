from django.contrib import admin
from .models import GospelSong, Quiz, Preacher,PreachingSession

admin.site.register(GospelSong)
admin.site.register(Quiz)
admin.site.register(Preacher)

admin.site.register(PreachingSession)
