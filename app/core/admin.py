from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models


""" This class creted for updating admin for support custom user model"""


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
         (None, {'fields': ('email', 'password')}),
         (_('Personal Info'), {'fields': ('name',)}),
         (_
             ('Permissions'),
             {'fields': ('is_active', 'is_staff', 'is_superuser')}),
         (_('Important dates'), {'fields': ('last_login',)})
        )
    # It was from django doc's and no more explain
    add_fieldsets = (
         (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
         }),
        )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Tag)
admin.site.register(models.Ingredient)