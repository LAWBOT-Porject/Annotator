from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from os import walk
from config.hparam import hparam as hp

def annotate_view(request, *args, **kwargs):
    #return HttpResponse('Annotateur sera bien tot disponible')
    files = []
    for (dirpath, dirnames, filenames) in walk(hp.upload.folder):
        files.extend(filenames)
    return render(request, 'annotate.html', {'files' : files, 
                                            'root_path': hp.upload.folder})

def read_file(request , file):
    f = open(hp.upload.folder + file, 'r')
    file_content = f.read()
    f.close()
    #context = {'file_content': file_content}
    #return render(request, "annotate.html", context)
    return HttpResponse(file_content)
