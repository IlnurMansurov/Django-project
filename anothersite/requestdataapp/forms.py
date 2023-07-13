from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError

class UserBioForm(forms.Form):
    name = forms.CharField(max_length=100)
    age = forms.IntegerField(label='Yor age', min_value=1, max_value=120)
    bio = forms.CharField(label='Biography', widget=forms.Textarea)


def validate_file_name(file: InMemoryUploadedFile) ->None:
    if file.name and 'virus' in file.name:
        raise ValidationError('file name should not contain "virus')
    elif file.size >1024:
        raise ValidationError('The file size must be under 10 MB')


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validate_file_name])