from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from os import walk
from .forms import decisionInfo,decisionForm, PartiePhysiqueForm
from config.hparam import hparam as hp

#from django.conf import settings


def annotate_view(request, *args, **kwargs):
    files = []
    infos = decisionInfo()#auto_id=False)
    decision= decisionForm()
    personnePhysiqueForm = PartiePhysiqueForm()
    for (dirpath, dirnames, filenames) in walk(hp.files.treated_files_folder):
        files.extend(filenames)
    if (request.method == 'POST'):
        print('hello')
    if (request.method == 'GET'):
        print('hello1')
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
    return HttpResponse(file_content)
    #context = {'file_content': file_content}
    #return render(request, "annotate.html", context)
def return_new_decision_form(request):
    decision= decisionForm()
    return HttpResponse(decision)
