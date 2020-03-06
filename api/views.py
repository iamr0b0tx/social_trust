# from twitterscraper import query_tweets
from ibm_watson.natural_language_understanding_v1 import (
    EmotionOptions, SentimentOptions, Features
    #CategoriesOptions, ConceptsOptions, EntitiesOptions, KeywordsOptions,
)
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
import json
import json, requests

from random import randint

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

CODES = [1234, 7356, 9273, 9387]
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


apikey = "JOZPP1z2nOqpnnkHd0e-wkqvXKqlFV3BzMu_B3nyLIvA"
url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/ee434d2a-f5ac-486c-a42d-a3feb5ce37cf"

authenticator = IAMAuthenticator(apikey)
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2019-07-12',
    authenticator=authenticator
)

natural_language_understanding.set_service_url(url)
DEFAULT = {
    "score": 0.0,
    "label": "neutral",
    "sadness": 0.0,
    "joy": 0.0,
    "fear": 0.0,
    "disgust": 0.0,
    "anger": 0.0
}

@require_http_methods(['GET'])
def get_score(request, twitter_handle=None):
    # initial data
    identity_score = False
    financial_footprint = False
    social_score = False

    BAD_RESPONSE = HttpResponse(
        json.dumps(DEFAULT.update(
            {"identity_score": identity_score, "financial_footprint": financial_footprint, 'social_score':social_score}
        ))
    )
    
    if twitter_handle is None or not twitter_handle or not twitter_handle.isalnum():
        return BAD_RESPONSE
    
    # tweet = list(query_tweets(f"{twitter_handle} -user", 5))
    text = "I ordered just once from TerribleCo, they screwed up, never used the app again."

    try:
        result = natural_language_understanding.analyze(
            text=text,
            features=Features(
                # categories=CategoriesOptions(limit=3),
                # concepts=ConceptsOptions(limit=3),
                # entities=EntitiesOptions(sentiment=True, limit=1),
                # keywords=KeywordsOptions(sentiment=True,emotion=True,limit=2),
                sentiment=SentimentOptions(),
                emotion=EmotionOptions()
            )
        ).get_result()

        
        social_score = dict(result["sentiment"]["document"])
        social_score.update(result["emotion"]["document"]["emotion"])

        return HttpResponse(
            json.dumps(
                {"identity_score": 1/len(twitter_handle), "financial_footprint": financial_footprint, 'social_score':social_score},
                indent=2
            )
        )

    except Exception as e:
        print(e)
    
    return BAD_RESPONSE

@require_http_methods(['GET'])
def verify_bvn(request, bank_verification_number=None):
    # initial data
    phone_number = email = False

    if bank_verification_number is None or len(bank_verification_number) != 11 or not bank_verification_number.isdigit():
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
def signup_with_bvn(request, bank_verification_number=None, phone_number=None, code=None, pin=None):
    
    # initial data
    status = False
    
    BAD_RESPONSE = HttpResponse(
        json.dumps(
            {"status": status}
        )
    )

    if (phone_number is None or len(phone_number) != 14) or not phone_number[1:].isdigit():
        return BAD_RESPONSE

    if (bank_verification_number is None or len(bank_verification_number) != 11 or not bank_verification_number.isdigit()):
        return BAD_RESPONSE

    if code == None or not code.isdigit() or len(code) != 4:
        return BAD_RESPONSE

    if pin == None or not pin.isdigit() or len(pin) != 6:
        return BAD_RESPONSE

    code = code in CODES
    single = Bvn(header).get_single({
        "body": {"BVN": bank_verification_number},
        "Aes_key": YOUR_AES_KEY,
        "Iv_key": YOUR_IV_KEY
    })['data']

    try:
        url = "http://127.0.0.1:8000/api/customer/"
        head = {"Content-Type":"application/json"}
        body = {
            "firstname": single['FirstName'],
            "lastname":	single['LastName'],
            "middlename":	single['MiddleName'],
            "email": single['Email'],
            "pin": pin,
            "phonenumber": single['PhoneNumber1'],
            "image": ""
        }
        
        return HttpResponse(requests.post(url=url, headers=head, data=json.dumps(body)).text)
    except Exception as e:
        print(e)

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

    code = CODES[randint(0, len(CODES)-1)]

    url = "https://sandboxapi.fsi.ng/atlabs/messaging"
    header = {"Sandbox-Key":YOUR_SANDBOX_KEY, "Content-Type":"application/json"}
    body = {"to": phone_number, "from": "FSI", "message": f"Your bank Verification Code is {code}"}
    
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


class BankView(viewsets.ModelViewSet):
    queryset = Bank.objects.all().order_by()
    serializer_class = BankSerializer


class BankAccountView(viewsets.ModelViewSet):
    queryset = BankAccount.objects.all().order_by()
    serializer_class = BankAccountSerializer


class BeneficiaryView(viewsets.ModelViewSet):
    queryset = Beneficiary.objects.all().order_by()
    serializer_class = BeneficiarySerializer


class CustomerView(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('-timestamp')
    serializer_class = CustomerSerializer


class CustomerCodeView(viewsets.ModelViewSet):
    queryset = CustomerCode.objects.all().order_by('-timestamp')
    serializer_class = CustomerCodeSerializer


class TransactionView(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by('-timestamp')
    serializer_class = TransactionSerializer


class OtherAddressView(viewsets.ModelViewSet):
    queryset = OtherAddress.objects.all().order_by('-timestamp')
    serializer_class = OtherAddressSerializer


class OtherEmailView(viewsets.ModelViewSet):
    queryset = OtherEmail.objects.all().order_by('-timestamp')
    serializer_class = OtherEmailSerializer


class OtherPhoneNumberView(viewsets.ModelViewSet):
    queryset = OtherPhoneNumber.objects.all().order_by('-timestamp')
    serializer_class = OtherPhoneNumberSerializer
