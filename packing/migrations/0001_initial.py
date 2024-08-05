# Generated by Django 4.2.11 on 2024-08-05 08:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dispatch', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BoxSize',
            fields=[
                ('box_size_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('box_size', models.CharField(blank=True, max_length=500, null=True)),
                ('box_description', models.CharField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'BoxSize',
            },
        ),
        migrations.CreateModel(
            name='ItemPacking',
            fields=[
                ('item_packing_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('item_name', models.CharField(blank=True, max_length=1000, null=True)),
                ('item_qty', models.IntegerField(blank=True, null=True)),
                ('is_parent', models.BooleanField(default=False)),
                ('box_code', models.CharField(blank=True, max_length=300, null=True)),
                ('remarks', models.CharField(blank=True, max_length=300, null=True)),
                ('sub_item_ref', models.IntegerField(blank=True, null=True)),
                ('serial_no', models.CharField(blank=True, max_length=300, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('item_ref_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='packing_master_list', to='dispatch.masteritemlist')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ItemPacking',
            },
        ),
        migrations.CreateModel(
            name='PackingPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(blank=True, max_length=300, null=True)),
                ('exports_price', models.FloatField(blank=True, default=0.0, null=True)),
                ('domestic_price', models.FloatField(blank=True, default=0.0, null=True)),
                ('price', models.FloatField(blank=True, default=0.0, null=True)),
                ('valid_from', models.DateField(blank=True, null=True)),
                ('valid_to', models.DateField(blank=True, null=True)),
                ('revision_no', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('box_size_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='packing.boxsize')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'PackingPrice',
            },
        ),
        migrations.CreateModel(
            name='ItemPackingInline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_no', models.CharField(blank=True, max_length=300, null=True)),
                ('tag_no', models.CharField(blank=True, max_length=300, null=True)),
                ('box_no_manual', models.CharField(blank=True, max_length=50, null=True)),
                ('scale_max', models.FloatField(blank=True, null=True)),
                ('scale_min', models.FloatField(blank=True, null=True)),
                ('scale_unit', models.CharField(blank=True, max_length=100, null=True)),
                ('scale_output', models.CharField(blank=True, max_length=100, null=True)),
                ('range_max', models.FloatField(blank=True, null=True)),
                ('range_min', models.FloatField(blank=True, null=True)),
                ('range_unit', models.CharField(blank=True, max_length=100, null=True)),
                ('range_output', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('inline_item_list_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dispatch.inlineitemlist')),
                ('item_pack_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_packing_inline', to='packing.itempacking')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ItemPackingInline',
            },
        ),
        migrations.CreateModel(
            name='BoxType',
            fields=[
                ('box_type_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('box_type', models.CharField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('prices', models.FloatField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'BoxType',
            },
        ),
        migrations.AddField(
            model_name='boxsize',
            name='box_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='packing.boxtype'),
        ),
        migrations.AddField(
            model_name='boxsize',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='boxsize',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='BoxDetailsFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('box_code', models.CharField(blank=True, max_length=100, null=True)),
                ('file', models.FileField(blank=True, upload_to='multi_file/%Y_%m_%d/%H_%M_%S')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'BoxDetailsFile',
            },
        ),
        migrations.CreateModel(
            name='BoxDetails',
            fields=[
                ('box_details_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('box_code', models.CharField(blank=True, max_length=300, null=True)),
                ('parent_box', models.CharField(blank=True, max_length=300, null=True)),
                ('height', models.FloatField(blank=True, default=0.0, null=True)),
                ('length', models.FloatField(blank=True, default=0.0, null=True)),
                ('breadth', models.FloatField(blank=True, default=0.0, null=True)),
                ('price', models.FloatField(blank=True, default=0.0, null=True)),
                ('remarks', models.CharField(blank=True, max_length=300, null=True)),
                ('main_box', models.BooleanField(default=False)),
                ('status', models.CharField(blank=True, max_length=300, null=True)),
                ('box_serial_no', models.IntegerField(null=True)),
                ('main_dil_no', models.IntegerField(null=True)),
                ('loaded_flag', models.BooleanField(default=False)),
                ('loaded_date', models.DateTimeField(null=True)),
                ('delivery_flag', models.BooleanField(default=False)),
                ('panel_flag', models.BooleanField(null=True)),
                ('box_item_flag', models.BooleanField(default=False)),
                ('gross_weight', models.IntegerField(null=True)),
                ('net_weight', models.IntegerField(null=True)),
                ('qa_wetness', models.IntegerField(null=True)),
                ('project_wetness', models.IntegerField(null=True)),
                ('box_price', models.FloatField(blank=True, default=0.0, null=True)),
                ('box_no_manual', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('box_size', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='box_sizes', to='packing.boxsize')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('dil_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dispatch', to='dispatch.dispatchinstruction')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'BoxDetails',
            },
        ),
    ]
