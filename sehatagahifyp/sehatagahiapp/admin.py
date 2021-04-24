from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .models import Item
from sehatagahiapp.models import Therapist



# Register your models here.
admin.site.register(User)
admin.site.register(Therapist)
