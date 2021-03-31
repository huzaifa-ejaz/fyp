from django import forms
import django.core.validators as validator
from .validators import *

class Item_form(forms.Form):
    Name = forms.CharField(label='Item Name',max_length=25, validators=[validator.RegexValidator(regex=r'[a-zA-Z][a-zA-Z ]+')])
    Type = forms.ChoiceField(label='Item Type',choices=(('1','Video'), ('2','Image'), ('3','PDF')))
    FilePath = forms.FileField(validators=[file_size])


    def clean(self):
        cleaned_data = super().clean()
        Type = cleaned_data.get("Type")
        File = cleaned_data.get("FilePath").name
        if File.endswith('.mp4') and Type != 'Video':
            self.add_error('Type', 'Wrong File type selected')
        elif File.endswith('.pdf') and Type != 'PDF':
            self.add_error('Type', 'Wrong File type selected')
        elif File.endswith('.png') and Type != 'Image':
            self.add_error('Type', 'Wrong File type selected')


class Therapist_Register_form(forms.Form):
    Name = forms.CharField(label='Full Name',max_length=25, validators=[validator.RegexValidator(regex=r'[a-zA-Z][a-zA-Z ]+')])
    Username=forms.CharField(label='User Name',max_length=25,validators=[username_val])
    MobileNumber = forms.CharField(label='Mobile Number 03xxxxxxxxx',max_length=11,validators=[validator.RegexValidator(regex=r'[0][3][0-9]+')])
    WorkEmail = forms.EmailField(label='Work Email',validators=[validator.EmailValidator(whitelist =['sehatagahi'])])
    Password = forms.CharField(label='Password',max_length=10, widget=forms.PasswordInput,min_length=6)
    PasswordRe= forms.CharField(label='Re-enter Password',max_length=10, widget=forms.PasswordInput,min_length=6)
    SecurityQs1 = forms.CharField(label='Security Qs1: First and Last letter of Father\'s name',max_length=100)
    SecurityQs2 = forms.CharField(label='Security Qs1: First and Last letter of birth city',max_length=100)
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("Password")
        passwordre = cleaned_data.get("PasswordRe")
        if password!=passwordre:
            self.add_error('PasswordRe', 'The password does not match')



