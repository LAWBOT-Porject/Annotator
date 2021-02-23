from django.urls import path
from .views import (annotate_view, read_file,
                    get_category_by_nppac) #submit_demand

app_name = 'annotate'
urlpatterns = [
    path('<str:directory>', annotate_view, name='annotate'),
    path('', annotate_view, name='annotate'),
    path('read', read_file, name='read'),
    # path('submit_individual_demande/<int:tab_idx>', submit_demand, name='submit_demand'),
    path('get_default_category', get_category_by_nppac, name='get_default_category'),
]
