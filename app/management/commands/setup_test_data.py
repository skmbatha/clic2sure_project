from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from app.models import CreditAccount,SavingsAccount,Transaction
from app.factories import UserFactory,CreditAccountFactory,SavingsAccountFactory,TransactionsFactory

import random
from django.db import transaction
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import ( PBKDF2PasswordHasher)


NUM_USERS = 5
NUM_SAVINGS_ACCOUNTS = 30
NUM_CREDIT_ACCOUNTS = 20
NUMBER_OF_TRANSACTIONS = 100


class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):

        self.stdout.write("Deleting old data...")
        models = [User, SavingsAccount, CreditAccount, Transaction]
        for m in models:
            if m is not User:
                m.objects.all().delete()
            else:
                users=m.objects.all()
                for user in users:
                    if user.username!='admin':
                        user.delete()


        self.stdout.write("Creating new data...")
        users = []
        for u in range(NUM_USERS):
            hasher=PBKDF2PasswordHasher()
            person = UserFactory(password=hasher.encode('pass','salt'),email='user{}@mail.com'.format(u))
            users.append(person)

            Token.objects.get_or_create(user=person)

        
        self.stdout.write("Creating savings accounts for all users...")
        savings_accs=[]
        for _ in range(NUM_SAVINGS_ACCOUNTS):
            savings_acc = SavingsAccountFactory(user=users[random.randint(0, len(users)-1)],balance=float(random.randint(50, 1000)))
            savings_accs.append(savings_acc)
        

        self.stdout.write("Creating credit accounts for all users...")
        credit_accs=[]
        for u in range(NUM_CREDIT_ACCOUNTS):
            credit_acc = CreditAccountFactory(user=users[random.randint(0, len(users)-1)],balance=float(random.randint(-20000, 50000)))
            credit_accs.append(credit_acc)


        self.stdout.write("Creating transactions for all users...")
        for t in range(NUMBER_OF_TRANSACTIONS):
            account_type=['SAVINGS','CREDIT'][random.randint(0, 1)]
            transaction_type=['WITHDRAWAL','DEPOSIT'][random.randint(0, 1)]
            amount = float(random.randint(0, 1000))

            acc=savings_accs[random.randint(0, len(savings_accs)-1)] if account_type=="SAVINGS" else credit_accs[random.randint(0, len(credit_accs)-1)]
            
            user=acc.user
            account_id=acc.id

            if account_type=='SAVINGS':
                balance_init=SavingsAccount.objects.get(pk=account_id).balance
                new_amnt=balance_init+amount if transaction_type=="DEPOSIT" else balance_init-amount
                if(new_amnt>=50):
                    TransactionsFactory(
                        user=user,
                        account_type=account_type,
                        transaction_type=transaction_type,
                        amount=amount,
                        account_id=account_id,
                        balance=new_amnt
                    )
                
            else:
                balance_init=CreditAccount.objects.get(pk=account_id).balance
                new_amnt=balance_init+amount if transaction_type=="DEPOSIT" else balance_init-amount
                if(new_amnt>=-20000):
                    TransactionsFactory(
                        user=user,
                        account_type=account_type,
                        transaction_type=transaction_type,
                        amount=amount,
                        account_id=account_id,
                        balance=new_amnt
                    )

            

            