from django.contrib import admin
from api.models import (
    Bank, BankAccount, Beneficiary, Customer, CustomerCode,
    Transaction, OtherAddress, OtherEmail, OtherPhoneNumber
)

all_models = (
    Bank, 
    BankAccount, 
    Beneficiary, 
    Customer, 
    CustomerCode,
    Transaction, 
    OtherAddress, 
    OtherEmail, 
    OtherPhoneNumber
)

# Register your models here.
for model in all_models:
    admin.site.register(model)
