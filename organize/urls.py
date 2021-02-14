from django.urls import path
from .views import organize_view, create_new_dir, search_key_words, move_files, annotate_view #, get_ul_elements
# from annotate.views import annotate_view
app_name = 'organize'
urlpatterns = [
    path('', organize_view, name='organize'),
    path('search_key_words', search_key_words, name='search_key_words'),
    path('move_files', move_files, name='move_files'),
    # path('annotate/<str:directory>', annotate_view, name='annotate_view'),
    path('annotate', annotate_view, name='annotate_view'),
    # path('get_ul_elements', get_ul_elements, name='get_ul_elements'),
    path('create_new_directory_annotator', create_new_dir, name='create_directory'),
]
