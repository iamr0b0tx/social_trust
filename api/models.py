from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Bank(models.Model):
    bank_id = models.AutoField(primary_key=True)
    bank_name = models.CharField(max_length=45)
    bank_code = models.CharField(max_length=45)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'bank'


class BankAccount(models.Model):
    bank_account_id = models.AutoField(primary_key=True)
    account_number = models.CharField(max_length=15)
    bank = models.ForeignKey(Bank, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'bank_account'


class Beneficiary(models.Model):
    beneficiary_id = models.AutoField(primary_key=True)
    account_number = models.CharField(max_length=45, blank=True, null=True)
    bank = models.ForeignKey(Bank, models.DO_NOTHING)
    customer = models.ForeignKey('Customer', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'beneficiary'


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    middlename = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(unique=True, max_length=45)
    pin = models.CharField(max_length=150)
    phonenumber = models.CharField(max_length=45)
    image = models.CharField(max_length=150, blank=True, null=True)
    status = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'customer'


class CustomerCode(models.Model):
    customer_code_id = models.AutoField(primary_key=True)
    customer_code = models.CharField(max_length=45, blank=True, null=True)
    bank_account = models.ForeignKey(BankAccount, models.DO_NOTHING)
    customer = models.ForeignKey(Customer, models.DO_NOTHING)
    facebook_link = models.CharField(max_length=150, blank=True, null=True)
    twitter_link = models.CharField(max_length=100, blank=True, null=True)
    linkedin_link = models.CharField(max_length=100, blank=True, null=True)
    phonenumber = models.CharField(max_length=45)
    instagram_link = models.CharField(max_length=45, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'customer_code'


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    amount = models.IntegerField()
    customer = models.ForeignKey(Customer, models.DO_NOTHING)
    customer_code = models.ForeignKey(CustomerCode, models.DO_NOTHING, blank=True, null=True)
    beneficiary = models.ForeignKey(Beneficiary, models.DO_NOTHING, blank=True, null=True)
    status = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'transaction'


class OtherAddress(models.Model):
    other_address_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=45)
    customer = models.ForeignKey(Customer, models.DO_NOTHING)
    status = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'other_address'
        unique_together = (('other_address_id', 'customer'),)


class OtherEmail(models.Model):
    other_email_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=45, blank=True, null=True)
    customer = models.ForeignKey(Customer, models.DO_NOTHING)
    status = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'other_email'
        unique_together = (('other_email_id', 'customer'),)


class OtherPhoneNumber(models.Model):
    other_phone_id = models.AutoField(primary_key=True)
    phonenumber = models.CharField(max_length=45)
    customer = models.ForeignKey(Customer, models.DO_NOTHING)
    status = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'other_phone_number'
        unique_together = (('other_phone_id', 'customer'),)
