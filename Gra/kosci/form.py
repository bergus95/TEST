from django import forms
from django.core.validators import validate_email


class ContactForm(forms.Form):
    # tu daj nazwy inputow
    imie = forms.CharField(max_length=100)

#    def clean_email(self):
 #       em = self.cleaned_data['email']
  #      if not validate_email(em):
   #         raise forms.ValidationError('Niepoprawny email!')

class UsernameForm(forms.Form):
    username = forms.name = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super(UsernameForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Twój nick:"
