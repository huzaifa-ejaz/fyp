from .models import Item
from django import forms


class Item_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(Item_form, self).__init__(*args, **kwargs)
    class Meta:
        model=Item
        fields=("Name","FilePath","Type")

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=60)
    password = forms.CharField(label="Password", widget = forms.PasswordInput(), max_length=60)
