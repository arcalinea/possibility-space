import re, random, datetime
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import authenticate

from models import Category, Exchange, Profile

# class SignupForm(forms.Form):
#     username = forms.CharField(label='username', max_length='100')
#     email = forms.CharField()
#     password = forms.CharField()

class GiftMatch(forms.Form):
    category = forms.CharField(max_length=255, required=True)

    def match(self, request):
        category = self.cleaned_data.get('category')
        requests = Exchange.objects.filter(category=category, complete=False)
        possibilities = []
        for req in requests:
            if req.receiver.id != request.user.id:
                possibilities.append(req)
        print "Possibilities", possibilities
        gift_req = random.choice(possibilities)
        return gift_req


class RequestForm(forms.Form):
    category = forms.CharField(max_length=255, required=True)
    link = forms.CharField(max_length=255, required=False)
    description = forms.CharField(max_length=1000, required=True)

    def gift_request(self, request):
        user = request.user
        c_id = self.cleaned_data.get('category')
        category = Category.objects.get(id=c_id)
        link = self.cleaned_data.get('link')
        description = self.cleaned_data.get('description')
        receiver = Profile.objects.get(id=user.id)
        gift = Exchange(category=category, link=link, description=description, receiver=receiver, request_date=datetime.datetime.now())
        if gift is not None:
            print "gift desc: ", gift.description
            print "gift receiver: ", gift.receiver
            print "gift link: ", gift.link
            print "gift category: ", gift.category
            gift.save()
            return gift

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

class RegistrationForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    password = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password (again)"))

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))

    def clean(self):
        if 'password' in self.cleaned_data and 'confirm_password' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'address']
        widgets = {
            'bio': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Bio', 'rows': '3', 'form': 'profile-form', 'name': 'bio'}
            ),
            'address': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Address', 'rows': '3', 'form': 'profile-form', 'name': 'address'}
            ),
        }
    #
    # bio = forms.CharField(
    #     label='Bio',
    #     widget=forms.Textarea(
    #         attrs={'class': 'form-control', 'placeholder': 'Bio', 'rows': '3', 'form': 'profile-form', 'name': 'bio'}
    #     )
    # )
    # address = forms.CharField(
    #     label='Your Address',
    #     widget=forms.Textarea(
    #         attrs={'class': 'form-control', 'placeholder': 'Address', 'rows': '3', 'form': 'profile-form', 'name': 'address'}
    #     )
    # )




        # if request.method == "POST":
        #     logging.debug("TEST CREATE PROFILE")
        #     user_id = request.user.id
        #     profile = Profile.objects.get(id=user_id)
        #     logging.debug("Profile User Name=%s", profile)
        #     # You can't overwrite to edit this right now
        #     profile.bio = request.POST.get('bio')
        #     profile.address = request.POST.get('address')
        #     logging.debug("Profile Bio=%s", profile.bio)
        #     profile.save()
