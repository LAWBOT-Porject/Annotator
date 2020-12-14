"""Upload helper functions

This package contains utility functions for uploading files into the server

This file can also be imported as a module and contains the following functions:

    * handle_uploaded_file - save the uploaded files
"""


from config.hparam import hparam as hp
import textract
import re
from shutil import copyfile


def handle_uploaded_file(f, name):
    with open( hp.files.uploaded_files_folder + name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def allow_file_types():
    return ','.join(hp.files.allowed_file_types)

def verify_file_type(file_name):
    return ('.' + file_name.split('.')[-1] in 
    hp.files.allowed_file_types) or ('.' + file_name.split('.')[-1] in [ x.upper() 
                                            for x in hp.files.allowed_file_types ])
                                            

def transform_to_standard_chars(raw_text):
    raw_text = raw_text.lower()
    translation_table = str.maketrans(hp.files.fr_accented_letters,
                                    hp.files.equivalant_letters)
    raw_text = raw_text.translate(translation_table)
    raw_text = raw_text.replace('æ', 'ae')
    raw_text = raw_text.replace('œ', 'oe')
    return raw_text

def search_city(raw_text, cities_file_path):
    raw_text = transform_to_standard_chars(raw_text)
    with open(cities_file_path, 'r') as f:
        for line in f:
            line = line.replace('\n', '')
            city = raw_text.find(line)
            if (city != -1):
                return line[:3].upper()
        return 'city404'

def search_juridiction(raw_text, juridictions_file_path):
    raw_text = transform_to_standard_chars(raw_text)
    with open(juridictions_file_path, 'r') as f:
        for line in f:
            line = line.replace('\n', '')
            juridiction = raw_text.find(line)
            if (juridiction != -1):
                return abbreviate_juridiction(line)
        return 'jurid404'

def abbreviate_juridiction(in_juridiction):
    for dic in hp.files.juridictions_abbreviations :
        for key in dic:
            if (in_juridiction == key):
                return dic[key]
    return 'juridabbr404'

def search_reference(raw_text):
    raw_text = transform_to_standard_chars(raw_text)
    try:
        reference = re.findall(r'\b[0-9]{2}[\/]?[0-9]{5}[\.]?',
							raw_text)[0]
    except: reference = ''

    if reference != '':
       return str(int(''.join(reference.split('/'))[:7]))
    else :
        return 'reference_404'

def convert_to_txt(file_name):
    if ('.' + file_name.split('.')[-1] != hp.files.standard_file_type):
        text = textract.process(hp.files.uploaded_files_folder + 
                                file_name, errors="ignore")
        text = text.decode("utf-8")
        search_text = str(text)[:200]
        juridiction = search_juridiction(search_text, hp.files.static_data_folder 
                                                    + hp.files.juridictions_file_name)
        city = search_city(search_text, hp.files.static_data_folder 
                                                    + hp.files.cities_file_name)
        reference = search_reference(search_text)
        new_file_name = juridiction + city + reference + hp.files.standard_file_type
        file = open(hp.files.treated_files_folder + 
                    #file_name.split('.')[0] +
                    new_file_name , "w")
        file.write(str(text)) 
        file.close()
    else :
        with open(hp.files.uploaded_files_folder + file_name, 'r') as file:
            text = file.read()
            search_text = str(text)[:200]
            juridiction = search_juridiction(search_text, hp.files.static_data_folder 
                                                        + hp.files.juridictions_file_name)
            city = search_city(search_text, hp.files.static_data_folder 
                                                        + hp.files.cities_file_name)
            reference = search_reference(search_text)
            new_file_name = juridiction + city + reference + hp.files.standard_file_type
            copyfile(hp.files.uploaded_files_folder + 
            file_name, hp.files.treated_files_folder + new_file_name)
