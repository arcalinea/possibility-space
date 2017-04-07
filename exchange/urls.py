from django.conf.urls import url
from . import views

# from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(explore)$', views.explore_index, name='explore_index'),
    url(r'^(participate)$', views.participate_index, name='participate_index'),
    url(r'^(participate/dashboard)$', views.participate_dashboard, name='participate_dashboard'),
    url(r'^(participate/create-profile)$', views.create_profile, name='create_profile'),
    url(r'^(participate/profile)$', views.display_profile, name='display_profile'),

    url(r'^(participate/invite)$', views.invite_friends, name='invite_friends'),
    url(r'^(participate/invite/success)$', views.invite_success, name='invite_success'),
    url(r'^(participate/enter-invite)$', views.enter_invite, name='enter_invite'),

    url(r'^participate/request$', views.create_request, name="create_request"),
    url(r'^participate/give$', views.create_gift, name="create_gift"),
    url(r'^participate/give/match$', views.accept_match, name="accept_match"),
    url(r'^participate/give/confirm$', views.confirm_gift, name="confirm_gift"),
    url(r'^participate/give/complete$', views.gift_complete, name="gift_complete"),
    url(r'^participate/request/complete$', views.request_complete, name="request_complete"),


    url(r'^login/$', views.auth_login, name='auth_login'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register/success/$', views.register_success, name='register_success'),

    # url(r'^accounts/register/$', views.register, name='register'),
    # url(r'^accounts/register/complete/$', views.registration_complete, name='registration_complete'),
    # url(r'^accounts/login/$', views.login, name='login'),


]
