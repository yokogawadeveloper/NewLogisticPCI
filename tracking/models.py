from dispatch.models import DispatchInstruction
from subordinate.models import *

User = get_user_model()


# Create your models here.
class SAPInvoiceDetails(models.Model):
    reference_no = models.CharField(max_length=100, null=True, blank=True)
    delivery = models.CharField(max_length=100, null=True, blank=True)
    delivery_item = models.CharField(max_length=100, null=True, blank=True)
    tax_invoice_no = models.CharField(max_length=100, null=True, blank=True)
    tax_invoice_date = models.DateField(null=True, blank=True)
    reference_doc_item = models.CharField(max_length=100, null=True, blank=True)
    billing_no = models.CharField(max_length=100, null=True, blank=True)
    billing_created_date = models.DateField(null=True, blank=True)
    hs_code = models.CharField(max_length=100, null=True, blank=True)
    hs_code_export = models.CharField(max_length=100, null=True, blank=True)
    delivery_qty = models.IntegerField(null=True, blank=True)
    delivery_unit = models.CharField(max_length=100, null=True, blank=True)
    tax_invoice_assessable_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tax_invoice_total_tax_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tax_invoice_total_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sales_item_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    packing_status = models.CharField(max_length=150, null=True, blank=True)
    do_item_packed_qty = models.IntegerField(null=True, blank=True)
    packed_qty_unit = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        db_table = 'SAPInvoiceDetails'


class TruckType(models.Model):
    truck_type_name = models.CharField(max_length=100, null=True)
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        db_table = 'TruckType'


class TrackingTransportation(models.Model):
    truck_type = models.ForeignKey(TruckType, on_delete=models.CASCADE)
    transportation_name = models.CharField(max_length=100, null=True)
    contact_number = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    # other fields
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        db_table = 'TrackingTransportation'


class TruckRequest(models.Model):
    transporter = models.ForeignKey(TrackingTransportation, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True)
    taluk = models.ForeignKey(Taluk, on_delete=models.CASCADE, null=True)
    pincode = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=100, null=True)
    remarks = models.TextField(null=True)
    # other fields
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        db_table = 'TruckRequest'


class TruckRequestTypesList(models.Model):
    truck_request = models.ForeignKey(TruckRequest, on_delete=models.CASCADE)
    truck_type = models.ForeignKey(TruckType, related_name='truck_request_type_list', on_delete=models.CASCADE)
    truck_count = models.IntegerField(default=0)
    # other fields
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        db_table = 'TruckRequestTypesList'


class TruckList(models.Model):
    truck_type = models.ForeignKey(TruckType, null=True, on_delete=models.CASCADE)
    transportation = models.ForeignKey(TrackingTransportation, null=True, on_delete=models.CASCADE)
    truck_request = models.ForeignKey(TruckRequest, null=True, on_delete=models.CASCADE)
    truck_request_types_list = models.ForeignKey(TruckRequestTypesList, null=True, on_delete=models.CASCADE)
    vehicle_no = models.CharField(max_length=50, null=True, blank=True)
    driver_name = models.CharField(max_length=50, null=True, blank=True)
    driver_no = models.CharField(max_length=50, null=True, blank=True)
    rating = models.CharField(max_length=20, null=True, blank=True)
    rating_remarks = models.CharField(max_length=200, null=True, blank=True)
    check_in = models.DateTimeField(null=True, blank=True)
    check_in_remarks = models.CharField(max_length=500, null=True, blank=True)
    check_out_remarks = models.CharField(max_length=500, null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    check_out_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    gate_pass_no = models.IntegerField(default=0)
    status = models.CharField(max_length=50, default='Open')
    loading_remarks = models.CharField(max_length=300, null=True)
    delivered_datetime = models.DateTimeField(null=True)
    loaded_flag = models.BooleanField(default=False)
    loaded_date = models.DateTimeField(null=True)
    tracking_status = models.IntegerField(default=0)
    tracking_flag = models.IntegerField(default=0)
    tracking_date = models.DateTimeField(null=True)
    expected_date = models.DateField(null=True, blank=True)
    remarks = models.TextField(null=True)
    oa_details = models.BooleanField(default=False, null=True, blank=True)
    no_of_boxes = models.IntegerField(default=0)
    # other fields
    created_by = models.ForeignKey(User, related_name='UserTable', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        db_table = 'TruckList'


class TruckDilMappingDetails(models.Model):
    dil_id = models.ForeignKey(DispatchInstruction, null=True, on_delete=models.CASCADE)
    truck_list_id = models.ForeignKey(TruckList, null=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        db_table = 'TruckDilMappingDetails'


class TruckLoadingDetails(models.Model):
    dil_id = models.ForeignKey(DispatchInstruction, null=True, on_delete=models.CASCADE)
    truck_list_id = models.ForeignKey(TruckList, null=True, on_delete=models.CASCADE)
    box_code = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        db_table = 'TruckLoadingDetails'


class TruckDeliveryDetails(models.Model):
    truck_list_id = models.ForeignKey(TruckList, null=True, on_delete=models.CASCADE)
    current_datetime = models.DateTimeField(null=True)
    current_location = models.CharField(max_length=1000, null=True)
    current_latitude = models.CharField(max_length=50, null=True)
    current_longitude = models.CharField(max_length=50, null=True)
    current_status = models.CharField(max_length=250, null=True)
    manual_flag = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        db_table = 'TruckDeliveryDetails'


class DeliveryChallan(models.Model):
    truck_list = models.ForeignKey(TruckList, on_delete=models.CASCADE)
    e_way_bill_no = models.CharField(max_length=100, null=True)
    e_way_bills_date = models.DateField(null=True, blank=True)
    delivers_dates = models.DateField(null=True, blank=True)
    lrn_no = models.CharField(max_length=100, null=True)
    lrn_date = models.DateField(null=True, blank=True)
    no_of_boxes = models.IntegerField(default=0)
    description_of_goods = models.CharField(max_length=200, null=True)
    mode_of_delivery = models.CharField(max_length=100, null=True)
    freight_mode = models.CharField(max_length=100, null=True)
    destination = models.CharField(max_length=100, null=True)
    kind_attended = models.CharField(max_length=100, null=True)
    consignee_remakes = models.CharField(max_length=100, null=True)
    remarks = models.TextField(null=True)
    # other fields
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        db_table = 'DeliveryChallan'

    def invoice_details(self):
        return DCInvoiceDetails.objects.filter(delivery_challan=self)


class DCInvoiceDetails(models.Model):
    delivery_challan = models.ForeignKey(DeliveryChallan, related_name='dc_invoice_details', on_delete=models.CASCADE)
    dil_id = models.ForeignKey(DispatchInstruction, null=True, on_delete=models.CASCADE)
    truck_list = models.ForeignKey(TruckList, on_delete=models.CASCADE)
    so_no = models.CharField(max_length=100, null=True)
    bill_no = models.CharField(max_length=100, null=True, blank=True)
    bill_date = models.DateField(null=True, blank=True)
    bill_type = models.CharField(max_length=100, null=True)
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    eway_bill_no = models.CharField(max_length=100, null=True, blank=True)
    eway_bill_date = models.DateField(null=True, blank=True)
    # other fields
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        db_table = 'DCInvoiceDetails'


class InvoiceChequeDetails(models.Model):
    dc_invoice_details = models.ForeignKey(DCInvoiceDetails, related_name='invoice_cheque_details',
                                           on_delete=models.CASCADE)
    cod_cheque_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    invoice_no = models.CharField(max_length=100, null=True)
    cheque_no = models.CharField(max_length=100, null=True)
    cod_cheque_received_date = models.DateField(null=True, blank=True)
    bank_name = models.CharField(max_length=100, null=True)
    cheque_date = models.DateField(null=True, blank=True)
    cheque_withdrawal_date = models.DateField(null=True, blank=True)
    remarks = models.CharField(max_length=100, null=True)
    # other fields
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        db_table = 'InvoiceChequeDetails'


class EWBDetails(models.Model):
    ewb_no = models.CharField(max_length=100, null=True, blank=True)
    ewb_date = models.DateField(null=True, blank=True)
    supply_type = models.CharField(max_length=100, null=True, blank=True)
    doc_no = models.CharField(max_length=100, null=True, blank=True)
    doc_date = models.DateField(null=True, blank=True)
    doc_type = models.CharField(max_length=100, null=True, blank=True)
    other_party_gstin = models.CharField(max_length=100, null=True, blank=True)
    transporter_details = models.CharField(max_length=100, null=True, blank=True)
    from_gstin = models.CharField(max_length=100, null=True, blank=True)
    to_gstin = models.CharField(max_length=100, null=True, blank=True)
    from_gstin_info = models.CharField(max_length=1000, null=True, blank=True)
    to_gstin_info = models.CharField(max_length=1000, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    no_of_items = models.IntegerField(default=0)
    main_hsn_code = models.CharField(max_length=100, null=True, blank=True)
    main_hsn_desc = models.CharField(max_length=100, null=True, blank=True)
    assessable_value = models.CharField(max_length=100, null=True, blank=True)
    sgst_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cgst_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    igst_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cess_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cess_non_adv_value = models.IntegerField(default=0)
    other_value = models.IntegerField(default=0)
    total_invoice_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valid_till_date = models.DateField(null=True, blank=True)
    other_party_rejection_status = models.CharField(max_length=100, null=True, blank=True)
    inr = models.CharField(max_length=100, null=True, blank=True)
    gen_mode = models.CharField(max_length=100, null=True, blank=True)
    # other fields
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        db_table = 'EWBDetails'


class GatePassInfo(models.Model):
    driver_name = models.CharField(max_length=100, null=True, blank=True)
    transporter_name = models.CharField(max_length=100, null=True, blank=True)
    checkin_date = models.DateField(null=True, blank=True)
    normal_remarks = models.CharField(max_length=300, null=True, blank=True)
    status_no = models.CharField(max_length=100, null=True, blank=True)
    gate_pass_no = models.IntegerField(null=True, blank=True)
    gate_pass_type = models.CharField(max_length=100, null=True, blank=True)
    checkout_date = models.DateField(null=True, blank=True)
    checkout_remarks = models.CharField(max_length=300, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    approve_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    approved_date = models.DateField(null=True, blank=True)
    # other filed
    create_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()

    class Meta:
        db_table = 'GatePassInfo'


class GatePassTruckDetails(models.Model):
    gate_info = models.ForeignKey(GatePassInfo, related_name='gate_pass_truck_details', on_delete=models.CASCADE)
    truck_info = models.ForeignKey(TruckList, related_name='gate_pass_truck_details', on_delete=models.CASCADE)
    # other filed
    create_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()

    class Meta:
        db_table = 'GatePassTruckDetails'


class GatePassApproverDetails(models.Model):
    gate_info = models.ForeignKey(GatePassInfo, related_name='gate_pass_approver_details', on_delete=models.CASCADE)
    emp = models.ForeignKey(User, related_name='gate_pass_approver_details', on_delete=models.CASCADE)
    approver_status = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.CharField(max_length=100, null=True, blank=True)
    status_no = models.IntegerField(null=True, blank=True)
    approver_flag = models.BooleanField(default=False)
    create_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()

    class Meta:
        db_table = 'GatePassApproverDetails'
        unique_together = (('gate_info', 'emp'),)


class GatePassAuthThreads(models.Model):
    gate_pass_info = models.ForeignKey(GatePassInfo, related_name='gate_pass_auth_threads', on_delete=models.CASCADE)
    emp = models.ForeignKey(User, related_name='gate_pass_auth_threads', on_delete=models.CASCADE)
    status = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()

    class Meta:
        db_table = 'GatePassAuthThreads'
