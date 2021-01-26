from django.urls import path , re_path
from .views import annotate_view, read_file#, return_new_decision_form#,read_file

app_name = 'annotate'
urlpatterns = [
    path('', annotate_view, name='annotate'),
    # re_path(r'^read.*', read_file, name='read_file'),
    path('read/<str:file>', read_file, name='read'),
    #path('new_decision_form', return_new_decision_form, name='new_decision_form' )
    #url(r'^add/(?P<id>\d+)/$', views.addview, name='add'),
    # re_path(r'^(?P<path>.*)/$', annotate_view),
    # path('test/', read_file, name='test'),
]
