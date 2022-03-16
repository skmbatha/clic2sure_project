"""Django database models for financials project."""

from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


class CreditAccount(models.Model):
    """This is a database models.Model  
    
    This class defined the database table schema for the
    credit accounts table.
    
    Attributes
    ----------
    user : User
        This field holds the Account owner (User)'s foreign key
    Balance : float
        This fields shows the balance in the account.
        
     Methods
    ----------
    print_csv(self):
        This prints the CSV type output for the account
    __str__(self):
        This methods returns a text descriptino of the account
    """
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0,validators = [MinValueValidator(-20000.0),])

    def print_csv(self):
        """This method returns a dictionary representing one row for a csv file"""
        
        return {'Account':'Credit','Balance':str(self.balance),'User':str(self.user)}
    
    def __str__(self):
        """This methods returns a text descriptino of the account"""
        
        return "Account type: Credit (acc_id: {}), Balance: R{}".format(str(self.pk),str(self.balance))


class SavingsAccount(models.Model):
    """This is a database models.Model  
    
    This class defined the database table schema for the
    savings accounts table.
    
    Attributes
    ----------
    user : User
        This field holds the Account owner (User)'s foreign key
    Balance : float
        This fields shows the balance in the account.
        
     Methods
    ----------
    print_csv(self):
        This prints the CSV type output for the account
    __str__(self):
        This methods returns a text descriptino of the account
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.FloatField(validators = [MinValueValidator(50.0),], blank=False)

    def print_csv(self):
        """This method returns a dictionary representing one row for a csv file"""
    
        return {'Account':'Savings','Balance':str(self.balance),'User':str(self.user)}
    
    def __str__(self):
        """This methods returns a text descriptino of the account"""
    
        return "Account type: Savings (acc_id: {})- Balance: R{}".format(str(self.pk),str(self.balance))


class Transaction(models.Model):
    """This is a database models.Model  
    
    This class defined the database table schema for the
    transactions table.
    
    Attributes
    ----------
    user : User
        This field holds the Account owner (User)'s foreign key
    account_type:str
        This fields holds the account type information, it can eithwe be : SAVINGS or CREDIT
    account_id:int
        Since a user can have multiplen accounts, this value holds the account id as
        as addition to the account_type
    transaction_type:str
        This fields holds the transaction type. It can either be WITHDRAWAL OR DEPOSIT
    amount:float
        This value holds the transaction amount, e.g A widthdrawal/deposit of <amount>
    balance:float
        This value shows the remainint account balance after the tyransaction
        was done.
    
     Methods
    ----------
    __str__(self):
        This methods returns a text descriptino of the account
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_type=models.CharField(max_length=7) # SAVINGS OR CREDIT
    account_id=models.IntegerField(default=-1) # ACCOUNT ID
    transaction_type=models.CharField(max_length=11) # WITHDRAWAL OR DEPOSIT
    transaction_date= models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(default=0)
    balance = models.FloatField(default=0)
    
    def __str__(self):
        """This methods returns a text descriptino of a transaction"""
    
        return "{} of R{} in {} account(id={}) - Remaining balance : R{}".format(str(self.transaction_type).capitalize(),str(self.amount),self.account_type.capitalize(),str(self.account_id),str(self.balance))