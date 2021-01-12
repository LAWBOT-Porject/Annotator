from django import forms
import datetime

class DateInput(forms.DateInput):
    input_type= 'date'
    input_format= ('%d %B %Y')
    # attrs= { 
    #         'placeholder': 'jj-mm-aaaa'
    #         }

class decisionInfo(forms.Form):
    rg = forms.CharField( label='', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'numéro RG'}))
    juridiction = forms.CharField( label='',max_length=100, widget=forms.TextInput(attrs={'placeholder': 'juridiction'})) 
    ville = forms.CharField( label='',max_length=100, widget=forms.TextInput(attrs={'placeholder': 'ville'}))
    date = forms.DateField(initial=datetime.date.today, label='', widget=DateInput)#,widget=forms.TextInput(attrs={'placeholder': 'jj-mm-aaaa'}))

class decisionForm(forms.Form):
    dispositifs = forms.CharField( label='', widget=forms.TextInput(attrs={'placeholder': 'Dispositifs'}))
