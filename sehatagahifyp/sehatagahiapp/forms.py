from django import forms
import django.core.validators as validator
from .validators import *

class Item_form(forms.Form):
    Name = forms.CharField(label='Item Name',max_length=25, validators=[validator.RegexValidator(regex=r'^[a-zA-Z][a-zA-Z ]+$')])
    Type = forms.ChoiceField(label='Item Type',choices=(('1','Video'), ('2','Image'), ('3','PDF')))
    FilePath = forms.FileField(validators=[file_size])


    def clean(self):
        cleaned_data = super().clean()
        Type = cleaned_data.get("Type")
        File = cleaned_data.get("FilePath").name
        if not (File.endswith('.mp4') and Type == '1' or File.endswith('.png') and Type == '2' or File.endswith('.pdf') and Type == '3'):
            self.add_error('Type', 'Please select .mp4 for Video, .png for Image or .pdf for PDF')


class Therapist_Register_form(forms.Form):
    Name = forms.CharField(label='Full Name',max_length=25, validators=[validator.RegexValidator(regex=r'^[a-zA-Z][a-zA-Z ]+$')])
    Username=forms.CharField(label='User Name',max_length=25,validators=[username_val])
    MobileNumber = forms.CharField(label='Mobile Number 03xxxxxxxxx',max_length=11,validators=[validator.RegexValidator(regex=r'^[0][3][0-9]+$'), validator.MinLengthValidator(11)])
    WorkEmail = forms.EmailField(label='Work Email')
    Password = forms.CharField(label='Password',max_length=10, widget=forms.PasswordInput,validators=[validator.MinLengthValidator(limit_value=6)])
    PasswordRe= forms.CharField(label='Re-enter Password',max_length=10, widget=forms.PasswordInput,validators=[validator.MinLengthValidator(limit_value=6)])
    SecurityQs1 = forms.CharField(label='Security Qs1: First and Last letter of Father\'s name',max_length=100)
    SecurityQs2 = forms.CharField(label='Security Qs1: First and Last letter of birth city',max_length=100)
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("Password")
        passwordre = cleaned_data.get("PasswordRe")
        email=cleaned_data.get("WorkEmail")
        if password!=passwordre:
            self.add_error('PasswordRe', 'The password does not match')
        if '@sehatagahi.com' not  in email:
            self.add_error('WorkEmail', 'Please enter the correct email')




class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=60)
    password = forms.CharField(label="Password", widget = forms.PasswordInput(), max_length=60)

class Item_Rename_form(forms.Form):
    ReName = forms.CharField(label='Item Name',max_length=25, validators=[validator.RegexValidator(regex=r'^[a-zA-Z][a-zA-Z ]+$')])


class PatientRegisterForm(forms.Form):
    name = forms.CharField(label='Full Name',max_length=25, validators=[validator.RegexValidator(regex=r'^[a-zA-Z][a-zA-Z ]+$')])
    fatherName = forms.CharField(label='Father\'s Name',max_length=25, validators=[validator.RegexValidator(regex=r'^[a-zA-Z][a-zA-Z ]+$')])
    dob = forms.DateField(
        label = 'Date of Birth (dd/mm/yyyy)',
        widget=forms.DateInput(format='%d/%m/%Y'),
        input_formats=('%d/%m/%Y', )
        )
    gender = forms.ChoiceField(label='Gender', choices = ((1,'Male'),(2,'Female')))
    condition = forms.CharField(label='Condition', max_length=250)
    area = forms.CharField(label='Area/City', max_length=100)
    mobileNumber = forms.CharField(label='Caregiver Mobile Number 03xxxxxxxxx', max_length=11,validators=[validator.RegexValidator(regex=r'^[0][3][0-9]+$'),validator.MinLengthValidator(11)])
    username=forms.CharField(label='User Name',max_length=25,validators=[username_val])
    password = forms.CharField(label='Password',max_length=10, widget=forms.PasswordInput,validators=[validator.MinLengthValidator(limit_value=6)])
    passwordRe= forms.CharField(label='Re-enter Password',max_length=10, widget=forms.PasswordInput,validators=[validator.MinLengthValidator(limit_value=6)])

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        passwordre = cleaned_data.get("passwordRe")
        if password!=passwordre:
            self.add_error('passwordRe', 'The password does not match')

class PatientEditForm(forms.Form):
    name = forms.CharField(label='Full Name',max_length=25, validators=[validator.RegexValidator(regex=r'^[a-zA-Z][a-zA-Z ]+$')])
    fatherName = forms.CharField(label='Father\'s Name',max_length=25, validators=[validator.RegexValidator(regex=r'^[a-zA-Z][a-zA-Z ]+$')])
    dob = forms.DateField(
        label = 'Date of Birth (dd/mm/yyyy)',
        widget=forms.DateInput(format='%d/%m/%Y'),
        input_formats=('%d/%m/%Y', )
        )
    gender = forms.ChoiceField(label='Gender', choices = ((1,'Male'),(2,'Female')))
    condition = forms.CharField(label='Condition', max_length=250)
    area = forms.CharField(label='Area/City', max_length=100)
    mobileNumber = forms.CharField(label='Caregiver Mobile Number 03xxxxxxxxx', max_length=11,validators=[validator.RegexValidator(regex=r'^[0][3][0-9]+$'),validator.MinLengthValidator(11)])

class PatientPasswordChangeForm(forms.Form):
    username = forms.CharField(label = 'User Name', widget = forms.TextInput(attrs={'readonly':'readonly'}))
    password = forms.CharField(label='Password',max_length=10, widget=forms.PasswordInput,validators=[validator.MinLengthValidator(limit_value=6)])
    passwordRe= forms.CharField(label='Re-enter Password',max_length=10, widget=forms.PasswordInput,validators=[validator.MinLengthValidator(limit_value=6)])

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        passwordre = cleaned_data.get("passwordRe")
        if password!=passwordre:
            self.add_error('passwordRe', 'The password does not match')

class PatientLogForm(forms.Form):
    message = forms.CharField(label='اہم واقعہ لکھیں', max_length=500, widget=forms.Textarea)

class AddReportForm(forms.Form):
    Name = forms.CharField(label='Report Name', max_length=25,validators=[validator.RegexValidator(regex=r'^[a-zA-Z][a-zA-Z ]+$')])
    FilePath = forms.FileField(validators=[file_size])

    def clean(self):
        cleaned_data = super().clean()
        File = cleaned_data.get("FilePath").name
        if not ( File.endswith('.jpeg')  or File.endswith('.pdf')):
            self.add_error('FilePath', 'Please select .jpeg for Image or .pdf for PDF')
class TrackNameForm(forms.Form):
    trackName = forms.CharField(label='Name your Track (A Track is a collection of exercises)',max_length=30, validators=[validator.RegexValidator(regex=r'^[a-zA-Z][a-zA-Z ]+$')])

class TrackAssignForm(forms.Form):
    duration = forms.IntegerField(label="Duration (in weeks)", max_value = 50)
    notes = forms.CharField(label='Instructions', max_length=1000, widget =forms.Textarea, help_text = "Please write the instructions in Urdu if possible.")

