# Generated by Django 4.2.11 on 2024-08-05 08:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subordinate', '0001_initial'),
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DispatchInstruction',
            fields=[
                ('dil_id', models.AutoField(primary_key=True, serialize=False)),
                ('dil_no', models.CharField(blank=True, max_length=20, null=True)),
                ('dil_date', models.DateField(auto_now_add=True)),
                ('so_no', models.CharField(blank=True, max_length=20, null=True)),
                ('po_no', models.CharField(blank=True, max_length=50, null=True)),
                ('po_date', models.CharField(blank=True, max_length=20, null=True)),
                ('bill_to', models.CharField(blank=True, max_length=100, null=True)),
                ('warranty', models.CharField(blank=True, max_length=100, null=True)),
                ('ld', models.CharField(blank=True, max_length=100, null=True)),
                ('wf_type', models.IntegerField(blank=True, null=True)),
                ('current_level', models.IntegerField(blank=True, default=0, null=True)),
                ('dil_level', models.IntegerField(blank=True, default=0, null=True)),
                ('manual_tcs_gc', models.CharField(blank=True, max_length=100, null=True)),
                ('bill_type', models.CharField(blank=True, max_length=100, null=True)),
                ('advance_packing', models.CharField(blank=True, max_length=100, null=True)),
                ('specific_transport_instruction', models.CharField(blank=True, max_length=100, null=True)),
                ('di_attached', models.CharField(blank=True, max_length=100, null=True)),
                ('customer_contact_details', models.TextField(blank=True, null=True)),
                ('customer_name', models.CharField(blank=True, max_length=100, null=True)),
                ('customer_number', models.CharField(blank=True, max_length=100, null=True)),
                ('partial_shipment', models.CharField(blank=True, max_length=100, null=True)),
                ('if_partial_billable', models.CharField(blank=True, max_length=100, null=True)),
                ('any_other_special_instruction', models.TextField(blank=True, null=True)),
                ('opd_or_ppmg_engineer_name', models.CharField(blank=True, max_length=100, null=True)),
                ('sales_engineer_name', models.CharField(blank=True, max_length=100, null=True)),
                ('sales_office_name', models.CharField(blank=True, max_length=100, null=True)),
                ('ld_applicable', models.CharField(blank=True, max_length=100, null=True)),
                ('cdd', models.CharField(blank=True, max_length=100, null=True)),
                ('finance_by', models.CharField(blank=True, max_length=100, null=True)),
                ('finance_date', models.DateField(blank=True, null=True)),
                ('pqa_by', models.CharField(blank=True, max_length=100, null=True)),
                ('pqa_date', models.DateField(blank=True, null=True)),
                ('approval_level', models.CharField(blank=True, max_length=100, null=True)),
                ('approved_date', models.DateField(blank=True, null=True)),
                ('approved_flag', models.BooleanField(default=False)),
                ('dil_status_no', models.CharField(default=0, max_length=100)),
                ('dil_status', models.CharField(blank=True, max_length=100, null=True)),
                ('dil_sub_status_no', models.IntegerField(blank=True, default=0, null=True)),
                ('revision_flag', models.BooleanField(default=False)),
                ('revision_count', models.IntegerField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, default='', null=True)),
                ('dil_custom_so_flag', models.BooleanField(default=False)),
                ('updated_serial_flag', models.BooleanField(default=False)),
                ('dil_stage', models.IntegerField(blank=True, default=0, null=True)),
                ('submitted_date', models.DateField(blank=True, null=True)),
                ('acknowledge_by', models.CharField(blank=True, max_length=100, null=True)),
                ('acknowledge_date', models.DateField(blank=True, null=True)),
                ('packed_flag', models.BooleanField(default=False)),
                ('packed_date', models.DateField(blank=True, null=True)),
                ('loaded_flag', models.BooleanField(default=False)),
                ('loaded_date', models.DateField(blank=True, null=True)),
                ('dispatched_flag', models.BooleanField(default=False)),
                ('dispatched_date', models.DateField(blank=True, null=True)),
                ('business_unit', models.CharField(blank=True, max_length=100, null=True)),
                ('ship_to_party_no', models.CharField(blank=True, max_length=100, null=True)),
                ('ship_to_party_name', models.CharField(blank=True, max_length=100, null=True)),
                ('ship_to_address', models.TextField(blank=True, null=True)),
                ('ship_to_city', models.CharField(blank=True, max_length=100, null=True)),
                ('ship_to_postal_code', models.CharField(blank=True, max_length=100, null=True)),
                ('ship_to_country', models.CharField(blank=True, max_length=100, null=True)),
                ('ship_to_gst', models.CharField(blank=True, max_length=100, null=True)),
                ('sold_to_party_no', models.CharField(blank=True, max_length=100, null=True)),
                ('sold_to_party_name', models.CharField(blank=True, max_length=100, null=True)),
                ('sold_to_country', models.CharField(blank=True, max_length=100, null=True)),
                ('sold_to_postal_code', models.CharField(blank=True, max_length=100, null=True)),
                ('sold_to_city', models.CharField(blank=True, max_length=100, null=True)),
                ('sold_to_address', models.TextField(blank=True, null=True)),
                ('sold_to_gst', models.CharField(blank=True, max_length=100, null=True)),
                ('bill_to_party_name', models.CharField(blank=True, max_length=100, null=True)),
                ('bill_to_country', models.CharField(blank=True, max_length=100, null=True)),
                ('bill_to_postal_code', models.CharField(blank=True, max_length=100, null=True)),
                ('bill_to_city', models.CharField(blank=True, max_length=100, null=True)),
                ('bill_to_address', models.TextField(blank=True, null=True)),
                ('bill_to_party_no', models.CharField(blank=True, max_length=100, null=True)),
                ('bill_to_gst', models.CharField(blank=True, max_length=100, null=True)),
                ('payment_term_code', models.CharField(blank=True, max_length=100, null=True)),
                ('payment_term_text', models.TextField(blank=True, null=True)),
                ('file_link_flag', models.BooleanField(default=False)),
                ('only_for_packing_flag', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('delivery_terms', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='subordinate.deliveryterms')),
                ('dil_from', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.subdepartment')),
                ('export_packing_req', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='subordinate.exportpackingrequirement')),
                ('freight_basis', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='subordinate.freightbasis')),
                ('insurance_scope', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='subordinate.insurancescope')),
                ('mode_of_shipment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='subordinate.modeofshipment')),
                ('payment_status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='subordinate.paymentstatus')),
                ('special_gst_rate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='subordinate.specialgstrate')),
                ('special_packing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='subordinate.specialpacking')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'DispatchInstruction',
            },
        ),
        migrations.CreateModel(
            name='FileType',
            fields=[
                ('file_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('file_type', models.CharField(blank=True, max_length=100, null=True)),
                ('file_module_name', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'FileType',
            },
        ),
        migrations.CreateModel(
            name='SAPDispatchInstruction',
            fields=[
                ('sap_dil_id', models.AutoField(primary_key=True, serialize=False)),
                ('reference_doc', models.CharField(blank=True, max_length=100, null=True)),
                ('sold_to_party_no', models.CharField(blank=True, max_length=100, null=True)),
                ('sold_to_party_name', models.CharField(blank=True, max_length=100, null=True)),
                ('delivery', models.CharField(blank=True, max_length=100, null=True)),
                ('delivery_create_date', models.DateField(blank=True, null=True)),
                ('delivery_item', models.CharField(blank=True, max_length=100, null=True)),
                ('tax_invoice_no', models.CharField(blank=True, max_length=100, null=True)),
                ('tax_invoice_date', models.DateField(blank=True, null=True)),
                ('reference_doc_item', models.CharField(blank=True, max_length=100, null=True)),
                ('ms_code', models.CharField(blank=True, max_length=100, null=True)),
                ('sales_quantity', models.IntegerField(blank=True, null=True)),
                ('linkage_no', models.CharField(blank=True, max_length=100, null=True)),
                ('sales_office', models.CharField(blank=True, max_length=100, null=True)),
                ('term_of_payment', models.CharField(blank=True, max_length=100, null=True)),
                ('material_discription', models.CharField(blank=True, max_length=100, null=True)),
                ('plant', models.CharField(blank=True, max_length=100, null=True)),
                ('plant_name', models.CharField(blank=True, max_length=100, null=True)),
                ('unit_sales', models.CharField(blank=True, max_length=100, null=True)),
                ('billing_number', models.CharField(blank=True, max_length=100, null=True)),
                ('billing_create_date', models.DateField(blank=True, null=True)),
                ('currency_type', models.CharField(blank=True, max_length=100, null=True)),
                ('ship_to_party_no', models.CharField(blank=True, max_length=100, null=True)),
                ('ship_to_party_name', models.CharField(blank=True, max_length=100, null=True)),
                ('ship_to_country', models.CharField(blank=True, max_length=100, null=True)),
                ('ship_to_postal_code', models.CharField(blank=True, max_length=100, null=True)),
                ('ship_to_city', models.CharField(blank=True, max_length=100, null=True)),
                ('ship_to_street', models.CharField(blank=True, max_length=100, null=True)),
                ('ship_to_street_for', models.CharField(blank=True, max_length=100, null=True)),
                ('insurance_scope', models.CharField(blank=True, max_length=100, null=True)),
                ('sold_to_country', models.CharField(blank=True, max_length=100, null=True)),
                ('sold_to_postal_code', models.CharField(blank=True, max_length=100, null=True)),
                ('sold_to_city', models.CharField(blank=True, max_length=100, null=True)),
                ('sold_to_street', models.CharField(blank=True, max_length=100, null=True)),
                ('sold_to_street_for', models.CharField(blank=True, max_length=100, null=True)),
                ('material_no', models.CharField(blank=True, max_length=100, null=True)),
                ('hs_code', models.CharField(blank=True, max_length=100, null=True)),
                ('hs_code_export', models.CharField(blank=True, max_length=100, null=True)),
                ('delivery_quantity', models.IntegerField(blank=True, null=True)),
                ('unit_delivery', models.CharField(blank=True, max_length=100, null=True)),
                ('storage_location', models.CharField(blank=True, max_length=100, null=True)),
                ('dil_output_date', models.DateField(blank=True, null=True)),
                ('sales_doc_type', models.CharField(blank=True, max_length=100, null=True)),
                ('distribution_channel', models.CharField(blank=True, max_length=100, null=True)),
                ('invoice_item', models.CharField(blank=True, max_length=100, null=True)),
                ('tax_invoice_assessable_value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('tax_invoice_total_tax_value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('tax_invoice_total_value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('sales_item_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('packing_status', models.CharField(blank=True, max_length=100, null=True)),
                ('do_item_packed_quantity', models.IntegerField(blank=True, null=True)),
                ('packed_unit_quantity', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'SAPDispatchInstruction',
            },
        ),
        migrations.CreateModel(
            name='MultiFileAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to='multi_file/%Y_%m_%d/%H_%M_%S')),
                ('module_name', models.CharField(blank=True, max_length=100, null=True)),
                ('module_id', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('dil_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dispatch.dispatchinstruction')),
                ('file_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dispatch.filetype')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'MultiFileAttachment',
            },
        ),
        migrations.CreateModel(
            name='MasterItemList',
            fields=[
                ('item_id', models.AutoField(primary_key=True, serialize=False)),
                ('item_no', models.CharField(blank=True, max_length=100, null=True)),
                ('unit_of_measurement', models.CharField(blank=True, max_length=100, null=True)),
                ('so_no', models.CharField(blank=True, max_length=100, null=True)),
                ('material_description', models.CharField(blank=True, max_length=100, null=True)),
                ('material_no', models.CharField(blank=True, max_length=100, null=True)),
                ('ms_code', models.CharField(blank=True, max_length=100, null=True)),
                ('s_loc', models.CharField(blank=True, max_length=100, null=True)),
                ('bin', models.CharField(blank=True, max_length=100, null=True)),
                ('plant', models.CharField(blank=True, max_length=100, null=True)),
                ('linkage_no', models.CharField(blank=True, max_length=100, null=True)),
                ('group', models.CharField(blank=True, max_length=100, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('country_of_origin', models.CharField(blank=True, max_length=100, null=True)),
                ('serial_no', models.CharField(blank=True, max_length=100, null=True)),
                ('match_no', models.CharField(blank=True, max_length=100, null=True)),
                ('tag_no', models.CharField(blank=True, max_length=100, null=True)),
                ('range', models.CharField(blank=True, max_length=100, null=True)),
                ('customer_po_sl_no', models.CharField(blank=True, max_length=100, null=True)),
                ('customer_po_item_code', models.CharField(blank=True, max_length=100, null=True)),
                ('item_status', models.CharField(blank=True, max_length=100, null=True)),
                ('item_status_no', models.CharField(blank=True, max_length=100, null=True)),
                ('packed_quantity', models.IntegerField(default=0)),
                ('revision_flag', models.BooleanField(default=False)),
                ('revision_count', models.IntegerField(blank=True, default=0, null=True)),
                ('verified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('verified_at', models.DateField(auto_now=True)),
                ('verified_flag', models.BooleanField(default=False)),
                ('packed_by', models.CharField(blank=True, max_length=100, null=True)),
                ('packed_at', models.DateField(auto_now=True)),
                ('packing_flag', models.IntegerField(default=0)),
                ('custom_po_flag', models.BooleanField(default=False)),
                ('serial_no_qty', models.IntegerField(blank=True, default=0, null=True)),
                ('serial_flag', models.BooleanField(default=False)),
                ('warranty_flag', models.BooleanField(default=False)),
                ('warranty_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('status_no', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('dil_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='master_list', to='dispatch.dispatchinstruction')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'MasterItemList',
            },
        ),
        migrations.CreateModel(
            name='InlineItemList',
            fields=[
                ('inline_item_id', models.AutoField(primary_key=True, serialize=False)),
                ('serial_no', models.CharField(blank=True, max_length=100, null=True)),
                ('tag_no', models.CharField(blank=True, max_length=100, null=True)),
                ('accessory', models.CharField(blank=True, max_length=100, null=True)),
                ('other_info', models.CharField(blank=True, max_length=100, null=True)),
                ('component_no', models.CharField(blank=True, max_length=100, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('status_no', models.CharField(blank=True, max_length=100, null=True)),
                ('packed_flag', models.BooleanField(default=False)),
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
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('master_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inline_items', to='dispatch.masteritemlist')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'InlineItemList',
            },
        ),
        migrations.CreateModel(
            name='DispatchPODetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('so_no', models.CharField(blank=True, max_length=100, null=True)),
                ('po_no', models.CharField(blank=True, max_length=100, null=True)),
                ('po_date', models.DateField(auto_now_add=True)),
                ('payment_id', models.CharField(blank=True, max_length=100, null=True)),
                ('payment_text', models.CharField(blank=True, max_length=100, null=True)),
                ('sales_person', models.CharField(blank=True, max_length=100, null=True)),
                ('bill_to', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'DispatchPODetails',
            },
        ),
        migrations.CreateModel(
            name='DispatchBillDetails',
            fields=[
                ('di_bill_id', models.AutoField(primary_key=True, serialize=False)),
                ('material_description', models.CharField(blank=True, max_length=100, null=True)),
                ('material_no', models.CharField(blank=True, max_length=100, null=True)),
                ('ms_code', models.CharField(blank=True, max_length=100, null=True)),
                ('s_loc', models.CharField(blank=True, max_length=100, null=True)),
                ('sap_line_item_no', models.CharField(blank=True, max_length=100, null=True)),
                ('linkage_no', models.CharField(blank=True, max_length=100, null=True)),
                ('group', models.CharField(blank=True, max_length=100, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('country_of_origin', models.CharField(blank=True, max_length=100, null=True)),
                ('item_status', models.CharField(blank=True, max_length=100, null=True)),
                ('item_status_no', models.CharField(blank=True, max_length=100, null=True)),
                ('packed_quantity', models.IntegerField(blank=True, null=True)),
                ('revision_flag', models.BooleanField(default=False)),
                ('revision_count', models.IntegerField(blank=True, default=0, null=True)),
                ('item_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('igst', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('cgst', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('sgst', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('tax_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total_amount_with_tax', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('dil_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dispatch.dispatchinstruction')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'DispatchBillDetails',
            },
        ),
        migrations.CreateModel(
            name='DAUserRequestAllocation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('status', models.CharField(blank=True, max_length=200, null=True)),
                ('approve_status', models.CharField(default='Approver', max_length=200)),
                ('approver_flag', models.BooleanField(default=False)),
                ('approved_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('remarks', models.CharField(blank=True, max_length=500, null=True)),
                ('approver_stage', models.CharField(blank=True, max_length=200, null=True)),
                ('approver_level', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('dil_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dispatch.dispatchinstruction')),
                ('emp_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'DAUserRequestAllocation',
            },
        ),
        migrations.CreateModel(
            name='DAAuthThreads',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('emp_id', models.IntegerField(null=True)),
                ('remarks', models.CharField(blank=True, max_length=500, null=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('approver', models.CharField(blank=True, max_length=50, null=True)),
                ('assign_list', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('dil_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dispatch.dispatchinstruction')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'DaAuthThreads',
            },
        ),
    ]
