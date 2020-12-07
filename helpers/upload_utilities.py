"""Upload helper functions

This package contains utility functions for uploading files into the server

This file can also be imported as a module and contains the following functions:

    * handle_uploaded_file - save the uploaded files
"""


from config.hparam import hparam as hp


def handle_uploaded_file(f, name):
    with open( hp.upload.folder + name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def allow_file_types():
    return ','.join(hp.upload.allowed_file_types)

def verify_file_type(file_name):
    return '.' + file_name.split('.')[-1] in hp.upload.allowed_file_types
