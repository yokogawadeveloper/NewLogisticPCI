# Generated by Django 4.2.11 on 2024-08-07 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0003_gatepassapproverdetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='gatepassinfo',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
