from os import walk, listdir
from os.path import isdir, basename, join
from pathlib import Path
from django.shortcuts import render
from django.http import HttpResponse
from config.hparam import hparam as hp

def organize_view(request, *args, **kwargs):
    #content = get_treated_folder()[0]
    return render(request, 'organize.html', {"dirpaths": get_ul_elements() #dict_man(content),
                                            })
def get_ul_elements():
    return dict_man(get_treated_folder()[0])

def get_treated_folder() -> list:
    result: list = []
    for (dirpath, dirnames, filenames) in walk(hp.files.treated_files_folder):
        # print(f'\n\nDirnames: {dirnames} \n')
        result.append(path_to_dict(dirpath))
    # print(f'\n\nDirnames: {result[0]} \n')
    return result

def path_to_dict(path):
    d = {'name': basename(path)}
    if isdir(path):
        d['type'] = "directory"
        d['path'] = path
        d['children'] = [path_to_dict(join(path,x)) for x in listdir(path)]
    else:
        d['type'] = "file"
    return d

level = 0
def dict_man (dic: dict):
    # html = '\n#########\n' + str(dic) + '\n'
    html = ''
    global level
    for k, v in dic.items():
        if k == 'type':
            if v == 'directory':
                ## TODO : Find safer method to store paths than data attributes
                html += '<li class= "level-'+ str(level)+'"><span class="caret" data-path="'+ dic['path'] +'">' + dic['name'] + '</span> <ul class="nested">'
            if v == 'file':
                html += '<li class= "level-'+ str(level)+'">' + dic['name'] + '</li>'
                #print(dic['name'])
        if k == 'children':
            level += 1
            for i in v:
                html +=  dict_man(i)
        else : continue
        html += '</ul>'
        level -= 1
    # html += '</ul></li></ul>'
    return html

def create_new_dir(request):
    import json
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    new_path = body['path']
    print(f'Here {new_path}')
    try:
        Path(new_path).mkdir(mode=755, parents=True, exist_ok=True)
    except: #FileNotFoundError or FileExistsError as e :
        print("Errors 1")
    return HttpResponse({"response": "Folder Created"}, content_type='application/json')
