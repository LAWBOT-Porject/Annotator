from django import forms
import datetime


class DateInput(forms.DateInput):
    input_type= 'date'
    input_format= ('%d %B %Y')
    # attrs= { 
    #         'placeholder': 'jj-mm-aaaa'
    #         }

class decisionInfo(forms.Form):
    rg = forms.CharField( label='', max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Numéro RG'}))
    juridiction = forms.CharField( label='',max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Juridiction'})) 
    chambre = forms.CharField( label='',max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Chambre'})) 
    ville = forms.CharField( label='',max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Ville'}))
    date = forms.DateField(initial=datetime.date.today, label='', widget=DateInput)#,widget=forms.TextInput(attrs={'placeholder': 'jj-mm-aaaa'}))
    titre_h = forms.CharField( label='',max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Titre Homme tribunal'}))
    nom_h = forms.CharField( label='',max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Nom Homme tribunal'}))
    prenom_h = forms.CharField( label='',max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Prénom Homme tribunal'}))
    CHOICES=[('homme','Homme'), ('femme','Femme')]
    sexe_h = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label='')

class decisionForm(forms.Form):
    dispositifs = forms.CharField( label='', widget=forms.TextInput(attrs={'placeholder': 'Dispositifs'}))
