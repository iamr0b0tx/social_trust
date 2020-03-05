# Generated by Django 3.0.4 on 2020-03-05 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('bank_id', models.AutoField(primary_key=True, serialize=False)),
                ('bank_name', models.CharField(max_length=45)),
                ('bank_code', models.CharField(max_length=45)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'bank',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('bank_account_id', models.AutoField(primary_key=True, serialize=False)),
                ('account_number', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'bank_account',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Beneficiary',
            fields=[
                ('beneficiary_id', models.AutoField(primary_key=True, serialize=False)),
                ('account_number', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'beneficiary',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.AutoField(primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=45)),
                ('lastname', models.CharField(max_length=45)),
                ('middlename', models.CharField(blank=True, max_length=45, null=True)),
                ('email', models.CharField(max_length=45, unique=True)),
                ('pin', models.CharField(max_length=150)),
                ('phonenumber', models.CharField(max_length=45)),
                ('image', models.CharField(blank=True, max_length=150, null=True)),
                ('status', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'customer',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CustomerCode',
            fields=[
                ('customer_code_id', models.AutoField(primary_key=True, serialize=False)),
                ('customer_code', models.CharField(blank=True, max_length=45, null=True)),
                ('facebook_link', models.CharField(blank=True, max_length=150, null=True)),
                ('twitter_link', models.CharField(blank=True, max_length=100, null=True)),
                ('linkedin_link', models.CharField(blank=True, max_length=100, null=True)),
                ('phonenumber', models.CharField(max_length=45)),
                ('instagram_link', models.CharField(blank=True, max_length=45, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'customer_code',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OtherAddress',
            fields=[
                ('other_address_id', models.AutoField(primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=45)),
                ('status', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'other_address',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OtherEmail',
            fields=[
                ('other_email_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.CharField(blank=True, max_length=45, null=True)),
                ('status', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'other_email',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OtherPhoneNumber',
            fields=[
                ('other_phone_id', models.AutoField(primary_key=True, serialize=False)),
                ('phonenumber', models.CharField(max_length=45)),
                ('status', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'other_phone_number',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField()),
                ('status', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'transaction',
                'managed': False,
            },
        ),
    ]
