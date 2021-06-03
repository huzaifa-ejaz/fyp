from sehatagahiapp.models import AuthorizedEmail, Therapist
from django import forms
import django.core.validators as validator
from .validators import *
from django.conf import settings


class Item_form(forms.Form):
    Name = forms.CharField(label='Item Name',max_length=25, validators=[validator.RegexValidator(regex=r'^[a-zA-Z][a-zA-Z\s]+[0-9]*$',message='Name needs to be alphabets followed by optional space and/or optional numeric digits.')])
    Type = forms.ChoiceField(label='Item Type',help_text='Please select the Item type from the drop down.',choices=(('1','Video'), ('2','Image'), ('3','PDF')))
    FilePath = forms.FileField(help_text='<br/>File formats:<br/>Video : mp4<br/>Image : png<br/>PDF : pdf')
    def clean(self):
        cleaned_data = super().clean()
        Type = cleaned_data.get("Type")
        File = cleaned_data.get("FilePath").name
        Fileobj=cleaned_data.get("FilePath")
        if not (File.endswith('.mp4') and Type == '1' or File.endswith('.png') and Type == '2' or File.endswith('.pdf') and Type == '3'):
            self.add_error('Type', 'Please select .mp4 for Video, .png for Image or .pdf for PDF')
        elif Fileobj.size > settings.MAXFILESIZE:
            self.add_error('FilePath','Maximum file size is 50MB')



class Therapist_Register_form(forms.Form):
    Name = forms.CharField(label='Full Name',max_length=25, validators=[validator.RegexValidator(regex=r'^[a-zA-Z][a-zA-Z ]+$')])
    Username=forms.CharField(label='User Name',max_length=25,validators=[username_val])
    MobileNumber = forms.CharField(label='Mobile Number 03xxxxxxxxx',max_length=11,validators=[validator.RegexValidator(regex=r'^[0][3][0-9]+$'), validator.MinLengthValidator(11)])
    WorkEmail = forms.EmailField(label='Work Email')
    Password = forms.CharField(label='Password',max_length=10, widget=forms.PasswordInput,validators=[validator.MinLengthValidator(limit_value=6)])
    PasswordRe= forms.CharField(label='Re-enter Password',max_length=10, widget=forms.PasswordInput,validators=[validator.MinLengthValidator(limit_value=6)])
    SecurityQs1 = forms.CharField(label='Security Qs1: First and Last letter of Father\'s name',max_length=2)
    SecurityQs2 = forms.CharField(label='Security Qs1: First and Last letter of birth city',max_length=2)
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("Password")
        passwordre = cleaned_data.get("PasswordRe")
        email=cleaned_data.get("WorkEmail")
        if password!=passwordre:
            self.add_error('PasswordRe', 'The password does not match')
        if '@sehatagahi.com' not  in email:
            self.add_error('WorkEmail', 'Please enter the correct email')
        
        #Checking if the provided email is an authorized email
        try:
            authorizedEmail = AuthorizedEmail.objects.get(WorkEmail__exact=email)
        except AuthorizedEmail.DoesNotExist:
            self.add_error('WorkEmail','Please enter a valid email')
        
        #Checking if the provided email is already in use by another user
        try:
            therapist = Therapist.objects.get(WorkEmail__exact = email)
            self.add_error('WorkEmail','This email is already in use by another user')
        except Therapist.DoesNotExist:
            pass




class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=60)
    password = forms.CharField(label="Password", widget = forms.PasswordInput(), max_length=60)

class Item_Rename_form(forms.Form):
    ReName = forms.CharField(label='Item Name',max_length=25,help_text="Please rename your item.", validators=[validator.RegexValidator(regex=r'^[a-zA-Z][a-zA-Z\s]+[0-9]*$',message='Name needs to be alphabets followed by optional space and/or optional numeric digits.')])


class PatientRegisterForm(forms.Form):
    name = forms.CharField(label='Full Name',max_length=25, validators=[validator.RegexValidator(regex=r'^[a-zA-Z][a-zA-Z ]+$',message='Only alphabets allowed, please enter your name again.')])
    fatherName = forms.CharField(label='Father\'s Name',max_length=25, validators=[validator.RegexValidator(regex=r'^[a-zA-Z][a-zA-Z ]+$',message='Only alphabets allowed, please enter your father\'s name again.')])
    dob = forms.DateField(
        label = 'Date of Birth',
        help_text='Date format to be used: dd/mm/yyyy',
        widget=forms.DateInput(format='%d/%m/%Y'),
        input_formats=('%d/%m/%Y', ),
        error_messages={'invalid':'Please specify date in the mentioned format.'}
        )
    gender = forms.ChoiceField(label='Gender', choices = ((1,'Male'),(2,'Female')))
    condition = forms.CharField(label='Condition', max_length=250,help_text='Please enter the conditions in a comma separated list.')
    area = forms.CharField(label='Area/City', max_length=100, validators=[validator.RegexValidator(regex=r'^[a-zA-Z][a-zA-Z ]+$',message='Only alphabets allowed, please enter area name again.')])
    mobileNumber = forms.CharField(label='Mobile Number',help_text='Please enter the caregiver\'s mobile number in format: 03xxxxxxxxx', max_length=11,validators=[validator.RegexValidator(regex=r'^[0][3][0-9]+$',message='Invalid mobile number, please enter again.')])
    username=forms.CharField(label='User Name',help_text='Note: User Name cannot be duplicate',max_length=25,validators=[username_val])
    password = forms.CharField(label='Password',max_length=10, help_text='Note: Password cannot be less than 6 charactors and not more than 10',widget=forms.PasswordInput,validators=[validator.MinLengthValidator(limit_value=6)])
    passwordRe= forms.CharField(label='Re-enter Password',max_length=10, help_text='Note: Please enter the password again', widget=forms.PasswordInput,validators=[validator.MinLengthValidator(limit_value=6)])

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        passwordre = cleaned_data.get("passwordRe")
        if password!=passwordre:
            self.add_error('passwordRe', 'The passwords does not match.')

class PatientEditForm(forms.Form):
    name = forms.CharField(label='Full Name',max_length=25, validators=[validator.RegexValidator(regex=r'^[a-zA-Z][a-zA-Z ]+$',message='Only alphabets allowed, please enter your name again.')])
    fatherName =forms.CharField(label='Father\'s Name',max_length=25, validators=[validator.RegexValidator(regex=r'^[a-zA-Z][a-zA-Z ]+$',message='Only alphabets allowed, please enter your father\'s name again.')])
    dob = forms.DateField(
        label='Date of Birth',
        help_text='Date format to be used: dd/mm/yyyy',
        widget=forms.DateInput(format='%d/%m/%Y'),
        input_formats=('%d/%m/%Y',),
        error_messages={'invalid': 'Please specify date in the mentioned format.'}
    )
    gender = forms.ChoiceField(label='Gender', choices = ((1,'Male'),(2,'Female')))
    condition = forms.CharField(label='Condition', max_length=250,
                                help_text='Please enter the conditions in a comma separated list.')
    area = forms.CharField(label='Area/City', max_length=100, validators=[
        validator.RegexValidator(regex=r'^[a-zA-Z][a-zA-Z ]+$',
                                 message='Only alphabets allowed, please enter area name again.')])
    mobileNumber = forms.CharField(label='Mobile Number',
                                   help_text='Please enter the caregiver\'s mobile number in format: 03xxxxxxxxx',
                                   max_length=11, validators=[
            validator.RegexValidator(regex=r'^[0][3][0-9]+$', message='Invalid mobile number, please enter again.')])


class PatientPasswordChangeForm(forms.Form):
    username = forms.CharField(label = 'User Name', widget = forms.TextInput(attrs={'readonly':'readonly'}))
    password = forms.CharField(label='Password', max_length=10,
                               help_text='Note: Password cannot be less than 6 charactors and not more than 10',
                               widget=forms.PasswordInput, validators=[validator.MinLengthValidator(limit_value=6)])
    passwordRe = forms.CharField(label='Re-enter Password', max_length=10,
                                 help_text='Note: Please enter the password again', widget=forms.PasswordInput,
                                 validators=[validator.MinLengthValidator(limit_value=6)])

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        passwordre = cleaned_data.get("passwordRe")
        if password != passwordre:
            self.add_error('passwordRe', 'The passwords does not match.')

class PatientLogForm(forms.Form):
    message = forms.CharField(label='اہم واقعہ لکھیں', max_length=500, widget=forms.Textarea)

class AddReportForm(forms.Form):
    Name = forms.CharField(label='Item Name',max_length=25, validators=[validator.RegexValidator(regex=r'^[a-zA-Z][a-zA-Z\s]+[0-9]*$',message='Name needs to be alphabets followed by optional space and/or optional numeric digits.')])
    FilePath = forms.FileField(help_text='<br/>File formats:<br/>Image : png<br/>PDF : pdf')

    def clean(self):
        cleaned_data = super().clean()
        File = cleaned_data.get("FilePath").name
        Fileobj=cleaned_data.get("FilePath")
        if not ( File.endswith('.png')  or File.endswith('.pdf')):
            self.add_error('FilePath', 'Please select .png for Image or .pdf for PDF')
        elif Fileobj.size > settings.MAXFILESIZE:
            self.add_error('FilePath','Maximum file size is 50MB')

class TrackNameForm(forms.Form):
    trackName = forms.CharField(label='Track Name',help_text='Please name your track, remember a track is a collection of exercises',max_length=30, validators=[validator.RegexValidator(regex=r'^[a-zA-Z][a-zA-Z\s]+[0-9]*$',message='Name needs to be alphabets followed by optional space and/or optional numeric digits.')])

class TrackAssignForm(forms.Form):
    duration = forms.IntegerField(label="Duration" ,help_text ='In number of weeks.', max_value = 10)
    notes = forms.CharField(label='Instructions', max_length=1000, widget =forms.Textarea, help_text = "Please write the instructions in Urdu.")

