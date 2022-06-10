from django.urls import path
from . import views

app_name = 'search_app'
urlpatterns = [
    path('', views.index, name='index'), # SEARCH FUNCTION
    path('results/', views.results, name='results'), # RESULTS
    path('similar-result/<str:sim>', views.similar_results, name='similar_results')
    
]

handler404 = "search_dreamstream.views.handle_not_found"