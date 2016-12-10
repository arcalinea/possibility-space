from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import logging, logging.handlers

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from forms import RegistrationForm
from models import Profile, Category, Exchange

from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import csrf, request

from django.core.mail import send_mail

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
            login(request, user)
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
    #TODO: Create or edit profile, depending on user profile status
    user = request.user
    profile = Profile.objects.get(id=user.id)
    logging.debug("Profile BIO=%s", profile.bio)
    logging.debug("CURRENT USER=%s", user)
    return render(request, 'exchange/participate/dashboard.html', {'profile': profile})

#####
def create_profile(request, args):
    # If user already has a profile, display?
    if request.method == "POST":
        logging.debug("TEST CREATE PROFILE")
        user_id = request.user.id
        profile = Profile.objects.get(id=user_id)
        if profile is not None:
            logging.debug("Profile User Name=%s", profile)
            # You can't overwrite to edit this right now
            profile.bio = request.POST.get('bio')
            profile.address = request.POST.get('address')
            logging.debug("Profile Bio=%s", profile.bio)
            profile.save()
            return HttpResponseRedirect('/exchange/participate/dashboard')
    else:
        return render(request, 'accounts/create_profile.html')

def invite_friends(request, args):
    if request.method == "POST":
        logging.debug("TEST INVITE FRIENDS")
        name = request.POST.get('name')
        email = request.POST.get('email')
        # logging.debug("TEST EMAIL=%s", email)
        # send_mail(
        #     "You've been invited to a secret santa gift exchange",
        #     'Visit possibility.space to participate',
        #     'possibility.space@gmail.com',
        #     [email],
        #     fail_silently=False,
        # )
        return HttpResponseRedirect('/exchange/participate/dashboard')
    else:
        return render(request, 'accounts/invite_friends.html')


def create_request(request):
    if request.method == "POST":
        user = request.user
        category = request.POST.get('category')
        link = request.POST.get('link')
        description = request.POST.get('description')
        receiver = Profile.objects.get(id=user.id)
        logging.debug("TEST receiver profile=%s", receiver)
        gift = Exchange(link=link, description=description, receiver=receiver)
        if gift is not None:
            print "gift desc: ", gift.description
            print "gift receiver: ", gift.receiver
            # gift.save()
        return render(request, 'exchange/participate/dashboard.html')
    else:
        return render(request, 'exchange/participate/create_request.html')

def create_gift(request):
    # Return requests in these categories
    if request.method == "POST":
        logging.debug("TEST POST GIFT")
        return render(request, 'exchange/participate/dashboard.html')
    else:
        return render(request, 'exchange/participate/give_gift.html')
