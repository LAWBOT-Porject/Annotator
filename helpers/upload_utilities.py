"""Upload helper functions

This package contains utility functions for uploading files into the server

This file can also be imported as a module and contains the following functions:

    * handle_uploaded_file - save the uploaded files
"""

from config.hparam import hparam as hp
import re, hashlib, textract#, codecs
from fuzzywuzzy import fuzz
from shutil import copyfile
from pathlib import Path
from annotate.models import (Ville as ville, Juridiction as juridiction)

def handle_uploaded_file(f, name):
    path = hp.files.uploaded_files_folder + '/temp/' + name
    with open( path, 'wb+' ) as destination: #encoding= 'utf-8'
        destination.write(f.read())
        # the method below is both time and memory efficient
        # for chunk in f.chunks():
        #     destination.write(str(chunk))
    # Create the folder path from the file hash
    md = md5(path)
    new_path = '/'.join([hp.files.uploaded_files_folder, md[:1], md[:2], md[:3],''])
    try:
        Path(new_path).mkdir(mode=755, parents=True, exist_ok=True)
    except: #FileNotFoundError or FileExistsError as e :
        print("Errors 1")
        # print(e.errno)
    # Move file from temp folder to the new folder
    try:
        # print('path {0}'.format(path))
        # print('new path {0}'.format(new_path + name))
        Path(path).rename(new_path + name)
    except FileExistsError: # FileNotFoundError or FileExistsError as e 
        # Delete file from temp folder if it already has a folder in uploads
        Path(path).unlink()
    return new_path + name

def allow_file_types():
    return ','.join(hp.files.allowed_file_types)

def verify_file_type(file_name):
    return ('.' + file_name.split('.')[-1] in 
    hp.files.allowed_file_types) or ('.' + file_name.split('.')[-1] in [ x.upper() 
                                            for x in hp.files.allowed_file_types ])

## Done : Save raw uploaded files in md5 related structure
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def transform_to_standard_chars(raw_text):
    raw_text = raw_text.lower()
    # translation_table = str.maketrans(hp.files.fr_accented_letters,
    #                                 hp.files.equivalant_letters)
    # raw_text = raw_text.translate(translation_table)
    raw_text = raw_text.replace('æ', 'ae')
    raw_text = raw_text.replace('œ', 'oe')
    raw_text = raw_text.replace('-', ' ')
    raw_text = raw_text.replace('ç', 'c')
    raw_text = raw_text.replace('é', 'e')
    raw_text = raw_text.replace('â', 'a')
    raw_text = raw_text.replace('ê', 'e')
    raw_text = raw_text.replace('î', 'i')
    raw_text = raw_text.replace('ô', 'o')
    raw_text = raw_text.replace('û', 'u')
    raw_text = raw_text.replace('à', 'a')
    raw_text = raw_text.replace('è', 'e')
    raw_text = raw_text.replace('ì', 'i')
    raw_text = raw_text.replace('ò', 'o')
    raw_text = raw_text.replace('ù', 'u')
    raw_text = raw_text.replace('ë', 'e')
    raw_text = raw_text.replace('ï', 'i')
    raw_text = raw_text.replace('ü', 'u')
    raw_text = raw_text.replace('ÿ', 'y')
    return raw_text

def search_city(raw_text):
    raw_text = transform_to_standard_chars(raw_text).lower()
    all_villes = ville.objects.all()
    cities     = [city.ville for city in all_villes]
    # cities = ville.objects.values('ville').distinct()
    biggest_ration = 0
    potential_city = ''
    for city in cities :
        cmp_city = transform_to_standard_chars(city).lower()
        temp_ratio = fuzz.partial_ratio(cmp_city, raw_text)
        position = raw_text.find(cmp_city)
        if (temp_ratio ==100 or (position != -1)):
            zip_code = [z.zip_code for z in all_villes if z.ville  == city]
            try :
                zc = zip_code[0]
            except :
                zc = '00001' # To tell that the city does not exist in db table
                position = -1
            #finally:
            return [zc, position]
        elif (temp_ratio > biggest_ration) :
            biggest_ration = temp_ratio
            potential_city = city
        else: continue
    zip_code = [z.zip_code for z in all_villes if z.ville == potential_city]
    position = raw_text.find(potential_city)
    try :
        zc = zip_code[0]
    except :
        zc = '00000'
        position = -1
    return [zc, position]

def search_juridiction(raw_text): #, juridictions_file_path)
    raw_text = transform_to_standard_chars(raw_text).lower()
    all_juridictions = juridiction.objects.filter(zip_code_id__isnull=True)
    juridics         = [juridic.type_juridiction for juridic in all_juridictions]
    # cities = ville.objects.values('ville').distinct()
    biggest_ration = 0
    potential_jurid = ''
    for jurid in juridics :
        cmp_jurid = transform_to_standard_chars(jurid).lower()
        temp_ratio = fuzz.partial_ratio(cmp_jurid, raw_text)
        position = raw_text.find(cmp_jurid)
        if (temp_ratio == 100 or (position != -1)):
            abbreviation = [j.abbreviation for j in all_juridictions if j.type_juridiction == jurid]
            try :
                abrv = abbreviation[0]
            except :
                abrv = 'ABRZ' # To tell that juridiction does not exist in table
                position = -1
            return [abrv, position]
        elif (temp_ratio > biggest_ration) :
            biggest_ration = temp_ratio
            potential_jurid = jurid
        else: continue
    abbreviation = [j.abbreviation for j in all_juridictions if j.type_juridiction == potential_jurid]
    position = raw_text.find(potential_jurid)
    try :
        abrv = abbreviation[0]
    except :
        abrv = 'ABRV'
        position = -1
    return [abrv, position]


def search_reference(raw_text):
    try: # Case 1 : reference is 10 digits
        reference = re.findall(r'[0-9]{10}', raw_text)[0]
        position = raw_text.find(reference)
    except:
        try : # Case 2 : reference is 8 digits
            reference = re.findall(r'[0-9]{8}', raw_text)[0]
            position = raw_text.find(reference)
        except:
            try : # Case 3 : reference is 7 digits separated or not by forwarded slach '/'
                reference = re.findall(r'[0-9]{2}[\/]?[0-9]{5}',raw_text)[0]
                position = raw_text.find(reference)
                return [''.join(reference.split('/'))[:7], position]
            except : return ['', -1]
    return [reference, position]

def convert_to_txt(file_path, file_name):
    if ('.' + file_name.split('.')[-1] != hp.files.standard_file_type):
        try:
            text = textract.process(file_path, encoding= 'utf-8', errors="ignore")
            try:
                text = text.decode("utf-8")
            except:
                text = text.decode("ISO-8859-1")
        except :
            try:
                text = textract.process(file_path, encoding= 'ISO-8859-1', errors="ignore")
                try:
                    text = text.decode("utf-8")
                except:
                    text = text.decode("ISO-8859-1")
            except:
                with open(file_path,  encoding='utf-8') as file:
                    text = file.read()
                    text = str(text)
        # text = text.decode("latin-1")
        search_text = text[500] #str(text)#[:170] no limit is better => case 2000042485 : too space created after convertion
        # print(search_text)
        juridiction = search_juridiction(search_text) #, hp.files.static_data_folder 
                                                    #  + hp.files.juridictions_file_name)
        juridiction_pos = juridiction[1]
        juridiction = juridiction[0]
        city = search_city(search_text) #, hp.files.static_data_folder 
        city_position = city[1]                             #            + hp.files.cities_file_name)
        city = city[0]
        reference = search_reference(search_text)
        rg_position = reference[1]
        reference = reference[0]
        if (reference == ''):
            reference = search_reference(file_name)[0]
        if (reference == ''):
            import uuid
            reference = str(uuid.uuid1().int)[5:15]

        new_file_name = '-'.join([juridiction, city, reference ])
        new_file_name += hp.files.standard_file_type
        # print(new_file_name)
        file = open(hp.files.treated_files_folder + '/'+
                    #file_name.split('.')[0] +
                    new_file_name , "w")
        file.write(text) 
        file.close()
        return [new_file_name, rg_position, 
        city_position, juridiction_pos, text,
        hp.files.treated_files_folder + '/'+ new_file_name]
    else :
        with open(file_path, encoding='utf-8') as file:
            decision_texte = file.read()
            search_text = decision_texte[:500]
            #search_text = str(search_text)[:200] #str(text)[:200]
            #print(search_text)#.decode('utf-8'))
            #print(str('\é\î\à\ç ') + str(search_text[:500].encode(encoding='utf-8').decode()))
            juridiction = search_juridiction(search_text) #, hp.files.static_data_folder 
            juridiction_pos = juridiction[1]
            juridiction = juridiction[0]
            #print('###### ', juridiction)                                            #+ hp.files.juridictions_file_name)
            city = search_city(search_text) #, hp.files.static_data_folder 
            city_position = city[1]                           #            + hp.files.cities_file_name)
            city = city[0]
            reference = search_reference(search_text)
            rg_position = reference[1]
            reference = reference[0]
            new_file_name = '-'.join([juridiction, city, reference ])
            new_file_name += hp.files.standard_file_type
            #print('##### treated path #{0}#'.format(hp.files.treated_files_folder+ '/' + new_file_name))
            copyfile(file_path, hp.files.treated_files_folder + '/' + new_file_name)
            return [new_file_name, rg_position, 
            city_position, juridiction_pos,decision_texte,#str(text),
            hp.files.treated_files_folder + '/' + new_file_name]
