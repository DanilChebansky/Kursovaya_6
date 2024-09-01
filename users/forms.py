from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from mailings.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(UserCreationForm, StyleFormMixin):
    class Meta:
        model = User
        fields = ("email", 'password1', 'password2')


class UserProfileForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
