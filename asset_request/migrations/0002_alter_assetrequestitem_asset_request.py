# Generated by Django 5.0.6 on 2024-06-25 08:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset_request', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetrequestitem',
            name='asset_request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='asset_request_items', to='asset_request.assetrequest'),
        ),
    ]
