from rest_framework import viewsets, generics
from django.contrib.auth.models import User

from api.models import (
    Bank, BankAccount, Beneficiary, Customer, CustomerCode,
    Transaction, OtherAddress, OtherEmail, OtherPhoneNumber
)

from api.serializers import (
    BankSerializer, BankAccountSerializer, BeneficiarySerializer, 
    CustomerSerializer, CustomerCodeSerializer, TransactionSerializer, 
    OtherAddressSerializer, OtherEmailSerializer, OtherPhoneNumberSerializer, UserSerializer
)


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by()
    serializer_class = UserSerializer


class CustomerView(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('-timestamp')
    serializer_class = CustomerSerializer

