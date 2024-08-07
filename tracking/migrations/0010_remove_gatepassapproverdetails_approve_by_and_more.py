# Generated by Django 4.2.11 on 2024-08-07 11:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tracking', '0009_alter_gatepassinfo_gate_pass_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gatepassapproverdetails',
            name='approve_by',
        ),
        migrations.RemoveField(
            model_name='gatepassapproverdetails',
            name='approved_date',
        ),
        migrations.AddField(
            model_name='gatepassinfo',
            name='approve_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='gatepassinfo',
            name='approved_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]