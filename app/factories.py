"""Dummy data creator module for database

More informatio about this is found at
https://mattsegal.dev/django-factoryboy-dummy-data.html
"""

import factory
from factory.django import DjangoModelFactory
from .models import CreditAccount,SavingsAccount,Transaction
from django.contrib.auth.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model=User

    username=factory.Faker("first_name")


class SavingsAccountFactory(DjangoModelFactory):
    class Meta:
        model= SavingsAccount

    user= factory.SubFactory(UserFactory)

class CreditAccountFactory(DjangoModelFactory):
    class Meta:
        model= CreditAccount

    user= factory.SubFactory(UserFactory)

class TransactionsFactory(DjangoModelFactory):
    class Meta:
        model= Transaction

    user = factory.SubFactory(UserFactory)
