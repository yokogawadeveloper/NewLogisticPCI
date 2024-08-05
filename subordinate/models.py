from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.

class InsuranceScope(models.Model):
    insurance_scope_name = models.CharField(max_length=100, null=True)
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.insurance_scope_name

    objects = models.Manager()

    class Meta:
        db_table = "InsuranceScope"


class FreightBasis(models.Model):
    freight_basis_name = models.CharField(max_length=100, null=True)
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.freight_basis_name

    objects = models.Manager()

    class Meta:
        db_table = "FreightBasis"


class DeliveryTerms(models.Model):
    delivery_terms_name = models.CharField(max_length=100, null=True)
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.delivery_terms_name

    objects = models.Manager()

    class Meta:
        db_table = "DeliveryTerms"


class ModeOfShipment(models.Model):
    mode_of_shipment_name = models.CharField(max_length=100, null=True)
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.mode_of_shipment_name

    objects = models.Manager()

    class Meta:
        db_table = "ModeOfShipment"


class PaymentStatus(models.Model):
    payment_status_name = models.CharField(max_length=100, null=True)
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.payment_status_name

    objects = models.Manager()

    class Meta:
        db_table = "PaymentStatus"


class SpecialPacking(models.Model):
    special_packing_name = models.CharField(max_length=100, null=True)
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.special_packing_name

    objects = models.Manager()

    class Meta:
        db_table = "SpecialPacking"


class ExportPackingRequirement(models.Model):
    export_packing_requirement_name = models.CharField(max_length=100, null=True)
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.export_packing_requirement_name

    objects = models.Manager()

    class Meta:
        db_table = "ExportPackingRequirement"


class SpecialGSTRate(models.Model):
    special_gst_rate_name = models.CharField(max_length=100, null=True)
    gst_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    cgst_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    sgst_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    igst_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.special_gst_rate_name

    objects = models.Manager()

    class Meta:
        db_table = "SpecialGSTRate"


class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    objects = models.Manager()

    class Meta:
        db_table = "State"


class District(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    objects = models.Manager()

    class Meta:
        db_table = "District"


class Taluk(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    objects = models.Manager()

    class Meta:
        db_table = "Taluk"


class Pincode(models.Model):
    pincode = models.CharField(max_length=6)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    taluk = models.ForeignKey(Taluk, on_delete=models.CASCADE)

    def __str__(self):
        return self.pincode

    objects = models.Manager()

    class Meta:
        db_table = "Pincode"


class CustomerDetails(models.Model):
    customer_code = models.CharField(max_length=200, null=True, blank=True)
    customer_name = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    address1 = models.CharField(max_length=500, null=True, blank=True)
    address2 = models.CharField(max_length=500, null=True, blank=True)
    address3 = models.CharField(max_length=500, null=True, blank=True)
    pincode = models.CharField(max_length=6, null=True, blank=True)
    gst_no = models.CharField(max_length=6, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    # other fields
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "CustomerDetails"

