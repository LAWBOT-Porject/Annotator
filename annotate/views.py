from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from os import walk
from .forms import decisionInfo,decisionForm, PartiePhysiqueForm
from config.hparam import hparam as hp
from helpers.upload_utilities import (
            search_city_asraw, 
            search_juridiction_asraw,
            search_reference,
            full_juridiction
            )
import json
#from django.conf import settings


def annotate_view(request, *args, **kwargs):
    files = []
    infos = decisionInfo()#auto_id=False)
    decision= decisionForm()
    personnePhysiqueForm = PartiePhysiqueForm()
    for (dirpath, dirnames, filenames) in walk(hp.files.treated_files_folder):
        files.extend(filenames)
    """ if (request.method == 'POST'):
        print('hello')
    if (request.method == 'GET'):
        print('hello1') """
    return render(request, 'annotate.html', {'files' : sorted(files), 
                                              'file_list_len': len(files),
                                               'infos': infos,
                                               'decision': decision,
                                               'personne': personnePhysiqueForm,
                                            # 'root_path': settings.FILES_DIR})
                                             'root_path': hp.files.treated_files_folder})

def read_file(request , file):
    f = open(hp.files.treated_files_folder + file, 'r')
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
    data = json.dumps(context)#, indent=4, sort_keys=True, default=str)
    return HttpResponse(data, content_type='application/json')
    #context = {'file_content': file_content}
    #return render(request, "annotate.html", context)
def return_new_decision_form(request):
    decision= decisionForm()
    return HttpResponse(decision)
