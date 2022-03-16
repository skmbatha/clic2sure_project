"""Django serializers for financials project."""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CreditAccount,SavingsAccount
from rest_framework.authtoken.models import Token


class CreateUserSerializer(serializers.HyperlinkedModelSerializer):

    """serializers.HyperlinkedModelSerializer 
    
    This class defined the Meta data used to map the 
    create serializaer class to the model User.
    
    Classes
    -------
    
    Meta:
        This class defines the metadata
        
    Methods
    -------
    create(self, validated_data):
        This function intercepts the user creation and implements it manually.
        This is because the user's password needs to be hashed. 
        A second reason is that a Token needs to be created for each user on 
        an account creation
    """
    
    class Meta:
        """This is a metadata class 
    
        ...
        
        Atributes
        ---------
        model:SavingsAccount
            This parameter holds the context model to be used
        fields:Set
            This field defined the model columns which should be linked/validated
        """
        model = User
        fields = ('pk','username','email','password')

    def create(self, validated_data):
        """ This function is called finally to create a database entry in User table
        
        ...
        
        Parameters
        ----------
        validated_data : <dict>
            This value is aumatically passed in when the data matching the model
            is validated.
        """
        #Create the user in the database
        user=User()
        user.username=validated_data['username']
        user.email=validated_data['email']
        user.set_password(validated_data['password'])
        user.save()
        
        #Create a token for the user
        Token.objects.get_or_create(user=user)
        
        return user
        
class CreditAccountsSerializer(serializers.HyperlinkedModelSerializer):
    """serializers.HyperlinkedModelSerializer 
    
    This class defined the Meta data used to map the 
    create serializaer class to the model User.
    
    Classes
    -------
    
    Meta:
        This class defines the metadata
    """
    
    class Meta:
        """This is a metadata class 
    
        ...
        
        Atributes
        ---------
        model:SavingsAccount
            This parameter holds the context model to be used
        fields:Set
            This field defined the model columns which should be linked/validated
        """
        
        model = CreditAccount
        fields = ('pk','balance',)

class SavingsAccountsSerializer(serializers.HyperlinkedModelSerializer):
    """serializers.HyperlinkedModelSerializer 
    
    This class defined the Meta data used to map the 
    create serializaer class to the model User.
    
    Classes
    -------
    
    Meta:
        This class defines the metadata
    """
    
    class Meta:
        """This is a metadata class 
    
        ...
        
        Atributes
        ---------
        model:SavingsAccount
            This parameter holds the context model to be used
        fields:Set
            This field defined the model columns which should be linked/validated
        """
    
        model = SavingsAccount
        fields = ('pk','balance',)
             
     

