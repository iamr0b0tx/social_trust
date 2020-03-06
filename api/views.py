import json, requests

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
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

from nibss.credentials import Credentials
from nibss.bvn import Bvn

YOUR_ORGANIZATION_CODE = "11111"
YOUR_SANDBOX_KEY = "f089e1189acb8419fcff28bc6d2177a0"

header = {
    "base_url": "",
    "Organizationcode": YOUR_ORGANIZATION_CODE,
    "sandbox-key": YOUR_SANDBOX_KEY,
    "content-type": "application/json",
    "accept": "application/json",
    "username": YOUR_ORGANIZATION_CODE,
    "password": "",
}

reset = Credentials(header).reset()

YOUR_PASSWORD = header["password"] = reset['password']
YOUR_AES_KEY = reset['aes_key']
YOUR_IV_KEY = reset['ivkey']


@require_http_methods(['GET'])
def verify_bvn(request, bank_verification_number=None):
    # initial data
    phone_number = email = False

    if bank_verification_number is None or len(bank_verification_number) != 11:
        return HttpResponse(
            json.dumps(
                {"phone_number": phone_number, "email": email}
            )
        )

    def hide_phone_number(value, start, end, placeholder='*'):
        if not value:
            return False

        value = list(value)
        value[start:end] = placeholder * (end - start)
        return ''.join(value)
    
    def hide_email(value, count, placeholder='*'):
        if not value:
            return False

        value = value.split('@')
        value[0] = value[0][:count] + (placeholder * (len(value[0]) - count))
        return '@'.join(value)

    
    try:
        single = Bvn(header).get_single({
            "body": {"BVN": bank_verification_number},
            "Aes_key": YOUR_AES_KEY,
            "Iv_key": YOUR_IV_KEY
        })

        if type(single) != dict:
            raise Exception

        single = single['data']

        phone_number = single.get("PhoneNumber", single.get("PhoneNumber1", False))
        phone_number = hide_phone_number(phone_number, -8, -4)
        
        email = single.get("Email", False)
        email = hide_email(email, 3)

    except Exception as e:
        print(e)
        
    return HttpResponse(
        json.dumps(
            {"phone_number": phone_number, "email": email}
        )
    )

@require_http_methods(['POST', 'GET'])
def signup_with_bvn(request, phone_number=None):
    
    # initial data
    status = False
    
    BAD_RESPONSE = HttpResponse(
        json.dumps(
            {"status": status}
        )
    )


    if phone_number is None or len(phone_number) != 14:
        return BAD_RESPONSE

    code = 1234
    url = "https://sandboxapi.fsi.ng/atlabs/messaging"
    header = {"Sandbox-Key":YOUR_SANDBOX_KEY, "Content-Type":"application/json"}
    body = {"to": "+2348037428664", "from": "FSI", "message": f"Your bank Verification Code is {code}"}
    
    response = json.loads(requests.post(
        url=url, headers=header, data=json.dumps(body)).text
    ).get("SMSMessageData", False)

    if response:
        response = response.get("Recipients", False)

        if response:
            if response[0].get("statusCode", False) == 101:
                status = True
                return HttpResponse(
                    json.dumps(
                        {"status": status}
                    )
                )

    return BAD_RESPONSE

@require_http_methods(['POST', 'GET'])
def verify_phone_number(request, phone_number=None):
    
    # initial data
    status = False
    
    BAD_RESPONSE = HttpResponse(
        json.dumps(
            {"status": status}
        )
    )


    if phone_number is None or len(phone_number) != 14:
        return BAD_RESPONSE

    code = 1234
    url = "https://sandboxapi.fsi.ng/atlabs/messaging"
    header = {"Sandbox-Key":YOUR_SANDBOX_KEY, "Content-Type":"application/json"}
    body = {"to": "+2348037428664", "from": "FSI", "message": f"Your bank Verification Code is {code}"}
    
    response = json.loads(requests.post(
        url=url, headers=header, data=json.dumps(body)).text
    ).get("SMSMessageData", False)

    if response:
        response = response.get("Recipients", False)

        if response:
            if response[0].get("statusCode", False) == 101:
                status = True
                return HttpResponse(
                    json.dumps(
                        {"status": status}
                    )
                )

    return BAD_RESPONSE

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by()
    serializer_class = UserSerializer


class CustomerView(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('-timestamp')
    serializer_class = CustomerSerializer

