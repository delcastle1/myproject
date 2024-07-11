from django.db.models import Count, Sum
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import QuizForm, UserLoginForm, UserRegistrationForm, GospelSongForm, PreachingSessionForm
from .models import GospelSong, Preacher, PreachingSession
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from .models import Visitor
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from preaching.models import GospelSong, Visitor
from django.db.models import Count, Sum
import json
from django.db.models.functions import ExtractMonth

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            role = form.cleaned_data['role']

            # Create the user
            user = User.objects.create_user(username=username, password=password)

            # Log in the user after registration
            login(request, user)

            # Redirect based on user role
            if role == 'preacher':
                return redirect('preacher_dashboard')
            elif role == 'artist':
                return redirect('artist_dashboard')
            elif role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('home')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('admin_dashboard')
                elif user.groups.filter(name='preacher').exists():
                    return redirect('preacher_dashboard')
                elif user.groups.filter(name='artist').exists():
                    return redirect('artist_dashboard')
                else:
                    return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})

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
def upload_content(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'upload_content.html')

@login_required
def upload_gospel_song(request):
    if request.method == 'POST':
        form = GospelSongForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save(commit=False)
            song.artist = request.user.username  # Assign the current user as the artist
            song.save()
            return redirect('artist_dashboard')  # Redirect to artist dashboard after successful upload
    else:
        form = GospelSongForm()
    
    return render(request, 'upload_gospel_song.html', {'form': form})

def gospel_songs(request):
    songs = GospelSong.objects.all()
    return render(request, 'gospel_songs.html', {'songs': songs})

def bible_studies(request):
    return render(request, 'bible_studies.html')

def bible_training(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bible_training')
    else:
        form = QuizForm()
    return render(request, 'bible_training.html', {'form': form})

@login_required
def mindeducation(request):
    return render(request, 'marriage.html')

@login_required
def schedule_session(request):
    if request.method == 'POST':
        form = PreachingSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.preacher = Preacher.objects.get(user=request.user)
            session.save()
            return redirect('preaching_sessions')
    else:
        form = PreachingSessionForm()
    return render(request, 'schedule_session.html', {'form': form})




def artist_dashboard(request):
    # Fetch data as needed for the artist dashboard
    songs = GospelSong.objects.filter(artist=request.user)
    song_count = songs.count()

    return render(request, 'dashboard/artist_dashboard.html', {
        'songs': songs,
        'song_count': song_count,
    })

@csrf_exempt
def increment_visitor_count(request, artist_id):
    artist = get_object_or_404(User, id=artist_id)
    visitor, created = Visitor.objects.get_or_create(artist=artist)
    visitor.count += 1
    visitor.save()
    return JsonResponse({'status': 'success', 'visitor_count': visitor.count})



@login_required
def downloads(request):
    if request.user.userprofile.role != 'artist':
        return redirect('home')

    # Implement your download logic here
    return render(request, 'dashboard/downloads.html')
@login_required
def statistics(request):
    if request.user.userprofile.role != 'artist':
        return redirect('home')

    artist = request.user

    # Total number of songs uploaded by the artist
    total_songs = GospelSong.objects.filter(artist=artist).count()

    # Total number of visitors who have accessed the artist's songs
    total_visitors = Visitor.objects.filter(artist=artist).count()

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
        'total_visitors': total_visitors,
        'total_downloads': total_downloads,
        'months_json': months_json,
        'counts_json': counts_json,
    })

def main_dashboard(request):
    # Retrieve Gospel songs uploaded by the current user
    songs = GospelSong.objects.filter(artist=request.user)
    
    # Example: Other data you may want to display on the main dashboard
    song_count = songs.count()
    
    return render(request, 'dashboard/main_dashboard.html', {
        'songs': songs,
        'song_count': song_count,
        # Add other context variables as needed
    })



def preacher_dashboard(request):
    return render(request, 'dashboard/preacher_dashboard.html')

def preaching_sessions(request):
    # Add logic to handle preaching sessions
    return render(request, 'dashboard/preaching_sessions.html')

def upload_preaching(request):
    # Handle uploading of preaching sessions
    if request.method == 'POST':
        # Handle form submission and saving
        pass  # Add your implementation here
    return render(request, 'dashboard/upload_preaching.html')

def record_preaching(request):
    # Handle recording of preaching sessions
    if request.method == 'POST':
        # Handle form submission and saving
        pass  # Add your implementation here
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

@login_required
def update_song_status(request, song_id):
    if request.method == 'POST':
        status = request.POST.get('status')
        song = GospelSong.objects.get(pk=song_id)
        song.status = status
        song.save()
        messages.success(request, 'Song status updated successfully')
    return redirect('admin_dashboard')

@login_required
def update_preaching_status(request, preaching_id):
    if request.method == 'POST':
        status = request.POST.get('status')
        preaching = PreachingSession.objects.get(pk=preaching_id)
        preaching.status = status
        preaching.save()
        messages.success(request, 'Preaching status updated successfully')
    return redirect('admin_dashboard')