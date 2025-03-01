# Generated by Django 5.1.2 on 2024-10-19 09:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allveg', '0033_buyer_business_name_buyer_pan_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyer',
            name='business_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='business_documents', to='allveg.documents'),
        ),
        migrations.AddField(
            model_name='buyer',
            name='gst_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gst_documents', to='allveg.documents'),
        ),
        migrations.AddField(
            model_name='buyer',
            name='pancard_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pancard_details', to='allveg.documents'),
        ),
    ]
