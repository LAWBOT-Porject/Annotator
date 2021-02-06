#from django.http.response import HttpResponse, HttpResponseRedirect
from .forms import UploadFileForm
from django.shortcuts import render
import time
from annotate.models import Decision, Juridiction as juridiction
from annotate.models import Ville as ville
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
                    upload_path = handle_uploaded_file(f, f.name)
                    first_annotation = convert_to_txt(upload_path, f.name)
                    new_file_name =  first_annotation[0]
                    zip_code = new_file_name[5:10]
                    juridiction_abr = new_file_name[:4]
                    # Slice just before '.txt'
                    rg = new_file_name[11:-4]
                    current_user = request.user
                    #print (current_user.id)
                    all_juridictions = juridiction.objects.filter(zip_code__zip_code=zip_code)
                    try :
                        jurid = all_juridictions.get(abbreviation=juridiction_abr)
                    except:
                        type_jurid = juridiction.objects.get(abbreviation= juridiction_abr)
                        type_jurid = type_jurid.type_juridiction
                        try:
                            city = ville.objects.get(zip_code=zip_code)
                        except :
                            city = None
                        new_juridiction = juridiction(type_juridiction=type_jurid, 
                                                    abbreviation=juridiction_abr,
                                                    zip_code=city)
                        new_juridiction.save()
                        jurid = new_juridiction
                    try:
                        all_decisions = Decision.objects.filter(rg=rg)
                        decision_exists = all_decisions.get(juridiction_id=jurid)
                    except:
                        new_decision = Decision(rg= rg, 
                                                rg_position=first_annotation[1],
                                                zip_code_position=first_annotation[2],
                                                juridiction_position=first_annotation[3],
                                                texte_decision=first_annotation[4],
                                                decision_original_path=upload_path,
                                                decision_treated_path=first_annotation[5],
                                                uploader_id=current_user,
                                                juridiction_id=jurid,)
                        new_decision.save()
                else :
                    # Otherwise remove it from the uploaded files list
                    unallowed_files += 1
        return render(request, 'response.html', {
            'number_files': (len(files) - unallowed_files),
            })
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


