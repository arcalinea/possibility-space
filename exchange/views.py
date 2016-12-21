from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import logging, logging.handlers

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from forms import RegistrationForm, LoginForm, GiftMatch, RequestForm, ProfileForm
from models import Profile, Category, Exchange

from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import csrf, request

from django.core.mail import send_mail

from django.contrib import messages

from utils import invite_code
import datetime
import json

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
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        logging.debug("FORM IS VALID")
        user = form.login(request)
        if user:
            login(request, user)
            #Redirect to a success page.
            return HttpResponseRedirect('/exchange/participate/dashboard')
    return render(request, 'accounts/login.html', {'login_form': form})
    logging.debug("Not using post method")

def logout_view(request):
    logging.debug("LOGGING OUT")
    logout(request)
    return HttpResponseRedirect('/')

def participate_dashboard(request, args):
    storage = messages.get_messages(request)
    print "STORAGE", storage
    #TODO: Create or edit profile, depending on user profile status
    user = request.user
    requests = Exchange.objects.filter(receiver=user.id)
    gifts = Exchange.objects.filter(giver=user.id)
    logging.debug("CURRENT USER=%s", user)
    return render(request, 'exchange/participate/dashboard.html', {'requests': requests, 'gifts': gifts})

#####
def create_profile(request, args):
    user_id = request.user.id
    logging.debug("TEST CREATE PROFILE")
    profile = Profile.objects.get(id=user_id)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            print "CREATE PROFILE FORM VALID"
            form.save()
            return HttpResponseRedirect('/participate/profile')
    else:
        form = ProfileForm(instance=profile)
        return render(request, 'accounts/create_profile.html', {'form': form})

def display_profile(request, args):
    user = request.user
    profile = Profile.objects.get(id=user.id)
    return render(request, 'accounts/profile.html', {'profile': profile})

def invite_friends(request, args):
    if request.method == "POST":
        # TODO: Count number of invites, add to user profile
        # TODO: Generate invite code, send emails
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
        invite = invite_code()
        logging.debug("INVITE CODE=%s", invite)
        return render(request, 'accounts/invite_success.html', {'invite': invite})
    else:
        return render(request, 'accounts/invite_friends.html')

def invite_success(request, invite):
    print "IN INVITE SUCCESS", invite
    return render(request, 'accounts/invite_success.html', {'invite': invite})

def enter_invite(request, args):
    if request.method == "POST":
        return HttpResponse("Invitate code success")
    else:
        return render(request, 'accounts/enter_invite.html')

def create_request(request):
    form = RequestForm(request.POST or None)
    num_req = Exchange.objects.filter(receiver=request.user.id).count()
    if num_req >= 1:
        messages.error(request, "Looks like you've already created a request")
        return redirect('/exchange/participate/dashboard')
    else:
        if request.POST and form.is_valid():
            gift_request = form.gift_request(request)
            print "GIFT", gift_request
            return HttpResponseRedirect('/exchange/participate/dashboard')
        return render(request, 'exchange/participate/create_request.html')

def create_gift(request):
    form = GiftMatch(request.POST or None)
    if request.POST and form.is_valid():
        gift_req = form.match(request)
        print "ITEM MATCH", gift_req
        return render(request, 'exchange/participate/accept_match.html', {'item': gift_req})
    else:
        return render(request, 'exchange/participate/give_gift.html')

def accept_match(request, item):
    print "In ACCEPT MATCH"
    return render(request, 'exchange/participate/accept_match.html', {'item', item})

def confirm_gift(request):
    print "IN CONFIRM GIFT"
    if request.POST and request.is_ajax():
        print "Request was post"
        item_id = request.POST['item_id']
        match = Exchange.objects.get(id=item_id)
        id = request.user.id
        print "ID", id
        profile = Profile.objects.get(id=id)
        match.giver = profile
        match.save()
        return HttpResponseRedirect('/exchange/participate/dashboard')
    else:
        return HttpResponseRedirect('/exchange/participate/dashboard')

def gift_complete(request):
    return render(request, 'exchange/participate/gift_complete.html')

def request_complete(request):
    return render(request, 'exchange/participate/request_complete.html')
