from django.shortcuts import render
from .forms import *
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import *
# Login/Signup functions
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def signup(request):
   # Displays before form input
    if request.method == 'GET':
        form = SignUpForm()
        usern = request.user
        context = {'form': form, 'usern': str(usern)}
        return render(request, 'user_dreamstream/signup.html', context)
    # Creates a new User
    elif request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            
            user = User.objects.create_user(
                username = form.cleaned_data['username'],
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                password = form.cleaned_data['password'],
                email = form.cleaned_data['email'],
            )
            prof_det = ProfileDetails.objects.create(
                user=user
            )
            #Logs user in after sign up
            new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, new_user)
        return HttpResponseRedirect(reverse('dream_users:profile'))


def user_login(request):
    # Displays login form
    if request.method == 'GET':
        usern = request.user
        context = {'log_form': LoginForm(), 'usern': str(usern)}
        return render(request, 'user_dreamstream/login.html', context)
    # Logs in user
    elif request.method == 'POST':
        log_form = LoginForm(request.POST)
        if log_form.is_valid():
            password = log_form.cleaned_data['password'] # Clears any empty spaces and removes them
            user =  authenticate(request, username=log_form.cleaned_data['username'], password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('dream_users:profile'))
            else:
                # Checks if user exists
                log_form.add_error('username', 'Invalid email or password')
                return render(request, 'user_dreamstream/login.html', {'log_form': log_form})
            
def profile(request):
    if str(request.user) == 'AnonymousUser': # Checks if the user is logged in
        return HttpResponseRedirect(reverse('dream_users:login'))
    else:
        # Displays profile info and details
        fav_movies = FavMovies.objects.all().filter(fav_user=request.user)
        num_favs = len(list(fav_movies))
        usern = request.user
        context = {'usern': str(usern), 'favs': fav_movies, 'numfav': num_favs}
        return render(request, 'user_dreamstream/profile.html', context)


def profile_settings(request):

    user_detail = request.user.profiledetails
    form = ChangePfpForm(instance=user_detail)
    if request.method == "POST":
        form = ChangePfpForm(request.POST, request.FILES ,instance=user_detail)
        if form.is_valid():
            form.save()
        else: #Checks if form is valid (if image size is a square)
           
            context = {'changeform': form}
            return render(request, 'user_dreamstream/settings.html', context)
        return HttpResponseRedirect(reverse('dream_users:profile'))
    context = {'changeform': form}
    return render(request, 'user_dreamstream/settings.html', context)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('dream_users:login'))


def add_fav(request, fav, posterimg):
    favmovs = FavMovies.objects.all().filter(fav_user=request.user)
    
    if fav not in str(favmovs): # Checks if movie is already in the users favorites list
        form = FavMovies(fav_user=request.user, title=fav, poster_img='https://cdn.watchmode.com/posters/'+posterimg)
        form.save()
    return HttpResponseRedirect(reverse('dream_users:profile'))

def delete_fav(request, fav_id):
    if FavMovies.objects.filter(id=fav_id).exists():
        favorite = FavMovies.objects.get(id=fav_id)
        favorite.delete()
    return HttpResponseRedirect(reverse('dream_users:profile'))