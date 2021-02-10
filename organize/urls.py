from django.urls import path
from .views import organize_view, create_new_dir, search_key_words #, get_ul_elements

app_name = 'organize'
urlpatterns = [
    path('', organize_view, name='organize'),
    path('search_key_words', search_key_words, name='search_key_words'),
    # path('get_ul_elements', get_ul_elements, name='get_ul_elements'),
    path('create_new_directory_annotator', create_new_dir, name='create_directory'),
]
