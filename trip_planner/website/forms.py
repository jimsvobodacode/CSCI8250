from django import forms
# from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm


class IndexForm(forms.Form):
    prompt = forms.CharField(required=True)
    