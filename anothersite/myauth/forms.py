from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import Group
from .models import Profile




class ProfileForm(forms.ModelForm):
    class Meta:
       model = Profile
       fields = 'user', 'bio', 'agreement_accepted', 'avatar',

