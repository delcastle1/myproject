from django.urls import path
from . import views
from .views import delete_song

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('upload/', views.upload_content, name='upload_content'),
    path('gospel_songs/', views.gospel_songs, name='gospel_songs'),
    path('upload_gospel_song/', views.upload_gospel_song, name='upload_gospel_song'),
    path('schedule_session/', views.schedule_session, name='schedule_session'),
    path('preacher_dashboard/', views.preacher_dashboard, name='preacher_dashboard'),
    path('artist_dashboard/', views.artist_dashboard, name='artist_dashboard'),
    path('statistics/', views.statistics, name='statistics'),
    path('main_dashboard/', views.main_dashboard, name='main_dashboard'),
    path('preaching_sessions/', views.preaching_sessions, name='preaching_sessions'),
    path('upload_preaching/', views.upload_preaching, name='upload_preaching'),
    path('record_preaching/', views.record_preaching, name='record_preaching'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('update_song_status/<int:song_id>/', views.update_song_status, name='update_song_status'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('delete_song/<int:song_id>/', delete_song, name='delete_song'),
    path('trending/', views.trending, name='trending'),
    path('popular/', views.popular, name='popular'),
    path('new/', views.new, name='new'),
    path('recent/', views.recent, name='recent'),
    path('search/', views.search, name='search'),
    path('gospel_songs/', views.gospel_songs, name='gospel_songs'),
    path('register/', views.register, name='register'),
    path('downloads/', views.downloads, name='downloads'),
    path('approve_songs/', views.admin_approve_songs, name='admin_approve_songs'),
    

]
