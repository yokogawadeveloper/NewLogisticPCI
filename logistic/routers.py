from rest_framework import routers
from accounts.views import *
from dispatch.views import *
from dispatch.outwards import *
from master.views import *
from packing.views import *
from subordinate.views import *
from subordinate.labels import *
from workflow.views import *
from tracking.views import *
from tracking.mediators import *
from reports.views import *
from reports.analytics import *

# Add routers here.

router = routers.DefaultRouter()
# ----------------------------- Accounts ------------------------------------------- #
router.register('employee_user', EmployeeUserViewSet, basename='employee_user')
router.register('update_user', UpdateEmployeeUserViewSet, basename='update_user')
router.register('sub_department', SubDepartmentViewSet, basename='sub_department')
# ----------------------------- DispatchInstruction ------------------------------------------- #
router.register('dispatch_instruction', DispatchInstructionViewSet, basename='dispatch_instruction')
router.register('dispatch_unrelated', DispatchUnRelatedViewSet, basename='dispatch_unrelated')
router.register('sap_dispatch_instruction', SAPDispatchInstructionViewSet, basename='sap_dispatch_instruction')
router.register('dispatch_bill_details', DispatchBillDetailsViewSet, basename='dispatch_bill_details')
router.register('master_item_list', MasterItemListViewSet, basename='master_item_list')
router.register('master_item_batch_list', MasterItemBatchViewSet, basename='master_item_batch_list')
router.register('inline_item_list', InlineItemListViewSet, basename='inline_item_list')
router.register('file_type', FileTypeViewSet, basename='file_type')
router.register('multi_file_attachment', MultiFileAttachmentViewSet, basename='multi_file_attachment')
router.register('da_user_request_allocation', DAUserRequestAllocationViewSet, basename='da_user_request_allocation')
router.register('dil_auth_thread', DILAuthThreadsViewSet, basename='dil_auth_thread')
router.register('connection_dispatch', ConnectionDispatchViewSet, basename='connection_dispatch')

# ----------------------------- Master ------------------------------------------- #
router.register('role_master', RoleMasterViewSet, basename='role_master')
router.register('module_master', ModuleMasterViewSet, basename='module_master')
router.register('user_role', UserRoleViewSet, basename='user_role')
router.register('user_access', UserAccessViewSet, basename='user_access')
# ----------------------------- SubOrdinate ------------------------------------------- #
router.register('insurance_scope', InsuranceScopeViewSet, basename='insurance_scope')
router.register('freight_basis', FreightBasisViewSet, basename='freight_basis')
router.register('delivery_terms', DeliveryTermsViewSet, basename='delivery_terms')
router.register('mode_of_shipment', ModeOfShipmentViewSet, basename='mode_of_shipment')
router.register('payment_status', PaymentStatusViewSet, basename='payment_status')
router.register('special_packing', SpecialPackingViewSet, basename='special_packing')
router.register('export_packing', ExportPackingRequirementViewSet, basename='export_packing')
router.register('special_gst_rate', SpecialGSTRateViewSet, basename='special_gst_rate')
router.register('state', StateViewSet, basename='state')
router.register('district', DistrictViewSet, basename='district')
router.register('taluk', TalukViewSet, basename='taluk')
router.register('pincode', PincodeViewSet, basename='pincode')
# ----------------------------- Packing ------------------------------------------- #
router.register('sap_invoice_details', SAPInvoiceDetailsViewSet, basename='sap_invoice_details')
router.register('box_type', BoxTypeViewSet, basename='box_type')
router.register('box_size', BoxSizeViewSet, basename='box_size')
router.register('box_detail', BoxDetailViewSet, basename='box_detail')
router.register('box_detail_file', BoxDetailsFileViewSet, basename='box_detail_file')
router.register('item_packing', ItemPackingViewSet, basename='item_packing')
# ----------------------------- Workflow ------------------------------------------- #
router.register('workflow_type', WorkFLowTypeViewSet, basename='workflow_type')
router.register('workflow_control', WorkFlowControlViewSet, basename='workflow_control')
router.register('workflow_employees', WorkFlowEmployeesViewSet, basename='workflow_employees')
router.register('workflow_da_approvers', WorkFlowDaApproversViewSet, basename='workflow_da_approvers')
router.register('workflow_access', WorkflowAccessViewSet, basename='workflow_access')

# ----------------------------- Tracking ------------------------------------------- #
router.register('truck_type', TruckTypeViewSet, basename='truck_type')
router.register('tracking_transportation', TrackingTransportationViewSet, basename='tracking_transportation')
router.register('truck_request', TruckRequestViewSet, basename='truck_request')
router.register('truck_list', TruckListViewSet, basename='truck_list')
router.register('truck_loading_details', TruckLoadingDetailsViewSet, basename='truck_loading_details')
router.register('delivery_challan', DeliveryChallanViewSet, basename='delivery_challan')
router.register('dc_invoice', DCInvoiceDetailsViewSet, basename='dc_invoice')
router.register('invoice_cheque_details', InvoiceChequeDetailsViewSet, basename='invoice_cheque_details')
router.register('truck_dil_mapped', TruckDIlMappingViewSet, basename='truck_dil_mapped')
router.register('truck_tracking', TruckTrackingViewSet, basename='truck_tracking')
router.register('ewb_details', EWBDetailsViewSet, basename='ewb_details')
router.register('get_pass_info', GatePassInfoViewSet, basename='get_pass_info')
router.register('get_pass_truck_details', GatePassTruckDetailsViewSet, basename='get_pass_truck_details')
router.register('gate_pass_approver_details', GatePassApproverDetailsViewSet, basename='gate_pass_approver_details')

# ----------------------------- Reports ------------------------------------------- #
router.register('dispatch_report', DispatchReportViewSet, basename='dispatch_report')
router.register('box_details_report', BoxDetailsReportViewSet, basename='box_details_report')
router.register('packing_list_pdf', PackingListPDFViewSet, basename='packing_list_pdf')
router.register('customer_consignee_export', CustomerConsigneeExport, basename='customer_consignee_export')
router.register('dc_invoice_details_report', DCInvoiceDetailsReportViewSet, basename='dc_invoice_details_report')
router.register('item_packing_report', ItemPackingReportViewSet, basename='item_packing_report')
router.register('customer_details_pdf', CustomerDocumentsDetailsViewSet, basename='customer_details_pdf')

# ----------------------------- Monitoring ------------------------------------------- #
router.register('monthly_monitor', MonthlyMonitoringViewSet, basename='monthly_monitor')

