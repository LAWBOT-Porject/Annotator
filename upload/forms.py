from django import forms
from helpers.upload_utilities import allow_file_types

class UploadFileForm(forms.Form):
    """ file_name   = forms.CharField(label='Donner un nom a votre fichier',
                                max_length=50, required=False) """
    file        = forms.FileField(widget=forms
                        .ClearableFileInput(
                            attrs={
                                    'multiple': True, 
                                    # 'accept': allow_file_types(),
                                    #'directory': True,
                                    'webkitdirectory': True,
                                    }
                            ))
