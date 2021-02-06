from django.urls import path
from .views import organize_view

app_name = 'organize'
urlpatterns = [
    path('', organize_view, name='organize'),    
]
