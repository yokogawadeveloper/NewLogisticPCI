from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from dispatch.models import DispatchInstruction
from tracking.models import DCInvoiceDetails
from dispatch.serializers import DispatchUnRelatedSerializer
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth


# Create your view
class MonthlyMonitoringViewSet(viewsets.ModelViewSet):
    queryset = DispatchInstruction.objects.all()
    serializer_class = DispatchUnRelatedSerializer

    @action(detail=False, methods=['GET'], url_path='monthly_wise_dil')
    def monthly_wise_dil(self, request):
        try:
            # Initialize dictionaries for all months with counts set to 0
            all_months_non_billable = {i: 0 for i in range(1, 13)}
            all_months_billable = {i: 0 for i in range(1, 13)}

            # Process NonBillable records
            non_billable_dispatch = (
                DispatchInstruction.objects.filter(bill_type='NonBillable')
                .annotate(month=TruncMonth('created_at'))
                .values('month')
                .annotate(count=Count('dil_id'))
                .order_by('month')
            )

            # Update the dictionary with actual counts for NonBillable records
            for entry in non_billable_dispatch:
                month_number = entry['month'].month
                all_months_non_billable[month_number] = entry['count']

            # Process Billable records
            billable_dispatch = (
                DispatchInstruction.objects.filter(bill_type='Billable')
                .annotate(month=TruncMonth('created_at'))
                .values('month')
                .annotate(count=Count('dil_id'))
                .order_by('month')
            )

            # Update the dictionary with actual counts for Billable records
            for entry in billable_dispatch:
                month_number = entry['month'].month
                all_months_billable[month_number] = entry['count']

            # Convert the counts to a list in order from January (index 0) to December (index 11)
            non_billable_monthly_counts = [all_months_non_billable[month] for month in range(1, 13)]
            billable_monthly_counts = [all_months_billable[month] for month in range(1, 13)]

            response_data = {
                'non_billable_monthly_counts': non_billable_monthly_counts,
                'billable_monthly_counts': billable_monthly_counts,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), 'status': status.HTTP_400_BAD_REQUEST})

    @action(detail=False, methods=['GET'], url_path='monthly_wise_billing')
    def monthly_wise_billing(self, request):
        try:
            all_months = {i: 0 for i in range(1, 13)}

            all_billing_invoice = (
                DCInvoiceDetails.objects.filter(bill_type='invoice')
                .annotate(month=TruncMonth('created_at'))
                .values('month')
                .annotate(total_amount=Sum('bill_amount'))
                .order_by('month')
            )

            # Update the dictionary with actual sums for each month
            for entry in all_billing_invoice:
                month_number = entry['month'].month
                all_months[month_number] = entry['total_amount']

            # Convert the sums to a list in order from January (index 0) to December (index 11)
            data = [all_months[month] for month in range(1, 13)]
            return Response({'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), 'status': status.HTTP_400_BAD_REQUEST})

