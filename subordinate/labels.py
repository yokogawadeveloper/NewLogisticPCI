from rest_framework import permissions
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from .serializers import *
import pandas as pd


# Create your views here.
class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = StateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = StateSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=False, url_path='import_state')
    def import_state(self, request):
        file = request.FILES['file']
        if file:
            df = pd.read_csv(file)
            df = df.where(pd.notnull(df), None)
            df['stateName'] = df['stateName'].str.strip()
            for index, row in df.iterrows():
                state = State.objects.filter(name=row['stateName']).first()
                if state:
                    state.name = row['stateName']
                    state.save()
                else:
                    State.objects.create(name=row['stateName'])
            return Response({'message': 'State imported successfully', 'status': status.HTTP_200_OK})


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = DistrictSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DistrictSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=False, url_path='import_district')
    def import_district(self, request):
        file = request.FILES['file']
        if file:
            df = pd.read_csv(file)
            df = df.where(pd.notnull(df), None)
            df['stateId_id'] = df['stateId_id'].fillna(0).astype(int)
            df['destinationName'] = df['destinationName'].str.strip()
            for index, row in df.iterrows():
                state = State.objects.filter(id=row['stateId_id']).first()
                if state:
                    district = District.objects.filter(name=row['destinationName']).first()
                    if district:
                        district.name = row['destinationName']
                        district.state = state
                        district.save()
                    else:
                        District.objects.create(name=row['destinationName'], state=state)
            return Response({'message': 'State imported successfully', 'status': status.HTTP_200_OK})


class TalukViewSet(viewsets.ModelViewSet):
    queryset = Taluk.objects.all()
    serializer_class = TalukSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = TalukSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = TalukSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=False, url_path='import_taluk')
    def import_taluk(self, request):
        try:
            with transaction.atomic():
                file = request.FILES['file']
                if file:
                    df = pd.read_csv(file)
                    df = df.where(pd.notnull(df), None)
                    df['destinationId_id'] = df['destinationId_id'].fillna(0).astype(int)
                    df['talukName'] = df['talukName'].str.strip()
                    for index, row in df.iterrows():
                        district = District.objects.filter(id=row['destinationId_id']).first()
                        if district:
                            taluk = Taluk.objects.filter(name=row['talukName']).first()
                            if taluk:
                                taluk.name = row['talukName']
                                taluk.district = district
                                taluk.save()
                            else:
                                Taluk.objects.create(name=row['talukName'], district=district)
                    return Response({'message': 'Taluk imported successfully', 'status': status.HTTP_200_OK})
        except Exception as e:
            return Response({'message': str(e), 'status': status.HTTP_400_BAD_REQUEST})


class PincodeViewSet(viewsets.ModelViewSet):
    queryset = Pincode.objects.all()
    serializer_class = PincodeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = PincodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PincodeSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=False, url_path='get_pincode')
    def get_pincode(self, request):
        pincode = request.data.get('pincode')
        pincode = Pincode.objects.filter(pincode=pincode)
        serializer = PincodeSerializer(pincode, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='import_pincode')
    def import_pincode(self, request):
        try:
            with transaction.atomic():
                file = request.FILES['file']
                if file:
                    df = pd.read_csv(file)
                    df = df.where(pd.notnull(df), None)
                    df['stateId_id'] = df['stateId_id'].fillna(0).astype(int)
                    df['destinationId_id'] = df['destinationId_id'].fillna(0).astype(int)
                    df['taluk_id_id'] = df['taluk_id_id'].fillna(0).astype(int)
                    df['pincodeNo'] = df['pincodeNo'].fillna(0).astype(int)
                    for index, row in df.iterrows():
                        state = State.objects.filter(id=row['stateId_id']).first()
                        district = District.objects.filter(id=row['destinationId_id']).first()
                        taluk = Taluk.objects.filter(id=row['taluk_id_id']).first()
                        if state and district and taluk:
                            pincode = Pincode.objects.filter(pincode=row['pincodeNo']).first()
                            if pincode:
                                pincode.pincode = row['pincodeNo']
                                pincode.state = state
                                pincode.district = district
                                pincode.taluk = taluk
                                pincode.save()
                            else:
                                Pincode.objects.create(pincode=row['pincodeNo'], state=state, district=district,
                                                       taluk=taluk)
                    return Response({'message': 'Pincode imported successfully', 'status': status.HTTP_200_OK})
        except Exception as e:
            return Response({'message': str(e), 'status': status.HTTP_400_BAD_REQUEST})
