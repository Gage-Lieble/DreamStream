from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static
app_name = 'dream_users'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),
    path('addfavorites/<str:fav>/<str:posterimg>/', views.add_fav, name='add_fav'),
    path('delete/<int:fav_id>', views.delete_fav, name='delete_fav')
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)