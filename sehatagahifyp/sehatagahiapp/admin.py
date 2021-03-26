from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .models import Item
from sehatagahiapp.models import Therapist

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class TherapistInline(admin.StackedInline):
    model = Therapist
    can_delete = False
    verbose_name_plural = 'therapist'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (TherapistInline,)

# Register your models here.
#admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Item)