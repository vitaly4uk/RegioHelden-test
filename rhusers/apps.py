from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _


def create_user_profile_dispatcher(*args, **kwargs):
    if kwargs['created'] and not kwargs['raw']:
        from rhusers.models import IBANProfile
        IBANProfile.objects.create(user=kwargs['instance'])


class RHUsersConfig(AppConfig):
    name = 'rhusers'
    verbose_name = _('RHUser')

    def ready(self):
        post_save.connect(create_user_profile_dispatcher, sender=get_user_model())