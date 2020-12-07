#from django.http.response import HttpResponse, HttpResponseRedirect
from .forms import UploadFileForm
from django.shortcuts import render
from helpers.upload_utilities import handle_uploaded_file

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


