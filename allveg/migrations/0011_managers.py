# Generated by Django 5.0.2 on 2024-10-13 17:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allveg', '0010_generalmanagers_legal_compliance_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Managers',
            fields=[
                ('manager_id', models.AutoField(primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('phone_number', models.CharField(max_length=10, unique=True)),
                ('fathers_or_husbands_name', models.CharField(blank=True, max_length=50, null=True)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10, null=True)),
                ('aadhaar_number', models.CharField(max_length=20, unique=True)),
                ('residential_address', models.CharField(max_length=255)),
                ('designation', models.CharField(max_length=55)),
                ('assigned_city', models.CharField(max_length=55)),
                ('joining_date', models.DateTimeField()),
                ('employee_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('document_path', models.FileField(blank=True, null=True, upload_to='')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('bank_details_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='allveg.bankdetails')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='manager_creator', to='allveg.users')),
                ('document_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='allveg.documents')),
                ('legal_compliance_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='allveg.legalcompliance')),
                ('superior_general_manager_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='allveg.generalmanagers')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='allveg.users')),
            ],
        ),
    ]
