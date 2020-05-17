from django import forms
from django.contrib.auth.models import User
from basic_app.models import UserProfileInfo

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput()) # need to add this one as we don t have it in the User class by default

    class Meta():
        model = User
        fields = ("username", "email", "password") # will be saved automatically in the database


class UserProfileInfoForm(forms.ModelForm):

    class Meta():
        model = UserProfileInfo
        fields = ("portfolio_site", "profile_pic") # saved in the database

