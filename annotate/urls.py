from django.urls import path , re_path
from .views import annotate_view, read_file#,read_file

app_name = 'annotate'
urlpatterns = [
    path('', annotate_view, name='annotate'),
    # re_path(r'^read.*', read_file, name='read_file'),
    path('read/<str:file>', read_file, name='read'),
    #url(r'^add/(?P<id>\d+)/$', views.addview, name='add'),
    # re_path(r'^(?P<path>.*)/$', annotate_view),
    # path('test/', read_file, name='test'),
]
