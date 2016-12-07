from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import logging, logging.handlers

from django.contrib.auth.models import User
# from .forms import SignupForm
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import csrf, request

from forms import RegistrationForm

# Create your views here.

def index(request):
    return render(request, 'exchange/index.html')

def explore_index(request, args):
    return render(request, 'exchange/explore/index.html')

def participate_index(request, args):
    return render(request, 'exchange/participate/index.html')

#####
def register(request):
    logging.debug("IN AUTH_REGISTER")
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
            email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
        else:
            form = RegistrationForm()
            variables = RequestContext(request, {
            'form': form
            })
            return render_to_response(
            'accounts/registration_form.html',
            variables,
            )
    else:
        logging.debug("Rendering registration form")
        return render(request, 'accounts/registration_form.html')
        logging.debug("Not using post method")
    # return HttpResponse("Register")

# @csrf_protect
def register_success(request):
     return render(request, 'accounts/registration_complete.html')

def auth_login(request):
    logging.debug("IN LOGIN METHOD")
    if request.method == "POST":
        logging.debug("TEST POST")
        username = request.POST.get('username')
        password = request.POST.get('password')
        logging.info('username=%s', username)
        logging.info("password=%s", password)
        user = authenticate(username=username, password=password)
        if user is not None:
            logging.debug("User is authenticated")
            # Redirect to a success page.
            return HttpResponseRedirect('/exchange/participate/dashboard')
        else:
            return HttpResponse("Not signed in")
    else:
        return render(request, 'accounts/login.html')
        logging.debug("Not using post method")

def logout(request):
    logging.debug("LOGGING OUT")
    return render(request, '/accounts/logout.html')

def participate_dashboard(request, args):
    user = request.user
    logging.debug("CURRENT USER=%s", user)
    return render(request, 'exchange/participate/dashboard.html')
