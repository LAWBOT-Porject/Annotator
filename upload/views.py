from django.http.response import HttpResponse, HttpResponseRedirect
from .forms import UploadFileForm
from django.shortcuts import render

# Upload view
def upload_view(request, *args, **kwargs):
    form = UploadFileForm()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')
        if form.is_valid():
            for f in files:
                handle_uploaded_file(f, f.name)
            return HttpResponse('Fichiers uplodes avec succes!')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def handle_uploaded_file(f, name):
    with open('upload/files_uploaded/' + name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
