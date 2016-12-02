from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(explore)$', views.explore_index, name='explore_index'),
    url(r'^(participate)$', views.participate_index, name='participate_index'),
]
