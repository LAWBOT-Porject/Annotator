from django.urls import path
from .views import categorize_view

app_name = 'categorize'
urlpatterns = [
    path('', categorize_view, name='categorize_view'),
]
