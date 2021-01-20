from django.shortcuts import render

def visualize_view(request, *args, **kwargs):
    return render(request, 'visualize.html', {})
