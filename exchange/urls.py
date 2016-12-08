from django.conf.urls import url
from . import views

# from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(explore)$', views.explore_index, name='explore_index'),
    url(r'^(participate)$', views.participate_index, name='participate_index'),
    url(r'^(participate/dashboard)$', views.participate_dashboard, name='participate_dashboard'),
    # url(r'^(participate/signup)', views.sign_up, name='signup'),

    url(r'^participate/request$', views.create_request, name="create_request"),
    url(r'^participate/give$', views.create_gift, name="create_gift"),

    url(r'^login/$', views.auth_login, name='auth_login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register/success/$', views.register_success, name='register_success'),

    # url(r'^accounts/register/$', views.register, name='register'),
    # url(r'^accounts/register/complete/$', views.registration_complete, name='registration_complete'),
    # url(r'^accounts/login/$', views.login, name='login'),


]
