from accounts.models import SubDepartment
from subordinate.models import *
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class DispatchInstruction(models.Model):
    dil_id = models.AutoField(primary_key=True)
    dil_no = models.CharField(max_length=20, null=True, blank=True)
    dil_date = models.DateField(auto_now=False, auto_now_add=True)
    so_no = models.CharField(max_length=20, null=True, blank=True)
    po_no = models.CharField(max_length=50, null=True, blank=True)
    po_date = models.CharField(max_length=20, null=True, blank=True)
    bill_to = models.CharField(max_length=100, null=True, blank=True)
    warranty = models.CharField(max_length=100, null=True, blank=True)
    ld = models.CharField(max_length=100, null=True, blank=True)
    wf_type = models.IntegerField(null=True, blank=True)
    current_level = models.IntegerField(null=True, blank=True, default=0)
    dil_level = models.IntegerField(null=True, blank=True, default=0)
    manual_tcs_gc = models.CharField(max_length=100, null=True, blank=True)
    bill_type = models.CharField(max_length=100, null=True, blank=True)
    # other related fields
    dil_from = models.ForeignKey(SubDepartment, on_delete=models.CASCADE, null=True, blank=True)
    insurance_scope = models.ForeignKey(InsuranceScope, on_delete=models.CASCADE, null=True, blank=True)
    freight_basis = models.ForeignKey(FreightBasis, on_delete=models.CASCADE, null=True, blank=True)
    delivery_terms = models.ForeignKey(DeliveryTerms, on_delete=models.CASCADE, null=True, blank=True)
    mode_of_shipment = models.ForeignKey(ModeOfShipment, on_delete=models.CASCADE, null=True, blank=True)
    payment_status = models.ForeignKey(PaymentStatus, on_delete=models.CASCADE, null=True, blank=True)
    special_packing = models.ForeignKey(SpecialPacking, on_delete=models.CASCADE, null=True, blank=True)
    export_packing_req = models.ForeignKey(ExportPackingRequirement, on_delete=models.CASCADE, null=True, blank=True)
    special_gst_rate = models.ForeignKey(SpecialGSTRate, on_delete=models.CASCADE, null=True, blank=True)
    # other information
    advance_packing = models.CharField(max_length=100, null=True, blank=True)
    specific_transport_instruction = models.CharField(max_length=100, null=True, blank=True)
    di_attached = models.CharField(max_length=100, null=True, blank=True)
    customer_contact_details = models.TextField(null=True, blank=True)
    customer_name = models.CharField(max_length=100, null=True, blank=True)
    customer_number = models.CharField(max_length=100, null=True, blank=True)
    partial_shipment = models.CharField(max_length=100, null=True, blank=True)
    if_partial_billable = models.CharField(max_length=100, null=True, blank=True)
    any_other_special_instruction = models.TextField(null=True, blank=True)
    opd_or_ppmg_engineer_name = models.CharField(max_length=100, null=True, blank=True)
    sales_engineer_name = models.CharField(max_length=100, null=True, blank=True)
    sales_office_name = models.CharField(max_length=100, null=True, blank=True)
    ld_applicable = models.CharField(max_length=100, null=True, blank=True)
    cdd = models.CharField(max_length=100, null=True, blank=True)
    finance_by = models.CharField(max_length=100, null=True, blank=True)
    finance_date = models.DateField(blank=True, null=True)
    pqa_by = models.CharField(max_length=100, null=True, blank=True)
    pqa_date = models.DateField(blank=True, null=True)
    approval_level = models.CharField(max_length=100, null=True, blank=True)
    approved_date = models.DateField(blank=True, null=True)
    approved_flag = models.BooleanField(default=False)
    dil_status_no = models.CharField(max_length=100, default=0)
    dil_status = models.CharField(max_length=100, null=True, blank=True)
    dil_sub_status_no = models.IntegerField(null=True, blank=True, default=0)
    revision_flag = models.BooleanField(default=False)
    revision_count = models.IntegerField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True, default="")
    dil_custom_so_flag = models.BooleanField(default=False)
    updated_serial_flag = models.BooleanField(default=False)
    dil_stage = models.IntegerField(null=True, blank=True, default=0)
    # DIL Acknowledge
    submitted_date = models.DateField(blank=True, null=True)
    acknowledge_by = models.CharField(max_length=100, null=True, blank=True)
    acknowledge_date = models.DateField(blank=True, null=True)
    packed_flag = models.BooleanField(default=False)
    packed_date = models.DateField(blank=True, null=True)
    loaded_flag = models.BooleanField(default=False)
    loaded_date = models.DateField(blank=True, null=True)
    dispatched_flag = models.BooleanField(default=False)
    dispatched_date = models.DateField(blank=True, null=True)
    # address
    business_unit = models.CharField(max_length=100, null=True, blank=True)
    ship_to_party_no = models.CharField(max_length=100, null=True, blank=True)
    ship_to_party_name = models.CharField(max_length=100, null=True, blank=True)
    ship_to_address = models.TextField(null=True, blank=True)
    ship_to_city = models.CharField(max_length=100, null=True, blank=True)
    ship_to_postal_code = models.CharField(max_length=100, null=True, blank=True)
    ship_to_country = models.CharField(max_length=100, null=True, blank=True)
    ship_to_gst = models.CharField(max_length=100, null=True, blank=True)

    sold_to_party_no = models.CharField(max_length=100, null=True, blank=True)
    sold_to_party_name = models.CharField(max_length=100, null=True, blank=True)
    sold_to_country = models.CharField(max_length=100, null=True, blank=True)
    sold_to_postal_code = models.CharField(max_length=100, null=True, blank=True)
    sold_to_city = models.CharField(max_length=100, null=True, blank=True)
    sold_to_address = models.TextField(null=True, blank=True)
    sold_to_gst = models.CharField(max_length=100, null=True, blank=True)

    bill_to_party_name = models.CharField(max_length=100, null=True, blank=True)
    bill_to_country = models.CharField(max_length=100, null=True, blank=True)
    bill_to_postal_code = models.CharField(max_length=100, null=True, blank=True)
    bill_to_city = models.CharField(max_length=100, null=True, blank=True)
    bill_to_address = models.TextField(null=True, blank=True)
    bill_to_party_no = models.CharField(max_length=100, null=True, blank=True)
    bill_to_gst = models.CharField(max_length=100, null=True, blank=True)

    payment_term_code = models.CharField(max_length=100, null=True, blank=True)
    payment_term_text = models.TextField(null=True, blank=True)
    file_link_flag = models.BooleanField(default=False)
    only_for_packing_flag = models.BooleanField(default=False)
    # default fields
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        db_table = "DispatchInstruction"


class SAPDispatchInstruction(models.Model):
    sap_dil_id = models.AutoField(primary_key=True)
    reference_doc = models.CharField(max_length=100, null=True, blank=True)
    sold_to_party_no = models.CharField(max_length=100, null=True, blank=True)
    sold_to_party_name = models.CharField(max_length=100, null=True, blank=True)
    delivery = models.CharField(max_length=100, null=True, blank=True)
    delivery_create_date = models.DateField(blank=True, null=True)
    delivery_item = models.CharField(max_length=100, null=True, blank=True)
    tax_invoice_no = models.CharField(max_length=100, null=True, blank=True)
    tax_invoice_date = models.DateField(blank=True, null=True)
    reference_doc_item = models.CharField(max_length=100, null=True, blank=True)
    ms_code = models.CharField(max_length=100, null=True, blank=True)
    sales_quantity = models.IntegerField(null=True, blank=True)
    linkage_no = models.CharField(max_length=100, null=True, blank=True)
    sales_office = models.CharField(max_length=100, null=True, blank=True)
    term_of_payment = models.CharField(max_length=100, null=True, blank=True)
    material_discription = models.CharField(max_length=100, null=True, blank=True)
    plant = models.CharField(max_length=100, null=True, blank=True)
    plant_name = models.CharField(max_length=100, null=True, blank=True)
    unit_sales = models.CharField(max_length=100, null=True, blank=True)
    billing_number = models.CharField(max_length=100, null=True, blank=True)
    billing_create_date = models.DateField(blank=True, null=True)
    currency_type = models.CharField(max_length=100, null=True, blank=True)
    ship_to_party_no = models.CharField(max_length=100, null=True, blank=True)
    ship_to_party_name = models.CharField(max_length=100, null=True, blank=True)
    ship_to_country = models.CharField(max_length=100, null=True, blank=True)
    ship_to_postal_code = models.CharField(max_length=100, null=True, blank=True)
    ship_to_city = models.CharField(max_length=100, null=True, blank=True)
    ship_to_street = models.CharField(max_length=100, null=True, blank=True)
    ship_to_street_for = models.CharField(max_length=100, null=True, blank=True)
    insurance_scope = models.CharField(max_length=100, null=True, blank=True)
    sold_to_country = models.CharField(max_length=100, null=True, blank=True)
    sold_to_postal_code = models.CharField(max_length=100, null=True, blank=True)
    sold_to_city = models.CharField(max_length=100, null=True, blank=True)
    sold_to_street = models.CharField(max_length=100, null=True, blank=True)
    sold_to_street_for = models.CharField(max_length=100, null=True, blank=True)
    material_no = models.CharField(max_length=100, null=True, blank=True)
    hs_code = models.CharField(max_length=100, null=True, blank=True)
    hs_code_export = models.CharField(max_length=100, null=True, blank=True)
    delivery_quantity = models.IntegerField(null=True, blank=True)
    unit_delivery = models.CharField(max_length=100, null=True, blank=True)
    storage_location = models.CharField(max_length=100, null=True, blank=True)
    dil_output_date = models.DateField(blank=True, null=True)
    sales_doc_type = models.CharField(max_length=100, null=True, blank=True)
    distribution_channel = models.CharField(max_length=100, null=True, blank=True)
    invoice_item = models.CharField(max_length=100, null=True, blank=True)
    tax_invoice_assessable_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tax_invoice_total_tax_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tax_invoice_total_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sales_item_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    packing_status = models.CharField(max_length=100, null=True, blank=True)
    do_item_packed_quantity = models.IntegerField(null=True, blank=True)
    packed_unit_quantity = models.CharField(max_length=100, null=True, blank=True)
    # default fields
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        db_table = "SAPDispatchInstruction"


class DispatchBillDetails(models.Model):
    di_bill_id = models.AutoField(primary_key=True)
    dil_id = models.ForeignKey(DispatchInstruction, on_delete=models.CASCADE, null=True, blank=True)
    material_description = models.CharField(max_length=100, null=True, blank=True)
    material_no = models.CharField(max_length=100, null=True, blank=True)
    ms_code = models.CharField(max_length=100, null=True, blank=True)
    s_loc = models.CharField(max_length=100, null=True, blank=True)
    sap_line_item_no = models.CharField(max_length=100, null=True, blank=True)
    linkage_no = models.CharField(max_length=100, null=True, blank=True)
    group = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    country_of_origin = models.CharField(max_length=100, null=True, blank=True)
    item_status = models.CharField(max_length=100, null=True, blank=True)
    item_status_no = models.CharField(max_length=100, null=True, blank=True)
    packed_quantity = models.IntegerField(null=True, blank=True)
    revision_flag = models.BooleanField(default=False)
    revision_count = models.IntegerField(null=True, blank=True, default=0)
    item_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    igst = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cgst = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sgst = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_amount_with_tax = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # default fields
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        db_table = "DispatchBillDetails"


class DispatchPODetails(models.Model):
    so_no = models.CharField(max_length=100, null=True, blank=True)
    po_no = models.CharField(max_length=100, null=True, blank=True)
    po_date = models.DateField(auto_now=False, auto_now_add=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_text = models.CharField(max_length=100, null=True, blank=True)
    sales_person = models.CharField(max_length=100, null=True, blank=True)
    bill_to = models.CharField(max_length=100, null=True, blank=True)
    # default fields
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        db_table = "DispatchPODetails"


class MasterItemList(models.Model):
    item_id = models.AutoField(primary_key=True)
    dil_id = models.ForeignKey(DispatchInstruction, related_name='master_list', on_delete=models.CASCADE, null=True,blank=True)
    item_no = models.CharField(max_length=100, null=True, blank=True)
    unit_of_measurement = models.CharField(max_length=100, null=True, blank=True)
    so_no = models.CharField(max_length=100, null=True, blank=True)
    material_description = models.CharField(max_length=100, null=True, blank=True)
    material_no = models.CharField(max_length=100, null=True, blank=True)
    ms_code = models.CharField(max_length=100, null=True, blank=True)
    s_loc = models.CharField(max_length=100, null=True, blank=True)
    bin = models.CharField(max_length=100, null=True, blank=True)
    plant = models.CharField(max_length=100, null=True, blank=True)
    linkage_no = models.CharField(max_length=100, null=True, blank=True)
    group = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    country_of_origin = models.CharField(max_length=100, null=True, blank=True)
    serial_no = models.CharField(max_length=100, null=True, blank=True)
    match_no = models.CharField(max_length=100, null=True, blank=True)
    tag_no = models.CharField(max_length=100, null=True, blank=True)
    range = models.CharField(max_length=100, null=True, blank=True)
    customer_po_sl_no = models.CharField(max_length=100, null=True, blank=True)
    customer_po_item_code = models.CharField(max_length=100, null=True, blank=True)
    item_status = models.CharField(max_length=100, null=True, blank=True)
    item_status_no = models.CharField(max_length=100, null=True, blank=True)
    packed_quantity = models.IntegerField(default=0)
    revision_flag = models.BooleanField(default=False)
    revision_count = models.IntegerField(null=True, blank=True, default=0)
    verified_by = models.CharField(max_length=100, null=True, blank=True)
    verified_at = models.DateField(auto_now=True, auto_now_add=False)
    verified_flag = models.BooleanField(default=False)
    packed_by = models.CharField(max_length=100, null=True, blank=True)
    packed_at = models.DateField(auto_now=True, auto_now_add=False)
    packing_flag = models.IntegerField(default=0)
    custom_po_flag = models.BooleanField(default=False)
    serial_no_qty = models.IntegerField(null=True, blank=True, default=0)
    serial_flag = models.BooleanField(default=False)
    warranty_flag = models.BooleanField(default=False)
    warranty_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    status_no = models.IntegerField(default=0)
    # default fields
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        db_table = "MasterItemList"


class InlineItemList(models.Model):
    inline_item_id = models.AutoField(primary_key=True)
    master_item = models.ForeignKey(MasterItemList, related_name='inline_items', on_delete=models.CASCADE, null=True,
                                    blank=True)
    serial_no = models.CharField(max_length=100, null=True, blank=True)
    tag_no = models.CharField(max_length=100, null=True, blank=True)
    accessory = models.CharField(max_length=100, null=True, blank=True)
    other_info = models.CharField(max_length=100, null=True, blank=True)
    component_no = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    status_no = models.CharField(max_length=100, null=True, blank=True)
    packed_flag = models.BooleanField(default=False)
    scale_max = models.FloatField(null=True, blank=True)
    scale_min = models.FloatField(null=True, blank=True)
    scale_unit = models.CharField(max_length=100, null=True, blank=True)
    scale_output = models.CharField(max_length=100, null=True, blank=True)
    range_max = models.FloatField(null=True, blank=True)
    range_min = models.FloatField(null=True, blank=True)
    range_unit = models.CharField(max_length=100, null=True, blank=True)
    range_output = models.CharField(max_length=100, null=True, blank=True)
    # default fields
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        db_table = "InlineItemList"


class DAUserRequestAllocation(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    emp_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    dil_id = models.ForeignKey(DispatchInstruction, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=200, null=True, blank=True)
    approve_status = models.CharField(max_length=200, default="Approver")
    approver_flag = models.BooleanField(default=False)
    approved_date = models.DateTimeField(auto_now_add=True, null=True)
    remarks = models.CharField(max_length=500, null=True, blank=True)
    approver_stage = models.CharField(max_length=200, null=True, blank=True)
    approver_level = models.IntegerField(null=True, blank=True)
    # default fields
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        db_table = 'DAUserRequestAllocation'


class DAAuthThreads(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    dil_id = models.ForeignKey(DispatchInstruction, null=True, on_delete=models.CASCADE)
    emp_id = models.IntegerField(null=True)
    remarks = models.CharField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    approver = models.CharField(max_length=50, null=True, blank=True)
    assign_list = models.CharField(max_length=250, null=True, blank=True)

    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()

    class Meta:
        db_table = 'DaAuthThreads'


class FileType(models.Model):
    file_type_id = models.AutoField(primary_key=True)
    file_type = models.CharField(max_length=100, null=True, blank=True)
    file_module_name = models.CharField(max_length=100, null=True, blank=True)
    # default fields
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        db_table = "FileType"


class MultiFileAttachment(models.Model):
    file = models.FileField(upload_to='multi_file/%Y_%m_%d/%H_%M_%S', blank=True)
    dil_id = models.ForeignKey(DispatchInstruction, null=True, on_delete=models.CASCADE)
    file_type = models.ForeignKey(FileType, null=True, on_delete=models.CASCADE)
    module_name = models.CharField(max_length=100, null=True, blank=True)
    module_id = models.IntegerField(blank=True, null=True)
    # default fields
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        db_table = "MultiFileAttachment"
