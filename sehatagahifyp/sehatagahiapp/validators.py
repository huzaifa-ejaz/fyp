from django.core.exceptions import ValidationError

def file_size(value):
    filesize=value.size
    if filesize>4194304000:
        raise ValidationError("maximum size is 500MB")
