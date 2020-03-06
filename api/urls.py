from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'user', views.UserView, 'user')
router.register(r'bank', views.BankView, 'Bank')
router.register(r'bank_account', views.BankAccountView, 'Bank Account')
router.register(r'beneficiary', views.BeneficiaryView, 'Beneficiary')
router.register(r'customer', views.CustomerView, 'organization')
router.register(r'customer_code', views.CustomerCodeView, 'Customer Code')
router.register(r'transaction', views.TransactionView, 'Transaction')
router.register(r'other_address', views.OtherAddressView, 'Other Address')
router.register(r'other_email', views.OtherEmailView, 'Other Email')
router.register(r'other_phone_number', views.OtherPhoneNumberView, 'Other PhoneNumber')


urlpatterns = [
    path('', include(router.urls)),
    path(r'get_score/<str:twitter_handle>', views.get_score),
    path(r'verify_bvn/<str:bank_verification_number>', views.verify_bvn),
    path(r'verify_phone_number/<str:phone_number>', views.verify_phone_number),
    path(r'signup_with_bvn/<str:bank_verification_number>/<str:phone_number>/<str:code>/<str:pin>', views.signup_with_bvn),
    
]
