from django.http import HttpResponse #, HttpResponseRedirect
# from django.urls import reverse
from django.shortcuts import render
# from os import walk
from os.path import basename
from annotate.models import (Ville as ville, Juridiction as juridiction)
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

def annotate_view(request, directory=None, *args, **kwargs):
    # print(request.path)
    if 'read' in request.path:
        # print("Mohamed")
        response = read_file(request)
        return response
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
    {"files": files, 'file_list_len': len(files),})
    
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

from json import loads
def read_file(request ):
    ## TODO : request file name from data base and get all extracted fields
    # f = open(hp.files.treated_files_folder + file, 'r')
    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)
    file = body['path']
    file_name = body['file_name']
    f = open(file, 'r', encoding='utf-8')
    file_content = f.read()
    f.close()
    if (request.method == 'POST'):
        print('Mohamed')
        print('Mohamed ', file_name)
        # print(file_content)
    ## TO CHANGE (more optimised) ##
    file_name = file_name.split('.')[0].split('-')
    try:
        city = ville.objects.filter(zip_code=file_name[1])[0].ville
    except:
        city = ''
    try:
        juridic = juridiction.objects.filter(abbreviation= file_name[0], zip_code__isnull=True)[0].type_juridiction
    except:
        juridic = ''
    rg = file_name[2]
    context = {
        'city': city,
        'juridiction': juridic,
        'rg': rg,
        'file': file_content
    }
    data = json.dumps(context)
    # data = json.dumps({"Here": "Mohamed"})
    return HttpResponse(data, content_type='application/json')
