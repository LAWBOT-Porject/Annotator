from django.shortcuts import render

def categorize_view(request):
    return render(request, 'categorize.html', {})
