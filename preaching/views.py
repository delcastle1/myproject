from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, UserLoginForm, GospelSongForm, PreachingSessionForm, PreacherRegistrationForm, UserRegistrationForm,AuthenticationForm
from .models import GospelSong, PreacherProfile, PreachingSession,CustomUser
from django.http import JsonResponse
from django.db.models import Count, Sum
from django.db.models.functions import ExtractMonth
import json
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import user_passes_test


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect_to_dashboard(user)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def upload_content(request):
    if request.method == 'POST':
        return redirect('home')
    else:
        return render(request, 'upload.html')

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    return render(request, 'contact.html')

@login_required
def schedule_session(request):
    if request.method == 'POST':
        form = PreachingSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.preacher = PreacherProfile.objects.get(user=request.user)
            session.save()
            return redirect('preaching_sessions')
    else:
        form = PreachingSessionForm()
    return render(request, 'schedule_session.html', {'form': form})

def artist_dashboard(request):
    songs = GospelSong.objects.filter(artist=request.user)
    song_count = songs.count()

    return render(request, 'dashboard/artist_dashboard.html', {
        'songs': songs,
        'song_count': song_count,
    })

@login_required
def statistics(request):
    if request.user.role != 'artist':
        return redirect('home')

    artist = request.user

    # Total number of songs uploaded by the artist
    total_songs = GospelSong.objects.filter(artist=artist).count()

    # Total number of downloads across all songs
    total_downloads = GospelSong.objects.filter(artist=artist).aggregate(total_downloads=Sum('download_count'))['total_downloads'] or 0

    # Example: Fetching data for trends (e.g., monthly uploads)
    monthly_uploads = GospelSong.objects.filter(artist=artist).annotate(month=ExtractMonth('upload_date')).values('month').annotate(count=Count('id'))

    # Prepare data for chart.js (example: monthly uploads)
    months = []
    counts = []
    for entry in monthly_uploads:
        months.append(entry['month'])
        counts.append(entry['count'])

    # Convert to JSON for passing into template
    months_json = json.dumps(months)
    counts_json = json.dumps(counts)

    return render(request, 'dashboard/statistics.html', {
        'total_songs': total_songs,
        'total_downloads': total_downloads,
        'months_json': months_json,
        'counts_json': counts_json,
    })

def main_dashboard(request):
    songs = GospelSong.objects.filter(artist=request.user)
    song_count = songs.count()

    return render(request, 'dashboard/main_dashboard.html', {
        'songs': songs,
        'song_count': song_count,
    })

def preacher_dashboard(request):
    return render(request, 'dashboard/preacher_dashboard.html')

def preaching_sessions(request):
    return render(request, 'dashboard/preaching_sessions.html')

def upload_preaching(request):
    return render(request, 'dashboard/upload_preaching.html')

def record_preaching(request):
    return render(request, 'dashboard/record_preaching.html')

@login_required
def admin_dashboard(request):
    songs = GospelSong.objects.all()
    preachings = PreachingSession.objects.all()
    
    context = {
        'songs': songs,
        'preachings': preachings
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get('role')
            user.save()
            if role == 'preacher':
                user.is_preacher = True
            elif role == 'artist':
                user.is_artist = True
            user.save()
            login(request, user)
            return redirect_to_dashboard(user)
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})
def redirect_to_dashboard(user):
    if user.is_staff:
        return redirect('admin_dashboard')
    elif user.is_preacher:
        return redirect('preacher_dashboard')
    elif user.is_artist:
        return redirect('artist_dashboard')
    else:
        return redirect('home')

def trending(request):
 return render(request,  'trending.html')

def popular(request):
 return render(request,  'popular.html')

def new(request):
 return render(request,  'new.html')

def recent(request):
 return render(request,  'recent.html')

def search(request):
 return render(request,  'search.html')


def downloads(request):
    return render(request, 'downloads.html')

@login_required
def upload_gospel_song(request):
    if request.method == 'POST':
        form = GospelSongForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save(commit=False)
            song.artist = request.user
            song.save()
            return redirect('artist_dashboard')
    else:
        form = GospelSongForm()
    
    return render(request, 'upload_gospel_song.html', {'form': form})

def gospel_songs(request):
    songs = GospelSong.objects.filter(is_approved=True)
    return render(request, 'gospel_songs.html', {'songs': songs})



def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin_approve_songs(request):
    songs = GospelSong.objects.filter(is_approved=False)
    return render(request, 'admin_approve_songs.html', {'songs': songs})

@login_required
def update_song_status(request, song_id):
    song = get_object_or_404(GospelSong, id=song_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        song.status = status
        song.save()
        messages.success(request, 'Song status updated successfully!')
    return redirect('admin_dashboard')

@login_required
def delete_song(request, song_id):
    song = get_object_or_404(GospelSong, id=song_id)
    if request.method == 'POST':
        song.delete()
        messages.success(request, 'Song deleted successfully!')
    return redirect('admin_dashboard')