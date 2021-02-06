from django.shortcuts import render

def organize_view(request, *args, **kwargs):
    return render(request, 'organize.html', {})
