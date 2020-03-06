from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from api.models import (
    Bank, BankAccount, Beneficiary, Customer, CustomerCode,
    Transaction, OtherAddress, OtherEmail, OtherPhoneNumber
)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
        read_only_fields = ('password',)

class BankSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bank
        fields = ('bank_id', 'bank_name', 'bank_code', 'timestamp')


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ('bank_account_id', 'account_number', 'bank')


class BeneficiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiary
        fields = ('beneficiary_id', 'account_number', 'bank', 'customer')


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    pin = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Pin'}
    )

    class Meta:
        model = Customer
        fields = (
            'customer_id', 'firstname', 'lastname', 'middlename',
            'email', 'pin', 'phonenumber', 'image',  'timestamp'
        )
        read_only_fields = ('customer_id', 'timestamp', 'status')

    def create(self, validated_data):
        validated_data['pin'] = make_password(validated_data.get('pin'))
        return super(CustomerSerializer, self).create(validated_data)

class CustomerCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerCode
        fields = (
            'customer_code_id', 'customer_code', 'bank_account', 'customer',
            'facebook_link', 'twitter_link', 'linkedin_link', 'phonenumber', 'instagram_link', 'timestamp'
        )


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('transaction_id', 'amount', 'customer', 'customer_code', 'beneficiary', 'status', 'timestamp')



class OtherAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherAddress
        fields = ('other_address_id', 'address', 'customer', 'timestamp')
        read_only_fields = ('other_address_id', 'timestamp')


class OtherEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherEmail
        fields = ('other_email_id', 'email', 'customer', 'status', 'timestamp')
        read_only_fields = ('other_email_id', 'timestamp')



class OtherPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherPhoneNumber
        fields = ('other_phone_id', 'phonenumber', 'customer', 'status', 'timestamp')
        read_only_fields = ('other_phone_id', 'timestamp')
