from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'user', views.UserView, 'user')
router.register(r'customer', views.CustomerView, 'organization')
# router.register(r'verify_bvn', views.verify_bvn, 'Verify BVN')

urlpatterns = [
    path('', include(router.urls)),
    path(r'verify_bvn/<str:bank_verification_number>', views.verify_bvn),
    path(r'verify_phone_number/<str:phone_number>', views.verify_phone_number),
]
