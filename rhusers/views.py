from django.contrib.auth import get_user_model
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.list import ListView

from rhusers.forms import UserUpdateForm


class UserListView(ListView):
    template_name = 'index.html'
    context_object_name = 'users'

    def get_queryset(self):
        User = get_user_model()
        return User.objects.all()

class UserDetailView(DetailView):
    template_name = 'detail.html'
    context_object_name = 'user'

    def get_queryset(self):
        User = get_user_model()
        return User.objects.all()


class UserUpdateView(UpdateView):
    template_name = 'update.html'
    form_class = UserUpdateForm

    def get_success_url(self):
        return '/'

    def get_queryset(self):
        User = get_user_model()
        return User.objects.all()


class UserDeleteView(DeleteView):
    template_name = 'delete.html'
    context_object_name = 'user'

    def get_success_url(self):
        return '/'

    def get_queryset(self):
        User = get_user_model()
        return User.objects.all()


class UserCreateView(CreateView):
    template_name = 'update.html'
    form_class = UserUpdateForm

    def get_success_url(self):
        return '/'

    def get_queryset(self):
        User = get_user_model()
        return User.objects.all()