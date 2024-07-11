from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.user_register, name='register'),
    path('upload/', views.upload_content, name='upload_content'),
    path('gospel_songs/', views.gospel_songs, name='gospel_songs'),
    path('bible_studies/', views.bible_studies, name='bible_studies'),
    path('upload_gospel_song/', views.upload_gospel_song, name='upload_gospel_song'),
    path('bible_training/', views.bible_training, name='bible_training'),
    path('marriage/', views.mindeducation, name='marriage'),
    path('schedule_session/', views.schedule_session, name='schedule_session'),
    path('preacher_dashboard/', views.preacher_dashboard, name='preacher_dashboard'),
    path('artist_dashboard/', views.artist_dashboard, name='artist_dashboard'),
    path('downloads/', views.downloads, name='downloads'),
    path('statistics/', views.statistics, name='statistics'),
    path('main_dashboard/', views.main_dashboard, name='main_dashboard'),
    path('preaching_sessions/', views.preaching_sessions, name='preaching_sessions'),
    path('upload_preaching/', views.upload_preaching, name='upload_preaching'),
    path('record_preaching/', views.record_preaching, name='record_preaching'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('update_song_status/<int:song_id>/', views.update_song_status, name='update_song_status'),
    path('update_preaching_status/<int:preaching_id>/', views.update_preaching_status, name='update_preaching_status'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

]
