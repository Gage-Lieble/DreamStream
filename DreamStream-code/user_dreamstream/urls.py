from django.urls import path
from . import views

app_name = 'dream_users'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),
    path('addfavorites/<str:fav>/<str:posterimg>/', views.add_fav, name='add_fav'),
    ]