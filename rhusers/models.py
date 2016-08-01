from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext as _
from iso3166 import countries_by_alpha2


def country_name_validator(code):
    if code.upper() not in countries_by_alpha2.keys():
        raise ValidationError(_('Incorrect country code'))


class IBANProfile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    country_code = models.CharField(_('country code'), max_length=2, validators=[country_name_validator])
    check_digits = models.DecimalField(_('check digits'), max_digits=2, decimal_places=0)
    bban = models.CharField(_('basic bank account number'), max_length=30, validators=[RegexValidator(r'^[0-9a-zA-Z]*$')])
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created', null=True)

    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')
