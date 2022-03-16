""" This module defined the models that are shown in admin

...
"""

from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import CreditAccount,SavingsAccount,Transaction
from rest_framework.authtoken.models import Token

# Register your models here.
admin.site.register(CreditAccount)
admin.site.register(SavingsAccount)
admin.site.register(Transaction)
