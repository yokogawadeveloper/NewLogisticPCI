from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.response import Response
from .serializers import *


# Create your views here.
class InsuranceScopeViewSet(viewsets.ModelViewSet):
    queryset = InsuranceScope.objects.all()
    serializer_class = InsuranceScopeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query_set = self.queryset.filter(is_active=True)
        return query_set

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = InsuranceScopeSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = InsuranceScopeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = InsuranceScopeSerializer(instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FreightBasisViewSet(viewsets.ModelViewSet):
    queryset = FreightBasis.objects.all()
    serializer_class = FreightBasisSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query_set = self.queryset.filter(is_active=True)
        return query_set

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = FreightBasisSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = FreightBasisSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = FreightBasisSerializer(instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeliveryTermsViewSet(viewsets.ModelViewSet):
    queryset = DeliveryTerms.objects.all()
    serializer_class = DeliveryTermsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query_set = self.queryset.filter(is_active=True)
        return query_set

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = DeliveryTermsSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = DeliveryTermsSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DeliveryTermsSerializer(instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ModeOfShipmentViewSet(viewsets.ModelViewSet):
    queryset = ModeOfShipment.objects.all()
    serializer_class = ModeOfShipmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query_set = self.queryset.filter(is_active=True)
        return query_set

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ModeOfShipmentSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = ModeOfShipmentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ModeOfShipmentSerializer(instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PaymentStatusViewSet(viewsets.ModelViewSet):
    queryset = PaymentStatus.objects.all()
    serializer_class = PaymentStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query_set = self.queryset.filter(is_active=True)
        return query_set

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = PaymentStatusSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = PaymentStatusSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PaymentStatusSerializer(instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SpecialPackingViewSet(viewsets.ModelViewSet):
    queryset = SpecialPacking.objects.all()
    serializer_class = SpecialPackingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query_set = self.queryset.filter(is_active=True)
        return query_set

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = SpecialPackingSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = SpecialPackingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = SpecialPackingSerializer(instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExportPackingRequirementViewSet(viewsets.ModelViewSet):
    queryset = ExportPackingRequirement.objects.all()
    serializer_class = ExportPackingRequirementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query_set = self.queryset.filter(is_active=True)
        return query_set

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ExportPackingRequirementSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = ExportPackingRequirementSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ExportPackingRequirementSerializer(instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SpecialGSTRateViewSet(viewsets.ModelViewSet):
    queryset = SpecialGSTRate.objects.all()
    serializer_class = SpecialGSTRateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query_set = self.queryset.filter(is_active=True)
        return query_set

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = SpecialGSTRateSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = SpecialGSTRateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = SpecialGSTRateSerializer(instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
