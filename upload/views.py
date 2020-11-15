#from django.http.response import HttpResponse, HttpResponseRedirect
from .forms import UploadFileForm
from django.shortcuts import render
from config.hparam import hparam as hp

# Upload view
def upload_view(request, *args, **kwargs):
    form = UploadFileForm()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')
        if form.is_valid():
            for f in files:
                handle_uploaded_file(f, f.name)
            return render(request, 'success.html', 
            {'number_files': len(files)} )
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def handle_uploaded_file(f, name):
    with open( hp.upload.folder + name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
