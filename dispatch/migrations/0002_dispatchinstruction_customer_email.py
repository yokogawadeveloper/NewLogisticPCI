# Generated by Django 4.2.11 on 2024-09-16 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispatch', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dispatchinstruction',
            name='customer_email',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
