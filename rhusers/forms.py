from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator

from rhusers.models import country_name_validator, IBANProfile


class UserUpdateForm(forms.ModelForm):

    country_code = forms.CharField(max_length=2, validators=[country_name_validator])
    check_digits = forms.IntegerField(max_value=99)
    bban = forms.CharField(max_length=30, validators=[RegexValidator(r'^[0-9a-zA-Z]*$')])

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        try:
            profile = self.instance.profile
        except ObjectDoesNotExist:
            pass
        else:
            self.fields['country_code'].initial = profile.country_code
            self.fields['check_digits'].initial = profile.check_digits
            self.fields['bban'].initial = profile.bban

    def save(self, commit=True):
        super(UserUpdateForm, self).save(commit)
        try:
            profile = self.instance.profile
        except ObjectDoesNotExist:
            IBANProfile.objects.create(
                user=self.instance,
                country_code=self.cleaned_data['country_code'],
                check_digits=self.cleaned_data['check_digits'],
                bban=self.cleaned_data['bban']
            )
        else:
            profile.country_code = self.cleaned_data['country_code']
            profile.check_digits = self.cleaned_data['check_digits']
            profile.bban = self.cleaned_data['bban']
            profile.save()

    class Meta:
        model = get_user_model()
        fields = ['username', 'last_name', 'first_name', 'email']