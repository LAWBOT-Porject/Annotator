from os import walk, listdir
from os.path import isdir, basename, join
from pathlib import Path
from ntpath import basename as ntbasename, join as ntjoin ##TODOO change this to os.basename once deployed
from json import loads, dumps
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from annotate.models import Decision
from config.hparam import hparam as hp

treated_files_folder = hp.files.treated_files_folder

def organize_view(request, *args, **kwargs):
    #content = get_treated_folder()[0]
    #print(f'ULs: {get_ul_elements(dirs_only=True)}')
    return render(request, 'organize.html', {"dirpaths": get_ul_elements(), #dict_man(content),
                                              "dirs_only": get_ul_elements(dirs_only=True)})
def get_ul_elements(dirs_only=False):
    if not dirs_only : return dict_man(get_treated_folder()[0])
    else : return dict_man_dirs(get_treated_folder()[0])
    
""" def get_ul_elements(request):
    return HttpResponse(dumps( dict_man(get_treated_folder()[0])), content_type='application/json') """

def get_treated_folder() -> list:
    result: list = []
    for (dirpath, dirnames, filenames) in walk(treated_files_folder):
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

def dict_man_dirs (dic: dict):
    # html = '\n#########\n' + str(dic) + '\n'
    html = ''
    global level
    for k, v in dic.items():
        if k == 'type':
            if v == 'directory':
                ## TODO : Find safer method to store paths than data attributes
                html += '<li class= "level-'+ str(level)+'"><span class="caret" data-path="'+ dic['path'] +'">' + dic['name'] + '</span> <ul class="nested">'
            if v == 'file': continue
            #     html += '<li class= "level-'+ str(level)+'">' + dic['name'] + '</li>'
                #print(dic['name'])
        if k == 'children':
            level += 1
            for i in v:
                html +=  dict_man_dirs(i)
        else : continue
        html += '</ul>'
        level -= 1
    # html += '</ul></li></ul>'
    return html

def create_new_dir(request):
    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)
    new_path = body['path']
    #print(f'Here {new_path}')
    try:
        Path(new_path).mkdir(mode=755, parents=True, exist_ok=True)
    except: #FileNotFoundError or FileExistsError as e :
        print("Errors 1")
    return HttpResponse(dumps({"response": "Folder Created"}), content_type='application/json')

def search_key_words(request):
    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)
    key_words = body['keys']
    operators = body['ops']
    # print(f'Here {key_words} {operators}')
    result = Decision.objects.all()
    for i in range(len(key_words)):
        if operators[i] == 'and':
            temp = Decision.objects.filter(texte_decision__icontains= key_words[i])
            result = result.intersection(temp)
        elif operators[i] == 'or':
            temp = Decision.objects.filter(texte_decision__icontains= key_words[i])
            result = result.union(temp)
        elif operators[i] == 'except':
            temp = Decision.objects.filter(texte_decision__icontains= key_words[i])
            result = result.difference(temp)
        else: continue
    file_names_list = []
    file_paths_list = []
    for i in result:
        file_names_list.append(basename(i.decision_treated_path))
        file_paths_list.append(i.decision_treated_path)
        #print(f'{i.rg}  {ntbasename(i.decision_treated_path)}')
    #print(type({"files_result": file_names_list}))#, "result": result})
    return JsonResponse({"file_names": file_names_list, "file_paths": file_paths_list}) #, "file_paths": file_paths_list})

def move_files(request):
    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)
    file_paths = body['paths']
    file_names = body['names']
    target_dir = body['targetDir']
    # print(target_dir)
    # print(file_paths)
    from pathlib import Path
    for i in range(len(file_paths)):
        try:
        # print('path {0}'.format(path))
        # print('new path {0}'.format(new_path + name))
            Path(file_paths[i]).rename(join(target_dir, file_names[i]))
            old = Decision.objects.get(decision_treated_path__contains = file_names[i])
            old.decision_treated_path = join(target_dir, file_names[i])
            old.save()
        except FileExistsError: # FileNotFoundError or FileExistsError as e 
            # Delete file from temp folder if it already has a folder in uploads
            print('FileExistsError')
            old = Decision.objects.get(decision_treated_path__contains = file_names[i])
            old.decision_treated_path = join(target_dir, file_names[i])
            old.save()
        except Decision.DoesNotExist:
            print('Doesnot Exist error')
            n = Decision(decision_treated_path=join(target_dir, file_names[i]))
            n.save()
    return JsonResponse({"response": "MPA"})

def annotate_view(request):
    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)
    selected_dir = body['directory']
    if selected_dir == '':
        selected_dir = treated_files_folder
    # decisions = Decision.objects.filter(decision_treated_path__contains = selected_dir)
    # files = []
    # for item in decisions:
    #     tmp = []
    #     decision_path = item.decision_treated_path
    #     tmp.append(basename(decision_path))
    #     tmp.append(decision_path)
    #     files.append(tmp)
    # return render(request, 'annotate.html', {"files": files})
    return redirect('/annotate')#, {"directory": selected_dir})
