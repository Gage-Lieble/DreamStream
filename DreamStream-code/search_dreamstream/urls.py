from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # SEARCH FUNCTION
    path('results/', views.results, name='results') # RESULTS
]