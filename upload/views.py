#from django.http.response import HttpResponse, HttpResponseRedirect
from .forms import UploadFileForm
from django.shortcuts import render
import time
from os import walk
from config.hparam import hparam as hp
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
                    new_file_name =  first_annotation[0].split('-')
                    zip_code = new_file_name[1]
                    juridiction_abr = new_file_name[0]
                    # Slice just before '.txt'
                    rg = new_file_name[2]
                    uuid =  new_file_name[3]
                    """ zip_code = new_file_name[5:10]
                    juridiction_abr = new_file_name[:4]
                    # Slice just before '.txt'
                    rg = new_file_name[11:-4] """
                    current_user = request.user
                    ## DONE : Treat the case of 00000 zipcode => Assign just the juridiction type without city
                    # If we know which city
                    if (zip_code != '00000'):
                        # Try to get the tribunal of the decision zip code and juridiction abr
                        try :
                            jurid = juridiction.objects.filter(zip_code__zip_code=zip_code, abbreviation=juridiction_abr)[0]
                        # If there is no result we should create a new one with the decision juridiction type and zip code
                        except IndexError:
                            # Search the type that is associated to the given abr and where the zip code is null
                            try:
                                type_jurid = juridiction.objects.filter(abbreviation= juridiction_abr, zip_code__isnull=True)[0]
                                type_jurid = type_jurid.type_juridiction
                            except IndexError:
                                type_jurid = ''
                            try:
                                # Search the city field that has the associated zip code
                                city = ville.objects.filter(zip_code=zip_code)[0]
                            except IndexError:
                                city = ''
                            if city == '' or type_jurid == '':
                                jurid=None
                            else:
                                new_juridiction = juridiction(type_juridiction=type_jurid, 
                                                            abbreviation=juridiction_abr,
                                                            zip_code=city)
                                new_juridiction.save()
                                jurid = new_juridiction
                    else :
                        # Link with the general juridictions that have no zip code
                        try:
                            jurid = juridiction.objects.filter(abbreviation= juridiction_abr, zip_code__isnull=True)[0]
                        except IndexError:
                            jurid=None
                            """ 
                    try:
                        # If there is no exception raised that means we already have this decision (Because .get raises Entry.DoesNotExist exception if there is no record found)
                        all_decisions = Decision.objects.filter(rg=rg).filter(uuid=uuid)
                        decision_exists = all_decisions.get(juridiction_id=jurid)
                    except Decision.DoesNotExist: """
                    new_decision = Decision(rg= rg,
                                            uuid= uuid,
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


