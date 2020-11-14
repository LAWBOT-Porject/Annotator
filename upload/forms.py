from django import forms

class UploadFileForm(forms.Form):
    """ file_name   = forms.CharField(label='Donner un nom a votre fichier',
                                max_length=50, required=False) """
    file        = forms.FileField(widget=forms
                        .ClearableFileInput(
                            attrs={'multiple': True}
                            ))
