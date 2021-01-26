""" from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm, CharField, TextInput, DateField, ChoiceField, RadioSelect
from .models import (
                Ville, 
                Juridiction, 
                Decision, 
                PersonnePhysique, 
                PersonneMorale,
                Demande,
                CategorieDemande,
                Norme,
                PersonneDecision,
                PartieDemande,
                )
import datetime


class PartiePhysiqueForm(ModelForm):
    class Meta:
        CHOICES=[('homme','Homme'), ('femme','Femme')]
        model = PersonnePhysique
        fields = [  'titre_personne_ph', 
                    'nom_personne_ph', 
                    'prenom_personne_ph',
                    'date_naissance_personne_ph',
                    'adresse_personne_ph',
                    'sexe_personne_ph'
        ]
        labels = {
            'titre_personne_ph': _(''),
            'nom_personne_ph': _(''),
            'prenom_personne_ph': _(''),
            'date_naissance_personne_ph': _(''),
            'adresse_personne_ph': _(''),
            'sexe_personne_ph': _(''),
        }
        help_texts = {
            'titre_personne_ph': _('Titre'),
            'nom_personne_ph': _('Nom'),
            'prenom_personne_ph': _('Prénom'),
            'date_naissance_personne_ph': _('date de naissance'),
            'adresse_personne_ph': _('Adresse'),
            # 'sexe_personne_ph': _('Some useful help text.'),
        }
        # """ #widgets = {
        #     'titre_personne_ph': CharField( max_length=20, 
        #                                     ),
        #     'nom_personne_ph': CharField( max_length=100, 
        #                                     ),
        #     'prenom_personne_ph': CharField( max_length=100, 
        #                                     ),
        #     'date_naissance_personne_ph': DateField(),
        #     'adresse_personne_ph': CharField( max_length=255, 
        #                                     ),
        #     'sexe_personne_ph' : ChoiceField(choices=CHOICES, 
        #                                     ),
        # } """
        # """ labels = {'', '', '', 'Date de naissance', '', ''} """

""" class PartieMoraleForm(ModelForm):
    class Meta:
        model = PersonneMorale
        fields = (  'nom_entreprise', 
                    'numero_SIRET', 
                    'numero_NAF',
                    'adresse_entreprise',
                  )
 """        
        #     """ widgets = {
        #     'nom_entreprise': CharField( max_length=255, 
        #                                     ),
        #     'numero_SIRET': CharField( max_length=100, 
        #                                     ),
        #     'numero_NAF': CharField( max_length=100, 
        #                                     ),
        #     'adresse_entreprise': CharField( max_length=20, 
        #                                     ),
        # } """
    #    """  labels = {'', '', '', ''}

""" class DateInput(forms.DateInput):
    input_type= 'date'
    input_format= ('%d %B %Y') """
    # attrs= { 
    #         'placeholder': 'jj-mm-aaaa'
    #         }

""" class decisionInfo(forms.Form):
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
 """
