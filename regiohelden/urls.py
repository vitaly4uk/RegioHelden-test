"""regiohelden URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test

from rhusers.views import UserListView, UserDetailView, UserUpdateView, UserDeleteView, UserCreateView


def is_staff_check(user):
    return user.is_staff

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^create/$', user_passes_test(is_staff_check)(UserCreateView.as_view())),
    url(r'^(?P<pk>[0-9]*)/delete/$', user_passes_test(is_staff_check)(UserDeleteView.as_view())),
    url(r'^(?P<pk>[0-9]*)/edit/$', user_passes_test(is_staff_check)(UserUpdateView.as_view())),
    url(r'^(?P<pk>[0-9]*)/$', UserDetailView.as_view()),
    url(r'^$', UserListView.as_view()),
]
