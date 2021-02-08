from os import walk, listdir
from os.path import isdir, basename, join
from django.shortcuts import render
from config.hparam import hparam as hp

def organize_view(request, *args, **kwargs):
    content = get_treated_folder()[0]
    # for k, v in content.items():
    #     print('#########')
    #     print(k)
    #     print(v)
    #     print('#########')
    
    return render(request, 'organize.html', {"dirpaths": dict_man(content),
                                            })

def get_treated_folder() -> list:
    result: list = []
    for (dirpath, dirnames, filenames) in walk(hp.files.treated_files_folder):
        result.append(path_to_dict(dirpath))
    return result

def path_to_dict(path):
    d = {'name': basename(path)}
    if isdir(path):
        d['type'] = "directory"
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
                html += '<li class= "level-'+ str(level)+'"><span class="caret">' + dic['name'] + '</span> <ul class="nested">'
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
