from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

def file_size(value):
    filesize=value.size
    if filesize>4194304000:
        raise ValidationError("maximum size is 500MB")
def username_val(value):
    if value.isnumeric():
        raise ValidationError("All numeric username not allowed")
    users = get_user_model().objects.all()
    for user in users:
        if value==user.username:
            raise ValidationError("Username already present")
            break


