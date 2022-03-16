"""Django views for financials project, app"""

import csv
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from rest_framework import status


from django.contrib.auth import authenticate
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from rest_framework import viewsets
from rest_framework.response import Response

from django.contrib.auth.models import User
from .models import CreditAccount,SavingsAccount,Transaction
from .serializers import CreateUserSerializer,CreditAccountsSerializer,SavingsAccountsSerializer


# View sets
class UserViewSet(viewsets.ModelViewSet):
    """This is a ModelViewSet  for url /createuser/
    
    This class uses the CreateUserSerializer to 
    automatically handle POST requests for creating accounts.
    
    Attributes
    ----------
    queryset : QuerySet
        This holds the view model contenxt
    serializer_class : serializers.HyperlinkedModelSerializer
        This attributes sets the serializer
    """
    
    queryset=User.objects.all()
    serializer_class=CreateUserSerializer

class LoginAndGetAuthToken(ObtainAuthToken):

    """This is an ObtainAuthToken type view for url /login/
    
    This Class handles defines the methods to handle post requests for logging in.
    
    Methods
    ----------
    post(self, request, *args, **kwargs)
        This method captures the user's login attempt request
        and then returns a Response obj with message "successful login" and a 
        login token if login was successful or returns failed if not.
    """

    def post(self, request, *args, **kwargs):
        """ Handles POST requests for a login attempt
        
        This methids returns A Responmse object of type JSON
        with the token,user_id,email and message if successfully logged in
        otherwise, it reponds with a login failed message.
        
        Parameters
        ----------
        request : Request
            The http request received
        *args : <dict>
            This captures the arguments passed with the request
        **kwargs : <dict>
            This captures the keyword arguments passed into the request
        """
        
        # Validate,authenticate
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        # Authenticate the supplied details
        user= authenticate(username=serializer.validated_data['username'],password=serializer.validated_data['password'])
        
        # Respond to user
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'message': 'Use this token in further transactions.'
            })           
        else:
            return Response({'message':'Couldn\'t login,please check your details'}, status=status.HTTP_404_NOT_FOUND)
            

# Account creation,update and delete
class SavingsAPIView(APIView):
    """This is an APIView type view for url /savings/
    
    This Class handles defines the post,patch and delete
    methods for savings accounts
    
    Attributes
    ----------
    queryset : QuerySet
        This holds the view model contenxt
    serializer_class : serializers.HyperlinkedModelSerializer
        This attributes sets the serializer
    permission_classes :  Set
        This attribute sets the permissions applied to this class
        the main function is to only allow authenticated users to access it's methods.
    
    Methods
    ----------
    post(self, request, *args, **kwargs)
        This method handles POST requests to /savings/ for creating an account
    patch(self, request, *args, **kwargs)
        This method handles the PATCH request to /savings/ for updating an account.
    delete(self, request, *args, **kwargs)
        This method handles the DELETE request to /savings/ for deleting an account.
    """
    
    queryset=SavingsAccount.objects.all()
    permission_classes = (IsAuthenticated,) 
    serializer_class=SavingsAccountsSerializer
    
    
    def post(self, request, *args, **kwargs):
        """ Handles POST requests for a savings account creation attempt request on url /savings/
        
        This method returns Response Objects of type JSON as resposes
        for validation and account creation success or failure
        
        Parameters
        ----------
        request : Request
            The http request received
        *args : <dict>
            This captures the arguments passed with the request
        **kwargs : <dict>
            This captures the keyword arguments passed into the request
        """
        
        # Validate,authenticate
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        # Get the user
        user=request.user
        
        # Respond to user
        savings=SavingsAccount(user_id=user.pk,balance=serializer.validated_data['balance'])
        savings.save()
        
        return Response({
            'message': 'Savings account successfully created for {}'.format(user.username)
        })           

    def patch(self, request, *args, **kwargs):
        """ Handles PATCH requests for a savings account on url /savings/?acc_id=<account_id>
        
        This method will attempt to validate the passed information 1st and then
        if succcessful, the URL parameter "acc_id" passed in the URL is received and then 
        used to get the account in question. If the account doesn't exist, the method will 
        return failed Response otherwise the the attempt to patch is done.
        
        Parameters
        ----------
        request : Request
            The http request received
        *args : <dict>
            This captures the arguments passed with the request
        **kwargs : <dict>
            This captures the keyword arguments passed into the request
        """
        
        # Validate,authenticate
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        
        # Get the user
        user=request.user

        # Get url params
        acc_id=request.GET.get('acc_id')

        # Implement patch
        savings_acc=SavingsAccount.objects.all().filter(user_id=user.pk).filter(pk=acc_id)

        if savings_acc:
            
            try:
                savings_acc=savings_acc[0]
                savings_acc.balance=float(serializer.validated_data['balance'])
                savings_acc.save()
            except Exception:
                return Response({'message':'Invalid update value passed'}, status=status.HTTP_404_NOT_FOUND)

            return Response({'message':'Savings account updated'})

        else:
            return Response({'message':'Savings account not found'}, status=status.HTTP_404_NOT_FOUND)         

    def delete(self, request, *args, **kwargs):
        """ Handles DELETE requests for a savings account on url /savings/?acc_id=<account_id>
        
        This method will attempt to validate the passed information 1st and then
        if succcessful, the URL parameter "acc_id" passed in the URL is received and then 
        used to get the account in question. If the account doesn't exist, the method will 
        return failed Response otherwise the the attempt to delete operation is implemented.
        When done, a success message is returned otherwise a fail message is returned.
        
        Parameters
        ----------
        request : Request
            The http request received
        *args : <dict>
            This captures the arguments passed with the request
        **kwargs : <dict>
            This captures the keyword arguments passed into the request
        """
        
        # Get url params
        acc_id=request.GET.get('acc_id')
        
        # Get the user
        user=request.user
        
        # Implement delete
        savings_acc=SavingsAccount.objects.all().filter(user_id=user.pk).filter(pk=acc_id)

        if savings_acc:

            savings_acc=savings_acc[0]
            savings_acc.delete()
            return Response({'message':'Savings account deleted'})

        else:

            return Response({'message':'Savings account doesn\'t exist'}, status=status.HTTP_404_NOT_FOUND)

class CreditAPIView(APIView):
    """This is an APIView type view for url /credit/
    
    This Class handles defines the post,patch and delete
    methods for credit accounts
    
    Attributes
    ----------
    queryset : QuerySet
        This holds the view model contenxt
    serializer_class : serializers.HyperlinkedModelSerializer
        This attributes sets the serializer
    permission_classes :  Set
        This attribute sets the permissions applied to this class
        the main function is to only allow authenticated users to access it's methods.
    
    Methods
    ----------
    post(self, request, *args, **kwargs)
        This method handles POST requests to /credit/ for creating an account.
    patch(self, request, *args, **kwargs)
        This method handles the PATCH request to /credit/ for updating an account.
    delete(self, request, *args, **kwargs)
        This method handles the DELETE request to /credit/ for deleting an account.
    """
    
    queryset=CreditAccount.objects.all()
    permission_classes = (IsAuthenticated,) 
    serializer_class=CreditAccountsSerializer

    def post(self, request, *args, **kwargs):
        """ Handles POST requests for a credit account creation attempt request on url /credit/
        
        This method returns Response Objects of type JSON as resposes
        for validation and account creation success or failure
        
        Parameters
        ----------
        request : Request
            The http request received
        *args : <dict>
            This captures the arguments passed with the request
        **kwargs : <dict>
            This captures the keyword arguments passed into the request
        """
        
        # Validate,authenticate
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        # Get the user
        user=request.user
        
        # Respond to user
        credit=CreditAccount(user_id=user.pk,balance=serializer.validated_data['balance'])
        credit.save()
        
        return Response({
            'message': 'Credit account successfully created for {}'.format(user.username)
        })           

    def patch(self, request, *args, **kwargs):
        """ Handles PATCH requests for a credit account on url /credit/?acc_id=<account_id>
        
        This method will attempt to validate the passed information 1st and then
        if succcessful, the URL parameter "acc_id" passed in the URL is received and then 
        used to get the account in question. If the account doesn't exist, the method will 
        return failed Response otherwise the the attempt to patch is done.
        
        Parameters
        ----------
        request : Request
            The http request received
        *args : <dict>
            This captures the arguments passed with the request
        **kwargs : <dict>
            This captures the keyword arguments passed into the request
        """
        
        # Validate,authenticate
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        
        # Get the user
        user=request.user

        # Get url params
        acc_id=request.GET.get('acc_id')

        # Implement patch
        credit_acc=CreditAccount.objects.all().filter(user_id=user.pk).filter(pk=acc_id)

        if credit_acc:
            
            try:
                credit_acc=credit_acc[0]
                credit_acc.balance=float(serializer.validated_data['balance'])
                credit_acc.save()
            except Exception:
                return Response({'message':'Invalid update value passed'}, status=status.HTTP_404_NOT_FOUND)

            return Response({'message':'Credit account updated'})

        else:
            return Response({'message':'Credit account not found'}, status=status.HTTP_404_NOT_FOUND)         

    def delete(self, request, *args, **kwargs):
        """ Handles DELETE requests for a credit account on url /credit/?acc_id=<account_id>
        
        This method will attempt to validate the passed information 1st and then
        if succcessful, the URL parameter "acc_id" passed in the URL is received and then 
        used to get the account in question. If the account doesn't exist, the method will 
        return failed Response otherwise the the attempt to delete operation is implemented.
        When done, a success message is returned otherwise a fail message is returned.
        
        Parameters
        ----------
        request : Request
            The http request received
        *args : <dict>
            This captures the arguments passed with the request
        **kwargs : <dict>
            This captures the keyword arguments passed into the request
        """
        
        # Get url params
        acc_id=request.GET.get('acc_id')
        
        # Get the user
        user=request.user
        
        # Implement delete
        credit_acc=CreditAccount.objects.all().filter(user_id=user.pk).filter(pk=acc_id)

        if credit_acc:

            credit_acc=credit_acc[0]
            credit_acc.delete()
            return Response({'message':'Credit account deleted'})

        else:

            return Response({'message':'Credit account doesn\'t exist'}, status=status.HTTP_404_NOT_FOUND)



# Transactions
class SavingsTransactAPIView(APIView):
    """This is an APIView type view for url /savings/transact/
    
    This Class handles defines the post
    method for savings account transactions
    
    Attributes
    ----------
    queryset : QuerySet
        This holds the view model context
    permission_classes :  Set
        This attribute sets the permissions applied to this class
        the main function is to only allow authenticated users to access it's methods.
    
    Methods
    ----------
    post(self, request, *args, **kwargs)
        This method handles POST requests to /savings/ transacting.
    """
    
    queryset=SavingsAccount.objects.all()
    permission_classes = (IsAuthenticated,) 

    def post(self, request, *args, **kwargs):
        """ Handles POST requests for a savings account transactions for url /savings/transact/?type=<widthdraw or deposit>
        
        This methods implements the widthdrawal and deposit of funds into
        an account (specified by "acc_id" in body) , the <type> of transaction 
        is passed in as a URL parameter using the key word "type". This will reponds
        width an HTTPResponse JSON object containing the transaction's success or failure.
        
        Parameters
        ----------
        request : Request
            The http request received
        *args : <dict>
            This captures the arguments passed with the request
        **kwargs : <dict>
            This captures the keyword arguments passed into the request
        """
        
        #get transaction type from url parameters
        transaction_type=request.GET.get('type')
        data=request.data

        #Get the user
        user=request.user

        #get account
        savings_acc=SavingsAccount.objects.all().filter(user_id=user.pk).filter(pk=data['acc_id'])

        if savings_acc:

            savings_acc=savings_acc[0]
            initial_amount=savings_acc.balance
            
            # Expression based on transaction type
            if transaction_type == 'widthdraw':
                savings_acc.balance=savings_acc.balance-float(data['amount'])
            elif transaction_type == 'deposit':
                savings_acc.balance=savings_acc.balance+float(data['amount'])
            else:
                return Response({'message':'Wrong transaction type'}, status=status.HTTP_404_NOT_FOUND)

            # Implement transaction
            if savings_acc.balance>=50:

                # Save transaction in Transaction model
                transaction=Transaction(user_id=user.pk,account_type='SAVINGS',account_id=data['acc_id'],transaction_type=transaction_type,amount=data['amount'],balance=savings_acc.balance)
                transaction.save()

                # Commit new balance to database
                savings_acc.save()
                return Response({'message':'{} successful'.format(transaction_type.capitalize()),'Balance':savings_acc.balance}) 
            else:
                return Response({'message':'You can\'t have an amount < R50, try a smaller amount','Balance':initial_amount}, status=status.HTTP_404_NOT_FOUND)
    
        else:

            return Response({'message':'Wrong savings account_id specified '}, status=status.HTTP_404_NOT_FOUND) 
  
class CreditTransactAPIView(APIView):
    """This is an APIView type view for url /credits/transact/
    
    This Class handles defines the post
    method for credit account transactions
    
    Attributes
    ----------
    queryset : QuerySet
        This holds the view model context
    permission_classes :  Set
        This attribute sets the permissions applied to this class
        the main function is to only allow authenticated users to access it's methods.
    
    Methods
    ----------
    post(self, request, *args, **kwargs)
        This method handles POST requests to /credit/ transacting.
    """
    
    queryset=CreditAccount.objects.all()
    permission_classes = (IsAuthenticated,) 


    def post(self, request, *args, **kwargs):
        """ Handles POST requests for a credit account transactions for url /credit/transact/?type=<widthdraw or deposit>
        
        This methods implements the widthdrawal and deposit of funds into
        an account (specified by "acc_id" in body) , the <type> of transaction 
        is passed in as a URL parameter using the key word "type". This will reponds
        width an HTTPResponse JSON object containing the transaction's success or failure.
        
        Parameters
        ----------
        request : Request
            The http request received
        *args : <dict>
            This captures the arguments passed with the request
        **kwargs : <dict>
            This captures the keyword arguments passed into the request
        """
        
        #get transaction type from url parameters
        transaction_type=request.GET.get('type')
        data=request.data

        #Get the user
        user=request.user

        #get account
        credit_acc=CreditAccount.objects.all().filter(user_id=user.pk).filter(pk=data['acc_id'])

        if credit_acc:

            credit_acc=credit_acc[0]
            initial_amount=credit_acc.balance
            
            # Expression based on transaction type
            if transaction_type == 'widthdraw':
                credit_acc.balance=credit_acc.balance-float(data['amount'])
            elif transaction_type == 'deposit':
                credit_acc.balance=credit_acc.balance+float(data['amount'])
            else:
                return Response({'message':'Wrong transaction type'}, status=status.HTTP_404_NOT_FOUND)

            # Implement transaction
            if credit_acc.balance>=-20000:

                # Save transaction in Transaction model
                transaction=Transaction(user_id=user.pk,account_type='CREDIT',account_id=data['acc_id'],transaction_type=transaction_type,amount=data['amount'],balance=credit_acc.balance)
                transaction.save()
                
                # Commit new balance to database            
                credit_acc.save()
                return Response({'message':'{} successful'.format(transaction_type.capitalize()),'Balance':credit_acc.balance}) 
            else:
                return Response({'message':'You can\'t have an amount <-R20 000, try a smaller amount','Balance':initial_amount}, status=status.HTTP_404_NOT_FOUND)
    
        else:

            return Response({'message':'Wrong credit account_id specified'}) 

class BalancesAPIView(APIView):
    """This is an APIView type view for url /balances/
    
    This Class handles defines the GET
    method for an authenticated user
    
    Attributes
    ----------
    queryset : QuerySet
        This holds the view model context
    permission_classes :  Set
        This attribute sets the permissions applied to this class
        the main function is to only allow authenticated users to access it's methods.
    
    Methods
    ----------
    get(self, request, *args, **kwargs)
        This method handles GET requests to get /balances/.
    """

    queryset=CreditAccount.objects.all()
    permission_classes = (IsAuthenticated,) 


    def get(self, request, *args, **kwargs):
        """ Handles GET requests on url /balances/
        
        This methods simple compiles the list of accounts and their relating balances,
        and the last 10 transactions they've made from any of the aacounts.
        The result is an HTTPResponse containnig JSON data with the infromation as described.
        The infromation received is of the logged in user. (Thwe autherntication token provided).
        
        Parameters
        ----------
        request : Request
            The http request received
        *args : <dict>
            This captures the arguments passed with the request
        **kwargs : <dict>
            This captures the keyword arguments passed into the request
        """

        #Get the user
        user=request.user

        #Make request
        data={"accounts":[],"last_10_transactions":[]}

        credit_accounts=CreditAccount.objects.all().filter(user_id=user.pk)
        savings_accounts=SavingsAccount.objects.all().filter(user_id=user.pk)
        transactions=Transaction.objects.all().filter(user_id=user.pk)

        if credit_accounts:
            for account in credit_accounts:
                data['accounts'].append(str(account))

        if savings_accounts:
            for account in savings_accounts:
                data['accounts'].append(str(account))

        if transactions:
            transactions=transactions[:10]
            for transaction in transactions:
                data['last_10_transactions'].append(str(transaction ))

        
        return Response(data) 

class CsvView(APIView):
    """This is an APIView type view for url /csv/
    
    This Class handles defines the GET
    method for downloading a CSV file
    
    Attributes
    ----------
    queryset : QuerySet
        This holds the view model context
    
    Methods
    ----------
    get(self, request, *args, **kwargs)
        This method handles GET requests to get /csv/.
    """

    queryset=CreditAccount.objects.all()

    def get(self, request, *args, **kwargs):
        """ Handles GET requests on url /csv/
        
        This methods simply compiles a list of accounts, the relating balances and the user
        or owner of the account into a cvs file and then returns it. To access this method a user doesn't need to
        be authenticated (this requirement wasn't specified).
        
        Parameters
        ----------
        request : Request
            The http request received
        *args : <dict>
            This captures the arguments passed with the request
        **kwargs : <dict>
            This captures the keyword arguments passed into the request
        """
        
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="bank_report.csv"'},
        )

        # Get all savings and credit accounts
        credit_accounts=CreditAccount.objects.all()
        savings_accounts=SavingsAccount.objects.all()

        # Make CSV
        writer = csv.writer(response)
        writer.writerow(['Account', 'Balance', 'User'])

        for account in credit_accounts:
            csv_data=account.print_csv()
            writer.writerow([csv_data['Account'], csv_data['Balance'], csv_data['User']])

        for account in savings_accounts:
            csv_data=account.print_csv()
            writer.writerow([csv_data['Account'], csv_data['Balance'], csv_data['User']])

        return response