#from django.http.response import HttpResponse, HttpResponseRedirect
from .forms import UploadFileForm
from django.shortcuts import render
from helpers.upload_utilities import (
    handle_uploaded_file,
    verify_file_type,
    convert_to_txt
    )

# Upload view
def upload_view(request, *args, **kwargs):
    form = UploadFileForm()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')
        unallowed_files = 0
        if form.is_valid():
            for f in files:
                # Verify if the uploaded file types are allowed
                if verify_file_type(f.name):
                    # Save the file only if its extention is allowed
                    handle_uploaded_file(f, f.name)
                    convert_to_txt(f.name)
                else :
                    # Otherwise remove it from the uploaded files list
                    unallowed_files += 1
            return render(request, 'response.html', 
            {'number_files': (len(files) - unallowed_files)} )
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


