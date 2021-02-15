from django.urls import path
from .views import categorize_view, create_norme

app_name = 'categorize'
urlpatterns = [
    path('', categorize_view, name='categorize_view'),
    path('create-norme', create_norme, name='create_norme'),
]
