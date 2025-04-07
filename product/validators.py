from django.core.exceptions import ValidationError

def validate_file_size(file):
    """
       This validator if file size is less than 10 mb

    """
    max_size = 50
    max_size_in_bytes = 10 * 1024 * 1024

    if file.size > max_size_in_bytes:
        raise ValidationError("File can not be larger than {max_size}MB")