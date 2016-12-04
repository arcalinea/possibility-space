from django import forms

class SignupForm(forms.Form):
    username = forms.CharField(label='username', max_length='100')
    email = forms.CharField()
    password = forms.CharField()
