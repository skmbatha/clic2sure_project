from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import CreditAccount,SavingsAccount

__author__ = "Katlego"


 # USER PROFILE TESTSS

class UserTests(APITestCase):
    """This test case is testing requirement 1"""
    
    def test_create_user_account(self):
        """Create a user accout in the empty database, then check if there is 1 user and gthe status code=200 """
        
        #Create user
        url = 'http://localhost:8000/createuser/'
        data = {'username': 'user1','password':'user1','email':'user1@mail.com'}
        response = self.client.post(url, data, format='json')

        #check if user is created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().filter(username='user1').count(), 1)
        
    def test_login_to_user_account(self):
        """Login to the user account using the API and then check the status code : 200"""
        
        #create user
        url = 'http://localhost:8000/createuser/'
        data = {'username': 'user1','password':'user1','email':'user1@mail.com'}
        response = self.client.post(url, data, format='json')
        
        #login with user
        url = 'http://localhost:8000/login/'
        data = {'username': 'user1','password':'user1'}
        response = self.client.post(url, data, format='json')
        
        #check if the user successfully loged in
        self.assertEqual(response.data['user_id'],User.objects.all().filter(username='user1')[0].pk)
        self.assertEqual(response.status_code,200)
        
 
# SAVINGS ACCOUNT 

class SavingsAccountTests(APITestCase):
    """This test case is testing requirement 2 and 6"""
    
    def test_create_savings_account_with_initial_balance_more_than_50(self):
        """ Ensure that we can create a savings account with the initial balance >= R50, Expected result: We should get status=200"""
        
        #create user
        url = 'http://localhost:8000/createuser/'
        data = {'username': 'user1','password':'user1','email':'user1@mail.com'}
        response = self.client.post(url, data, format='json')
        
        #login with user
        url = 'http://localhost:8000/login/'
        data = {'username': 'user1','password':'user1'}
        response = self.client.post(url, data, format='json')
        
        # Get authentication token
        token=response.data['token']
        
        
        # Make a create a savings account
        url = 'http://localhost:8000/savings/'
        data = {'balance':100}
        response = self.client.post(url, data, format='json',**{'HTTP_AUTHORIZATION':'Token {}'.format(token)})
        self.assertEqual(response.status_code,200)
        
    def test_create_savings_account_with_initial_balance_less_than_50(self):
        """ Ensure that we can create a savings account width initial balance < R50, Expected result: We should get status=400 """
        
        #create user
        url = 'http://localhost:8000/createuser/'
        data = {'username': 'user1','password':'user1','email':'user1@mail.com'}
        response = self.client.post(url, data, format='json')
        
        #login with user
        url = 'http://localhost:8000/login/'
        data = {'username': 'user1','password':'user1'}
        response = self.client.post(url, data, format='json')
        
        # Get authentication token
        token=response.data['token']
        
        
        # Make a create a savings account
        url = 'http://localhost:8000/savings/'
        data = {'balance':20}
        response = self.client.post(url, data, format='json',**{'HTTP_AUTHORIZATION':'Token {}'.format(token)})
        self.assertEqual(response.status_code,400)
        
    def test_update_savings_account_to_a_new_initial_balance(self):
        """ Update the initial amount of R200 to a new amount of R300 and test if's it's updated"""
        
        #create user
        url = 'http://localhost:8000/createuser/'
        data = {'username': 'user1','password':'user1','email':'user1@mail.com'}
        response = self.client.post(url, data, format='json')
        
        #login with user
        url = 'http://localhost:8000/login/'
        data = {'username': 'user1','password':'user1'}
        response = self.client.post(url, data, format='json')
        
        # Get authentication token
        token=response.data['token']
        
        
        # Make a create a savings account
        url = 'http://localhost:8000/savings/'
        data = {'balance':200}
        response = self.client.post(url, data, format='json',**{'HTTP_AUTHORIZATION':'Token {}'.format(token)})  

        # Update a savings account
        user=User.objects.get(username='user1')
        savings_acc=SavingsAccount.objects.all().filter(user_id=user.pk)[:1][0]
        url = 'http://localhost:8000/savings/?acc_id={}'.format(str(savings_acc.pk))
        data = {'balance':300}
        response = self.client.patch(url, data, format='json',**{'HTTP_AUTHORIZATION':'Token {}'.format(token)})
        
        self.assertEqual(response.status_code,200)
        self.assertEqual(SavingsAccount.objects.all().filter(user_id=user.pk)[:1][0].balance,300)
        
    def test_delete_a_savings_account(self):
        """ Delete the savings account and then check if we have zero savings accounts for the user"""
        
        #create user
        url = 'http://localhost:8000/createuser/'
        data = {'username': 'user1','password':'user1','email':'user1@mail.com'}
        response = self.client.post(url, data, format='json')
        
        #login with user
        url = 'http://localhost:8000/login/'
        data = {'username': 'user1','password':'user1'}
        response = self.client.post(url, data, format='json')
        
        # Get authentication token
        token=response.data['token']
        
        
        # Make a create a savings account
        url = 'http://localhost:8000/savings/'
        data = {'balance':200}
        response = self.client.post(url, data, format='json',**{'HTTP_AUTHORIZATION':'Token {}'.format(token)})

        # Delete a savings account
        user=User.objects.get(username='user1')
        savings_acc=SavingsAccount.objects.all().filter(user_id=user.pk)[:1][0]
        url = 'http://localhost:8000/savings/?acc_id={}'.format(str(savings_acc.pk))
        data = {}
        response = self.client.delete(url, data, format='json',**{'HTTP_AUTHORIZATION':'Token {}'.format(token)})
        
        self.assertEqual(response.status_code,200)
        self.assertEqual(SavingsAccount.objects.all().filter(user_id=user.pk).count(),0)
        
    def test_creating_multiple_savings_accounts(self):
        """Create two savings accounts using the API and then check from the database if there are 2 accounts for the user"""
        
        #create user
        url = 'http://localhost:8000/createuser/'
        data = {'username': 'user1','password':'user1','email':'user1@mail.com'}
        response = self.client.post(url, data, format='json')
        
        #login with user
        url = 'http://localhost:8000/login/'
        data = {'username': 'user1','password':'user1'}
        response = self.client.post(url, data, format='json')
        
        # Get authentication token
        token=response.data['token']
        
        
        # Create the 1st savings account
        url = 'http://localhost:8000/savings/'
        data = {'balance':200}
        response = self.client.post(url, data, format='json',**{'HTTP_AUTHORIZATION':'Token {}'.format(token)})
        
        
        # Create the 2nd savings account
        url = 'http://localhost:8000/savings/'
        data = {'balance':500}
        response = self.client.post(url, data, format='json',**{'HTTP_AUTHORIZATION':'Token {}'.format(token)})
        
        
        # Check if there are 2 accounts created under the user
        user=User.objects.get(username='user1')
        self.assertEqual(SavingsAccount.objects.all().filter(user_id=user.pk).count(),2)
        

class SavingsAccountTransactionsTests(APITestCase):
    """This test case is testing requirement 3 adn 4"""
    
    def test_widthdraw_from_savings_account(self):
        """ 1st deposit an amount of 200, then widthdraw 50 and check if the remaining amount is 150"""
       
        #create user
        url = 'http://localhost:8000/createuser/'
        data = {'username': 'user1','password':'user1','email':'user1@mail.com'}
        response = self.client.post(url, data, format='json')
        
        #login with user
        url = 'http://localhost:8000/login/'
        data = {'username': 'user1','password':'user1'}
        response = self.client.post(url, data, format='json')
        
        # Get authentication token
        token=response.data['token']
        
        
        # Make a create a savings account with init balance of 200
        url = 'http://localhost:8000/savings/'
        data = {'balance':200}
        response = self.client.post(url, data, format='json',**{'HTTP_AUTHORIZATION':'Token {}'.format(token)})
        self.assertEqual(response.status_code,200)
        
        # Make a widthfrawal of R50
        user=User.objects.get(username='user1')
        savings_acc=SavingsAccount.objects.all().filter(user_id=user.pk)[:1][0]
        url = 'http://localhost:8000/savings/transact/?type=widthdraw'
        data = {'amount':50,'acc_id':savings_acc.pk}
        response = self.client.post(url, data, format='json',**{'HTTP_AUTHORIZATION':'Token {}'.format(token)})
        self.assertEqual(response.status_code,200)
        
        # Check if remeining balance is 150
        self.assertEqual(SavingsAccount.objects.all().filter(user_id=user.pk)[:1][0].balance,150)
    
    def test_deposit_to_savings_account(self):
        """ 1st deposit an amount of 200 initially, then deposit 50 and check if the new amount is 250"""
       
        #create user
        url = 'http://localhost:8000/createuser/'
        data = {'username': 'user1','password':'user1','email':'user1@mail.com'}
        response = self.client.post(url, data, format='json')
        
        #login with user
        url = 'http://localhost:8000/login/'
        data = {'username': 'user1','password':'user1'}
        response = self.client.post(url, data, format='json')
        
        # Get authentication token
        token=response.data['token']
        
        
        # Make a create a savings account with init balance of 200
        url = 'http://localhost:8000/savings/'
        data = {'balance':200}
        response = self.client.post(url, data, format='json',**{'HTTP_AUTHORIZATION':'Token {}'.format(token)})
        self.assertEqual(response.status_code,200)
        
        # Make a widthfrawal of R50
        user=User.objects.get(username='user1')
        savings_acc=SavingsAccount.objects.all().filter(user_id=user.pk)[:1][0]
        url = 'http://localhost:8000/savings/transact/?type=deposit'
        data = {'amount':50,'acc_id':savings_acc.pk}
        response = self.client.post(url, data, format='json',**{'HTTP_AUTHORIZATION':'Token {}'.format(token)})
        self.assertEqual(response.status_code,200)
        
        # Check if new balance is 250
        self.assertEqual(SavingsAccount.objects.all().filter(user_id=user.pk)[:1][0].balance,250)


 #CREDIT ACCOUNT
 
class CreditAccountTests(APITestCase):
    """This test case is testing requirement 2 and 6"""

    def test_create_credit_account_with_initial_balance_more_than_negatieve_20000(self):
        """ Ensure that we can create a credit account with the initial balance >= -R20000, Expected respose status =200"""
        
        #create user
        url = 'http://localhost:8000/createuser/'
        data = {'username': 'user1','password':'user1','email':'user1@mail.com'}
        response = self.client.post(url, data, format='json')
        
        #login with user
        url = 'http://localhost:8000/login/'
        data = {'username': 'user1','password':'user1'}
        response = self.client.post(url, data, format='json')
        
        # Get authentication token
        token=response.data['token']
        
        
        # Make a create a credit account
        url = 'http://localhost:8000/credit/'
        data = {'balance':0}
        response = self.client.post(url, data, format='json',**{'HTTP_AUTHORIZATION':'Token {}'.format(token)})
        self.assertEqual(response.status_code,200)
        
    def test_create_credit_account_with_initial_balance_less_than_negatieve_20000(self):
        """ Ensure that we can create a credit account width initial balance < R-20000, Expected respose status =400"""
        
        #create user
        url = 'http://localhost:8000/createuser/'
        data = {'username': 'user1','password':'user1','email':'user1@mail.com'}
        response = self.client.post(url, data, format='json')
        
        #login with user
        url = 'http://localhost:8000/login/'
        data = {'username': 'user1','password':'user1'}
        response = self.client.post(url, data, format='json')
        
        # Get authentication token
        token=response.data['token']
        
        
        # Make a create a credit account
        url = 'http://localhost:8000/credit/'
        data = {'balance':-20001}
        response = self.client.post(url, data, format='json',**{'HTTP_AUTHORIZATION':'Token {}'.format(token)})
        self.assertEqual(response.status_code,400)
        
    def test_update_credit_account_to_a_new_initial_balance(self):
        """ Update the initial amount of R200 to a new amount of R300 and check if it's updated"""
        
        #create user
        url = 'http://localhost:8000/createuser/'
        data = {'username': 'user1','password':'user1','email':'user1@mail.com'}
        response = self.client.post(url, data, format='json')
        
        #login with user
        url = 'http://localhost:8000/login/'
        data = {'username': 'user1','password':'user1'}
        response = self.client.post(url, data, format='json')
        
        # Get authentication token
        token=response.data['token']
        
        
        # Make a create a credit account
        url = 'http://localhost:8000/credit/'
        data = {'balance':200}
        response = self.client.post(url, data, format='json',**{'HTTP_AUTHORIZATION':'Token {}'.format(token)})  

        # Update a credit account
        user=User.objects.get(username='user1')
        savings_acc=CreditAccount.objects.all().filter(user_id=user.pk)[:1][0]
        url = 'http://localhost:8000/credit/?acc_id={}'.format(str(savings_acc.pk))
        data = {'balance':300}
        response = self.client.patch(url, data, format='json',**{'HTTP_AUTHORIZATION':'Token {}'.format(token)})
        
        self.assertEqual(response.status_code,200)
        self.assertEqual(CreditAccount.objects.all().filter(user_id=user.pk)[:1][0].balance,300)
        
    def test_delete_a_credit_account(self):
        """ Test for an credit account deletion event, and then if there are zero credit accounts for the user"""
        
        #create user
        url = 'http://localhost:8000/createuser/'
        data = {'username': 'user1','password':'user1','email':'user1@mail.com'}
        response = self.client.post(url, data, format='json')
        
        #login with user
        url = 'http://localhost:8000/login/'
        data = {'username': 'user1','password':'user1'}
        response = self.client.post(url, data, format='json')
        
        # Get authentication token
        token=response.data['token']
        
        
        # Make a create a credit account
        url = 'http://localhost:8000/credit/'
        data = {'balance':200}
        response = self.client.post(url, data, format='json',**{'HTTP_AUTHORIZATION':'Token {}'.format(token)})

        # Delete a credit account
        user=User.objects.get(username='user1')
        savings_acc=CreditAccount.objects.all().filter(user_id=user.pk)[:1][0]
        url = 'http://localhost:8000/credit/?acc_id={}'.format(str(savings_acc.pk))
        data = {}
        response = self.client.delete(url, data, format='json',**{'HTTP_AUTHORIZATION':'Token {}'.format(token)})
        
        # Check if you have zero credit accounts for the user 
        self.assertEqual(response.status_code,200)
        self.assertEqual(CreditAccount.objects.all().filter(user_id=user.pk).count(),0)
      
    def test_creating_multiple_credit_accounts(self):
        """Create 2 accounts for the user and then check with the database if you have two accounts under the user"""
        
        #create user
        url = 'http://localhost:8000/createuser/'
        data = {'username': 'user1','password':'user1','email':'user1@mail.com'}
        response = self.client.post(url, data, format='json')
        
        #login with user
        url = 'http://localhost:8000/login/'
        data = {'username': 'user1','password':'user1'}
        response = self.client.post(url, data, format='json')
        
        # Get authentication token
        token=response.data['token']
        
        
        # Create the 1st credit account
        url = 'http://localhost:8000/credit/'
        data = {'balance':200}
        response = self.client.post(url, data, format='json',**{'HTTP_AUTHORIZATION':'Token {}'.format(token)})
        
        
        # Create the 2nd credit account
        url = 'http://localhost:8000/credit/'
        data = {'balance':500}
        response = self.client.post(url, data, format='json',**{'HTTP_AUTHORIZATION':'Token {}'.format(token)})
        
        
        # Check if there are 2 accounts created under the user
        user=User.objects.get(username='user1')
        self.assertEqual(CreditAccount.objects.all().filter(user_id=user.pk).count(),2)


class CreditAccountTransactionsTests(APITestCase):
    """This test case is testing requirement 3 and 4"""
    
    def test_widthdraw_from_credit_account(self):
        """ 1st deposit an amount of 200, then widthdraw 50 and check if the remaining amount is 150"""
       
        #create user
        url = 'http://localhost:8000/createuser/'
        data = {'username': 'user1','password':'user1','email':'user1@mail.com'}
        response = self.client.post(url, data, format='json')
        
        #login with user
        url = 'http://localhost:8000/login/'
        data = {'username': 'user1','password':'user1'}
        response = self.client.post(url, data, format='json')
        
        # Get authentication token
        token=response.data['token']
        
        
        # Make a create a credit account with init balance of 200
        url = 'http://localhost:8000/credit/'
        data = {'balance':200}
        response = self.client.post(url, data, format='json',**{'HTTP_AUTHORIZATION':'Token {}'.format(token)})
        self.assertEqual(response.status_code,200)
        
        # Make a widthfrawal of R50
        user=User.objects.get(username='user1')
        credit_acc=CreditAccount.objects.all().filter(user_id=user.pk)[:1][0]
        url = 'http://localhost:8000/credit/transact/?type=widthdraw'
        data = {'amount':50,'acc_id':credit_acc.pk}
        response = self.client.post(url, data, format='json',**{'HTTP_AUTHORIZATION':'Token {}'.format(token)})
        self.assertEqual(response.status_code,200)
        
        # Check if remeining balance is 150
        self.assertEqual(CreditAccount.objects.all().filter(user_id=user.pk)[:1][0].balance,150)
    
    def test_deposit_to_credit_account(self):
    
        """1st deposit an amount of 200 initially, then deposit 50 and check if the new amount is 250"""
       
        #create user
        url = 'http://localhost:8000/createuser/'
        data = {'username': 'user1','password':'user1','email':'user1@mail.com'}
        response = self.client.post(url, data, format='json')
        
        #login with user
        url = 'http://localhost:8000/login/'
        data = {'username': 'user1','password':'user1'}
        response = self.client.post(url, data, format='json')
        
        # Get authentication token
        token=response.data['token']
        
        
        # Make a create a credit account with init balance of 200
        url = 'http://localhost:8000/credit/'
        data = {'balance':200}
        response = self.client.post(url, data, format='json',**{'HTTP_AUTHORIZATION':'Token {}'.format(token)})
        self.assertEqual(response.status_code,200)
        
        # Make a widthfrawal of R50
        user=User.objects.get(username='user1')
        credit_acc=CreditAccount.objects.all().filter(user_id=user.pk)[:1][0]
        url = 'http://localhost:8000/credit/transact/?type=deposit'
        data = {'amount':50,'acc_id':credit_acc.pk}
        response = self.client.post(url, data, format='json',**{'HTTP_AUTHORIZATION':'Token {}'.format(token)})
        self.assertEqual(response.status_code,200)
        
        # Check if new balance is 250
        self.assertEqual(CreditAccount.objects.all().filter(user_id=user.pk)[:1][0].balance,250)


