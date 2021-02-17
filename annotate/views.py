import json
from os.path import basename
from django.http import HttpResponse
from config.hparam import hparam as hp
from django.shortcuts import render, redirect
from annotate.models import (Juridiction as juridiction,
                            Ville as ville, 
                            Categorie,
                            Decision)

treated_files_folder = hp.files.treated_files_folder
default_dir = None

def annotate_view(request, directory=None, *args, **kwargs):
    if request.method == 'GET':
        files = []
        global default_dir
        if (directory != None):
            selected_dir = directory
            default_dir = directory
        elif (default_dir != None):
            selected_dir = default_dir
        else:
            selected_dir = treated_files_folder
            default_dir = selected_dir
        decisions = Decision.objects.filter(decision_treated_path__contains = selected_dir)
        for item in decisions:
            tmp = []
            decision_path = item.decision_treated_path
            tmp.append(basename(decision_path))
            tmp.append(decision_path)
            files.append(tmp)
        return render(request, 'annotate.html', 
        {"files": files, 'file_list_len': len(files),})
    if request.method == 'POST':
        if 'read' in request.path:
            return read_file(request) 
        if 'get_default_category' in request.path:
            return get_category_by_nppac(request)
        print(request)
        return redirect('/annotate/'+ default_dir)

    

from json import loads
def read_file(request ):
    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)
    file = body['path']
    file_name = body['file_name']
    f = open(file, 'r', encoding='utf-8')
    file_content = f.read()
    f.close()
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
    return HttpResponse(data, content_type='application/json')

def get_category_by_nppac (request):
    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)
    nppac = body['nppac']
    try:
        default_categorie = Categorie.objects.get(noppac = nppac)
        default_categorie = getattr(default_categorie, 'description')
    except Categorie.DoesNotExist :
        default_categorie = '##### Catégorie non trouvée #####'
        nppac = ''
    data = json.dumps({"nppac": nppac, "default_categorie": default_categorie})
    return HttpResponse(data, content_type='application/json')
