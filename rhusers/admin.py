from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from rhusers.models import IBANProfile


class IBANProfileInline(admin.StackedInline):
    model = IBANProfile
    can_delete = False
    verbose_name = _('user profile')
    verbose_name_plural = _('user profiles')
    extra = 1
    max_num = 1
    min_num = 1
    fk_name = 'user'


class UserAdmin(BaseUserAdmin):
    inlines = [IBANProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)