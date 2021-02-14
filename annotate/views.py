from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
# from os import walk
from os.path import basename
#from .forms import decisionInfo,decisionForm, PartiePhysiqueForm
from config.hparam import hparam as hp
from helpers.upload_utilities import (
            search_city_asraw, 
            # search_juridiction_asraw,
            # search_reference,
            full_juridiction
            )
import json
from annotate.models import Decision
#from django.conf import settings

treated_files_folder = hp.files.treated_files_folder

def annotate_view(request, directory=None):
    files = []
    selected_dir = treated_files_folder
    if (directory != None):
        selected_dir = directory
    decisions = Decision.objects.filter(decision_treated_path__contains = selected_dir)
    for item in decisions:
        tmp = []
        decision_path = item.decision_treated_path
        tmp.append(basename(decision_path))
        tmp.append(decision_path)
        files.append(tmp)
    return render(request, 'annotate.html', 
    {"files": files})
    
    # for (dirpath, dirnames, filenames) in walk(hp.files.treated_files_folder):
    #     files.extend(filenames)
    """ if (request.method == 'POST'):
        print('hello')
    if (request.method == 'GET'):
        print('hello1') """
    # return render(request, 'annotate.html', {'files' : sorted(files), 
    #                                         'file_list_len': len(files),
    #                                         #'infos': infos,
    #                                         #'decision': decision,
    #                                         #'personne': personnePhysiqueForm,
    #                                         # 'root_path': settings.FILES_DIR})
    #                                         #  'root_path': hp.files.treated_files_folder
    #                                         })

def read_file(request , file):
    ## TODO : request file name from data base and get all extracted fields
    # f = open(hp.files.treated_files_folder + file, 'r')
    f = open(file, 'r')
    file_content = f.read()
    f.close()
    ## TO CHANGE (more optimised) ##
    file = file.split('.')[0]
    city = search_city_asraw(file_content, hp.files.static_data_folder 
                                                    + hp.files.cities_file_name)
    juridiction = full_juridiction(file[:4]).capitalize()
    rg = file[7:]
    context = {
        'city': city,
        'juridiction': juridiction,
        'rg': rg,
        'file': file_content
    }
    data = json.dumps(context)
    return HttpResponse(data, content_type='application/json')
