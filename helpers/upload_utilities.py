"""Upload helper functions

This package contains utility functions for uploading files into the server

This file can also be imported as a module and contains the following functions:

    * handle_uploaded_file - save the uploaded files
"""


from config.hparam import hparam as hp
import textract
from shutil import copyfile


def handle_uploaded_file(f, name):
    with open( hp.files.uploaded_files_folder + name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def allow_file_types():
    return ','.join(hp.files.allowed_file_types)

def verify_file_type(file_name):
    return '.' + file_name.split('.')[-1] in hp.files.allowed_file_types

def convert_to_txt(file_name):
    if ('.' + file_name.split('.')[-1] != hp.files.standard_file_type):
        text = textract.process(hp.files.uploaded_files_folder + 
                                file_name)
        text = text.decode("utf-8")
        file = open(hp.files.treated_files_folder + 
                    file_name.split('.')[0] + 
                    hp.files.standard_file_type, "w")
        file.write(str(text)) 
        file.close()
    else :
        copyfile(hp.files.uploaded_files_folder + file_name, hp.files.treated_files_folder + file_name)
