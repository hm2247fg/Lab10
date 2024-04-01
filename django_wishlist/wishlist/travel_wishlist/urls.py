from django.urls import path
from . import views

# URL patterns for the travel wishlist application
urlpatterns = [
    # URL pattern for the home page showing the list of places
    path('', views.place_list, name='place_list'),
    # URL pattern for the visited page showing the list of visited places
    path('visited', views.places_visited, name='places_visited'),
    # URL pattern for marking a place as visited
    path('place/<int:place_pk>/was_visited/', views.place_was_visited, name='place_was_visited')
]