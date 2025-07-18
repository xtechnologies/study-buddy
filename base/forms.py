from django.forms import ModelForm
from .models import Room
from django import forms
from .models import Profile
from django.contrib.auth.models import User

class Roomform(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'about']  # ✅ Include "about"
        widgets = {
            'about': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write something about yourself...'
            }),
        }