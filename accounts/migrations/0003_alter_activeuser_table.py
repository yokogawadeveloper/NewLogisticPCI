# Generated by Django 4.2.11 on 2024-08-05 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_activeuser'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='activeuser',
            table='ActiveUser',
        ),
    ]
