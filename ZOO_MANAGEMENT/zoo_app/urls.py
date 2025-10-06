from django.urls import path
from . import views

urlpatterns = [
    path('enclosures/', views.enclosure_view, name = 'enclosures'),
    path('animals/', views.animal_view, name = 'animals'),
    path('foods/', views.food_view, name = 'foods'),
    path('feedRecords/', views.feedRecords_view, name = 'feedRecords'),
    path('managers/', views.manager_view, name = "managers")
]
