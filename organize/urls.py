from django.urls import path
from .views import organize_view, create_new_dir

app_name = 'organize'
urlpatterns = [
    path('', organize_view, name='organize'),
    path('create_new_directory_annotator', create_new_dir, name='create'),
]
