#from django.http import HttpResponse

from django.shortcuts import render

def annotate_view(request, *args, **kwargs):
    #return HttpResponse('Annotateur sera bien tot disponible')
    return render(request, 'annotate.html', {})
