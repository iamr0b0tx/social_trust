from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'user', views.UserView, 'user')
router.register(r'customer', views.CustomerView, 'organization')

urlpatterns = [
    path('', include(router.urls)),
]
