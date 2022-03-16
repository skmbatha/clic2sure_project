"""Django urls for financials, app."""

from . import views
from django.urls import path,include
from rest_framework import routers

app_name = 'app' 

#initialize the DRF view sets
createuser= routers.DefaultRouter()
createuser.register(r'createuser',views.UserViewSet)

urlpatterns = [
    path('',include(createuser.urls)), 
    path('login/',views.LoginAndGetAuthToken.as_view(),name='login-handler'),
    path('balances/',views.BalancesAPIView.as_view(), name='user-balances'),
    path('csv/',views.CsvView.as_view(), name='user-balances'),
    
    path('savings/',views.SavingsAPIView.as_view()),
    path('credit/',views.CreditAPIView.as_view()),

    path('savings/transact/',views.SavingsTransactAPIView.as_view(), name='savings-transact'),
    path('credit/transact/',views.CreditTransactAPIView.as_view(), name='credit-transact'),

]
