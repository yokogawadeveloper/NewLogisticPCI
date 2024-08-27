from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Count
from rest_framework import permissions, status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F, Sum
from urllib.parse import urlparse
from .serializers import *
from .models import *
import random
import datetime
import os


# Create your views here.
class BoxTypeViewSet(viewsets.ModelViewSet):
    queryset = BoxType.objects.all()
    serializer_class = BoxTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query_set = self.queryset.filter(is_active=True)
        return query_set

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)
        return Response(serializer.data)


class BoxSizeViewSet(viewsets.ModelViewSet):
    queryset = BoxSize.objects.all()
    serializer_class = BoxSizeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query_set = self.queryset.filter(is_active=True)
        return query_set

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)
        return Response(serializer.data)


class BoxDetailViewSet(viewsets.ModelViewSet):
    queryset = BoxDetails.objects.all()
    serializer_class = BoxDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query_set = self.queryset.filter(is_active=True)
        return query_set

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False, url_path='create_box_details')
    def create_box_details(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                data = request.data
                random_code = random.randint(1000, 9999)
                count = [{'count': 1}]
                data['box_serial_no'] = count[0]['count']
                # check if the box is main box or not
                if self.get_queryset().filter(dil_id=data['dil_id']).exists():
                    count = self.get_queryset().filter(dil_id=data['dil_id'], main_box=True)
                    count = count.values('dil_id_id').annotate(count=Count('dil_id_id'))
                    # check if the box count is present
                    if not count.exists():
                        data['box_serial_no'] = 1
                    else:
                        data['box_serial_no'] += count[0]['count']
                # creating BoxDetails
                dil_id = DispatchInstruction.objects.filter(dil_id=data['dil_id']).first()
                box_size_id = BoxSize.objects.filter(box_size_id=data['box_size']).first()
                packing_price = PackingPrice.objects.filter(box_size_id=data['box_size']).first()
                price = packing_price.price if packing_price else 0
                create_data = {
                    'main_box': True,
                    'height': data['box_height'],
                    'length': data['box_length'],
                    'breadth': data['box_breadth'],
                    'panel_flag': data['panel_flag'],
                    'box_code': 'box-da_' + str(data['dil_id']) + '-' + str(random_code),
                    'parent_box': 'box-da_' + str(data['dil_id']) + '-' + str(random_code),
                    'box_serial_no': data['box_serial_no'],
                    'main_dil_no': data['dil_id'],
                    'status': 'packed',
                    'remarks': data['remarks'],
                    'gross_weight': data['gross_weight'],
                    'net_weight': data['net_weight'],
                    'qa_wetness': data['qa_wetness'],
                    'project_wetness': data['project_wetness'],
                    'box_price': price,
                }
                serializer = BoxDetailSerializer(data=create_data, context={'request': request})
                serializer.is_valid(raise_exception=True)
                serializer.save(created_by=request.user, dil_id=dil_id, box_size=box_size_id)
                # creating MasterItemList
                update_list = []
                dispatch = DispatchInstruction.objects.filter(dil_id=data['dil_id'])
                dispatch.update(dil_status="packing initiated", dil_status_no=10)
                # previous data
                for index, obj in enumerate(data['box_list']):
                    model_obj = BoxDetails.objects.get(box_details_id=obj['box_details_id'])
                    model_obj.parent_box = 'box-da_' + str(data['dil_id']) + '-' + str(random_code)
                    model_obj.status = 'packed'
                    update_list.append(model_obj)
                # update the BoxDetails
                BoxDetails.objects.bulk_update(update_list, ['parent_box', 'status', 'box_serial_no'])
                master_list = MasterItemList.objects.filter(dil_id=data['dil_id'], status_no__lte=4).count()
                if master_list == 0:
                    dispatch.update(
                        dil_status="Packed ,Ready For Load ",
                        dil_status_no=11, packed_flag=True,
                        packed_date=datetime.datetime.now()
                    )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            transaction.rollback()
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='filter_packed_box')
    def filter_packed_box(self, request, *args, **kwargs):
        data = request.data
        if data['main_box'] == 'ALL':
            filter_data = self.get_queryset()
        else:
            filter_data = self.get_queryset().filter(dil_id=data['dil_id'], main_box=data['main_box'],
                                                     status=data['status'])
        serializer = BoxDetailSerializer(filter_data, many=True, context={'request': request})
        serialize_data = serializer.data
        return Response({'data': serialize_data})

    @action(methods=['post'], detail=False, url_path='filter_packed_box_merged')
    def filter_packed_box_merged(self, request, *args, **kwargs):
        try:
            data = request.data
            if data['main_box'] == 'ALL':
                filter_data = self.get_queryset()
            elif data['status'] == "all":
                filter_data = self.get_queryset().filter(dil_id=data['dil_id'], main_box=data['main_box'])
            else:
                filter_data = self.get_queryset().filter(
                    dil_id=data['dil_id'],
                    main_box=data['main_box'],
                    status=data['status']
                )
            serializer = BoxDetailSerializer(filter_data, many=True, context={'request': request})
            serialize_data = serializer.data
            # filtering child box count
            for index, obj in enumerate(serialize_data):
                count = BoxDetails.objects.filter(parent_box=obj['box_code'])
                count = count.values('parent_box').annotate(count=Count('parent_box'))
                serialize_data[index]['box_count'] = count[0]['count']
            return Response({'data': serialize_data})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='box_details_code_filter')
    def box_details_code_filter(self, request, *args, **kwargs):
        try:
            data = request.data
            filter_data = BoxDetails.objects.filter(parent_box=data['box_code'], main_box=False).values_list('box_code',
                                                                                                             flat=True)
            box_data = BoxDetails.objects.filter(box_code__in=filter_data)
            item_packing_data = ItemPacking.objects.filter(box_code__in=filter_data)
            # serializer for box details
            box_serializer = BoxDetailSerializer(box_data, many=True, context={'request': request})
            box_serializer_data = box_serializer.data
            # serializer for item packing
            item_packing_serializer = ItemPackingSerializer(item_packing_data, many=True, context={'request': request})
            item_serializer_data = item_packing_serializer.data
            # for box details if box_item_flag
            new_box_details = BoxDetails.objects.filter(box_code=data['box_code'], box_item_flag=True).values_list(
                'box_code', flat=True)
            new_item_packing_data = ItemPacking.objects.filter(box_code__in=new_box_details)
            new_item_packing_serializer = ItemPackingSerializer(new_item_packing_data, many=True,
                                                                context={'request': request})
            for box in box_serializer_data:
                item_list = []
                for item in item_serializer_data:
                    if box['box_code'] == item['box_code']:
                        item_list.append(item)
                box['item_list'] = item_list
            return Response({
                'box_data': box_serializer_data,
                'new_item_packing': new_item_packing_serializer.data
            }, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='box_details_with_child')
    def box_details_with_child(self, request, *args, **kwargs):
        try:
            data = request.data
            filter_data = self.get_queryset().filter(parent_box=data['box_code'], main_box=False)
            serializer = BoxDetailSerializer(filter_data, many=True, context={'request': request})
            serialize_data = serializer.data
            return Response({'data': serialize_data})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='box_details_for_loading')
    def box_details_for_loading(self, request, *args, **kwargs):
        try:
            data = request.data
            filter_data = self.get_queryset().filter(dil_id=data['dil_id'], main_box=True, loaded_flag=False,
                                                     status='packed')
            serializer = BoxDetailSerializer(filter_data, many=True, context={'request': request})
            serialize_data = serializer.data
            return Response({'data': serialize_data})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='box_details_sum_of_boxes_weight')
    def box_details_sum_of_boxes_weight(self, request, *args, **kwargs):
        try:
            data = request.data
            dispatch_ids = data['dispatch_ids']
            box_details = self.get_queryset().filter(dil_id__in=dispatch_ids, main_box=True)
            no_of_boxes = len(box_details)
            net_weight = box_details.aggregate(Sum('net_weight'))['net_weight__sum']
            gross_weight = box_details.aggregate(Sum('gross_weight'))['gross_weight__sum']
            response_data = {
                'no_of_boxes': no_of_boxes,
                'net_weight': net_weight,
                'gross_weight': gross_weight,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False, url_path='box_summary_on_dil')
    def box_summary_on_dil(self, request, pk=None):
        try:
            dil_id = request.data['dil_id']
            box_details = BoxDetails.objects.filter(dil_id=dil_id, main_box=True)
            box_detail_count = BoxDetails.objects.filter(dil_id=dil_id, main_box=True).count()
            serializer = UnRelatedBoxDetailsSerializer(box_details, many=True)
            serialized_data = serializer.data
            # Add loop_count and box_detail_count to each item in the serialized data
            for loop_count, item in enumerate(serialized_data, start=1):
                item['loop_count'] = loop_count
                item['box_detail_count'] = box_detail_count
                item['length'] = int(item.pop('length', 0) or 0)
                item['breadth'] = int(item.pop('breadth', 0) or 0)
                item['height'] = int(item.pop('height', 0) or 0)
            return Response({'data': serialized_data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BoxDetailsFileViewSet(viewsets.ModelViewSet):
    queryset = BoxDetailsFile.objects.all()
    serializer_class = BoxDetailsFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='box_details_file_on_box_code')
    def box_details_file_on_box_code(self, request):
        try:
            data = request.data
            box_details_file = BoxDetailsFile.objects.filter(box_code=data['box_code'])
            serializer = BoxDetailsFileSerializer(box_details_file, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='create_multi_file_attachment')
    def create_multi_file_attachment(self, request, *args, **kwargs):
        try:
            for key, file in request.FILES.items():
                BoxDetailsFile.objects.create(
                    box_code=request.data['box_code'],
                    file=file,
                    created_by=request.user,
                    updated_by=request.user
                )
                return Response(
                    {'message': 'Box Details File uploaded successfully', 'status': status.HTTP_201_CREATED})
        except Exception as e:

            return Response({'message': str(e), 'status': status.HTTP_400_BAD_REQUEST})

    @action(methods=['post'], detail=False, url_path='download_file')
    def download_file(self, request):
        media_type = 'multipart/form-data'
        file_path = os.path.abspath('') + urlparse(request.data['url']).path
        file_pointer = open(file_path, 'rb')
        response = HttpResponse(file_pointer.read(), content_type=media_type)
        filename = os.path.basename(request.data['url'])
        response['Content-Disposition'] = 'attachment; filename=' + filename
        response['media_type'] = media_type
        return response


class ItemPackingViewSet(viewsets.ModelViewSet):
    queryset = ItemPacking.objects.all()
    serializer_class = ItemPackingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query_set = self.queryset.filter(is_active=True)
        return query_set

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)
        return Response(serializer.data)

    @action(methods=['post'], detail=False, url_path='create_multi_item_packing')
    def create_multi_item_packing(self, request, *args, **kwargs):
        try:
            update_list = []
            with transaction.atomic():
                data = request.data
                random_code = random.randint(1000, 9999)
                # check if the box is main box or not
                box_size = BoxSize.objects.filter(box_size_id=data['box_size']).first()
                dil = DispatchInstruction.objects.filter(dil_id=data['dil_id']).first()
                packing_price = PackingPrice.objects.filter(box_size_id=data['box_size']).first()
                price = packing_price.price if packing_price else 0
                if not dil:
                    return Response({'error': 'Invalid dispatch advice number'}, status=status.HTTP_400_BAD_REQUEST)
                if not box_size:
                    return Response({'error': 'Invalid box Size'}, status=status.HTTP_400_BAD_REQUEST)
                # # check if the box is main box or not
                if data['main_box'] is True:
                    parent_box = 'box-dil_' + str(data['dil_id']) + '-' + str(random_code)
                    stature = 'packed'
                    count = [{'count': 1}]
                    data['box_serial_no'] = count[0]['count']
                    # filter the da_no from the box details
                    if BoxDetails.objects.filter(dil_id=data['dil_id']).exists():
                        count = BoxDetails.objects.filter(dil_id=data['dil_id'], main_box=True)
                        count = count.values('dil_id_id').annotate(count=Count('dil_id_id'))
                        if not count.exists():
                            data['box_serial_no'] = 1
                        else:
                            data['box_serial_no'] += count[0]['count']

                    # Updating Boc Details
                    if data['box_item_flag'] is True:
                        for index, obj in enumerate(data['box_list']):
                            model_obj = BoxDetails.objects.get(box_details_id=obj['box_details_id'])
                            model_obj.parent_box = parent_box  # from main box
                            model_obj.status = 'packed'
                            model_obj.box_no_manual = obj['box_no_manual']

                            update_list.append(model_obj)
                        # update the BoxDetails
                        BoxDetails.objects.bulk_update(update_list, ['parent_box', 'status', 'box_no_manual'])

                else:
                    parent_box = None
                    stature = 'not_packed'
                    count = [{'count': 1}]
                    data['box_serial_no'] = count[0]['count']
                    # filter the da_no from the box details
                    if BoxDetails.objects.filter(dil_id=data['dil_id']).exists():
                        count = BoxDetails.objects.filter(dil_id=data['dil_id'], main_box=True)
                        count = count.values('dil_id_id').annotate(count=Count('dil_id_id'))
                        if not count.exists():
                            data['box_serial_no'] = 1
                        else:
                            data['box_serial_no'] += count[0]['count']

                # insert the BoxDetails
                BoxDetails.objects.create(
                    dil_id=dil,
                    box_size=box_size,
                    parent_box=parent_box,
                    box_code='box-dil_' + str(data['dil_id']) + '-' + str(random_code),
                    height=data['box_height'],
                    status=stature,
                    length=data['box_length'],
                    breadth=data['box_breadth'],
                    panel_flag=data['panel_flag'],
                    box_item_flag=data['box_item_flag'],
                    price=data['box_price'],
                    dil_id_id=data['dil_id'],
                    remarks=data['remarks'],
                    main_box=data['main_box'],
                    box_serial_no=data['box_serial_no'],
                    main_dil_no=data['dil_id'],
                    gross_weight=data['gross_weight'],
                    net_weight=data['net_weight'],
                    qa_wetness=data['qa_wetness'],
                    project_wetness=data['project_wetness'],
                    box_price=price,
                    created_by=request.user
                )
                # update the dispatch advice status
                dispatch = DispatchInstruction.objects.filter(dil_id=data['dil_id'])
                dispatch.update(dil_status="packing initiated", dil_status_no=10)
                # creating multiple Item Packing
                for obj in data['item_list']:
                    item_packing = ItemPacking.objects.create(
                        item_ref_id_id=obj['item_id'],
                        item_name=obj['material_description'],
                        item_qty=obj['entered_qty'],
                        is_parent=data['main_box'],
                        box_code='box-dil_' + str(data['dil_id']) + '-' + str(random_code),
                        remarks=obj['remarks'],
                        created_by_id=request.user.id,
                    )
                    for inline_items in obj['inline_items']:
                        serial_no = inline_items['serial_no']
                        tag_no = inline_items['tag_no']
                        box_no_manual = inline_items['box_count_no']
                        inline_item_list_id = inline_items.get('inline_item_id', None)
                        ItemPackingInline.objects.create(
                            box_no_manual=box_no_manual,
                            inline_item_list_id_id=inline_item_list_id,
                            item_pack_id=item_packing,
                            serial_no=serial_no,
                            tag_no=tag_no,
                            created_by_id=request.user.id
                        )
                        InlineItemList.objects.filter(inline_item_id=inline_item_list_id).update(packed_flag=True)
                # creating MasterItemList
                update_list = []
                for obj in data['item_list']:
                    item_obj = MasterItemList.objects.get(item_id=obj['item_id'])
                    item_obj.packed_quantity = obj['packed_qty'] + obj['entered_qty']
                    packed_qty = obj['packed_qty'] + obj['entered_qty']
                    if packed_qty == obj['quantity']:
                        item_obj.status = "packed"
                        item_obj.packing_flag = 4
                        item_obj.status_no = 5
                    # else:
                    #     item_obj.status = item_obj.status
                    #     item_obj.packing_flag = 3
                    # appending latest records
                    update_list.append(item_obj)
                MasterItemList.objects.bulk_update(update_list,
                                                   ['packed_quantity', 'status', 'packing_flag', 'status_no'])
                # update the dispatch advice status
                master_list = MasterItemList.objects.filter(dil_id=data['dil_id'], status_no__lte=4).count()
                if master_list == 0:
                    dispatch.update(
                        dil_status="Packed ,Ready For Load ",
                        dil_status_no=11, packed_flag=True,
                        packed_date=datetime.datetime.now()
                    )
                # return serializer data
                query_set = self.queryset.latest('item_packing_id')
                serializer = self.serializer_class(query_set, context={'request': request})
                serializer_data = serializer.data
                return Response({'item_packing': serializer_data, 'box_serial_no': data['box_serial_no']})
        except Exception as e:
            transaction.rollback()
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='item_packing_code_filter')
    def item_packing_code_filter(self, request, *args, **kwargs):
        try:
            data = request.data
            filter_data = self.get_queryset().filter(box_code=data['box_code'])
            serializer = self.serializer_class(filter_data, many=True, context={'request': request})
            serializer_data = serializer.data
            return Response({'data': serializer_data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='item_packing_progress')
    def item_packing_progress(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                request_data = request.data
                item_packing = ItemPacking.objects.filter(box_code=request_data['box_code'])
                for item in item_packing:
                    master_item_list = MasterItemList.objects.filter(item_id=item.item_ref_id_id)
                    master_item_list.update(packed_quantity=F('packed_quantity') - item.item_qty)
                    ItemPackingInline.objects.filter(item_pack_id=item.item_packing_id).delete()
                    ItemPacking.objects.filter(item_packing_id=item.item_packing_id).delete()
                BoxDetails.objects.filter(box_code=request_data['box_code']).delete()
                dispatch = DispatchInstruction.objects.filter(dil_id=request_data['dil_id'])
                dispatch.update(dil_status="packing in processed successfully", dil_status_no=10)
                return Response({'message': 'Item Packing Progressed'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='delete_on_box_code')
    def delete_on_box_code(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                data = request.data
                box_code = data['box_code']
                main_box = data['main_box']

                # Ensure BoxDetails exists
                if main_box:
                    box_code_list = BoxDetails.objects.filter(parent_box=box_code).values_list('box_code', flat=True)
                    box_detail_dil = BoxDetails.objects.filter(parent_box=box_code).first()  # only for dil
                else:
                    box_code_list = BoxDetails.objects.filter(box_code=box_code).values_list('box_code', flat=True)
                    box_detail_dil = BoxDetails.objects.filter(box_code=box_code).first()  # only for dil

                # Delete related ItemPackingInline records
                item_packing_ids = ItemPacking.objects.filter(box_code__in=box_code_list).values_list('item_packing_id',
                                                                                                      flat=True)
                item_packing_inline = ItemPackingInline.objects.filter(item_pack_id__in=item_packing_ids)
                inline_item_list_ids = item_packing_inline.values_list('inline_item_list_id', flat=True)
                InlineItemList.objects.filter(inline_item_id__in=inline_item_list_ids).update(packed_flag=False)

                # Delete ItemPacking records
                item_packing_inline.delete()
                BoxDetails.objects.filter(box_code__in=box_code_list).delete()

                # Update MasterItemList and DispatchInstruction statuses
                update_list = []
                for item_packing_id in item_packing_ids:
                    item_packing = ItemPacking.objects.get(item_packing_id=item_packing_id)
                    master_item_obj = MasterItemList.objects.get(item_id=item_packing.item_ref_id_id)
                    # update Master list
                    master_item_obj.packed_quantity = max(master_item_obj.packed_quantity - item_packing.item_qty, 0)
                    master_item_obj.item_status = "not_packed"
                    master_item_obj.item_status_no = 4
                    master_item_obj.packing_flag = 2
                    update_list.append(master_item_obj)
                # Update Master Item and ItemPacking
                MasterItemList.objects.bulk_update(update_list,
                                                   ['packed_quantity', 'item_status', 'packing_flag', 'item_status_no'])
                # ItemPacking.objects.filter(item_packing_id__in=item_packing_ids).delete()
                # Update dispatch status
                if box_detail_dil is not None:
                    dil_id = box_detail_dil.dil_id_id
                    DispatchInstruction.objects.filter(dil_id=dil_id).update(dil_status="Packing In Progress",
                                                                             dil_status_no=10, packed_flag=False)
                return Response({'success': 'Box details successfully deleted'}, status=200)
        except Exception as e:
            transaction.rollback()
            return Response({'error': str(e)}, status=400)

    @action(methods=['post'], detail=False, url_path='delete_on_item_packing')
    def delete_on_item_packing(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                data = request.data
                item_packing_id = data['item_packing_id']
                item_packing = ItemPacking.objects.filter(item_packing_id=item_packing_id)
                if not item_packing.exists():
                    return Response({'error': 'Item packing does not exist'}, status=status.HTTP_400_BAD_REQUEST)

                # Filter ItemPacking records
                item_packing_ids = item_packing.values_list('item_packing_id', flat=True)
                item_packing_inline = ItemPackingInline.objects.filter(item_pack_id__in=item_packing_ids)

                inline_item_list_ids = item_packing_inline.values_list('inline_item_list_id', flat=True)
                InlineItemList.objects.filter(inline_item_id__in=inline_item_list_ids).update(packed_flag=False)
                item_packing_inline.delete()
                # Update MasterItemList and DispatchInstruction statuses
                update_list = []
                item_packing_obj = ItemPacking.objects.filter(item_packing_id=item_packing_id).first()
                if item_packing_obj:
                    master_item_obj = MasterItemList.objects.get(item_id=item_packing_obj.item_ref_id_id)
                    dil_id = master_item_obj.dil_id.dil_id  # get dispatch id
                    master_item_obj.packed_quantity = max(master_item_obj.packed_quantity - 1, 0)
                    master_item_obj.item_status = "not_packed"
                    master_item_obj.item_status_no = 4
                    master_item_obj.packing_flag = 2
                    update_list.append(master_item_obj)
                    MasterItemList.objects.bulk_update(update_list, ['packed_quantity', 'item_status', 'packing_flag',
                                                                     'item_status_no'])
                    # Update dispatch status
                    DispatchInstruction.objects.filter(dil_id=dil_id).update(
                        dil_status="Packing In Progress",
                        dil_status_no=10, packed_flag=False
                    )
                # Update & Delete Item Packing
                if item_packing.exists():
                    item_packing_obj = item_packing.first()
                    if item_packing_obj.item_qty > 1:
                        item_packing.update(item_qty=F('item_qty') - 1)
                    else:
                        box_list = item_packing.values_list('box_code', flat=True)
                        if box_list.count() > 1:
                            BoxDetails.objects.filter(box_code__in=box_list).delete()
                        item_packing.delete()
                return Response({'success': 'packing details successfully deleted'}, status=status.HTTP_200_OK)

        except Exception as e:
            transaction.rollback()
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='delete_on_item_packing_inline')
    def delete_on_item_packing_inline(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                data = request.data
                item_packing_inline_id = data['item_packing_inline_id']
                # ItemPackingInline records
                item_packing_inline = ItemPackingInline.objects.filter(id=item_packing_inline_id)
                item_pack_id = item_packing_inline.values_list('item_pack_id', flat=True)
                inline_item_list_ids = item_packing_inline.values_list('inline_item_list_id', flat=True)
                InlineItemList.objects.filter(inline_item_id__in=inline_item_list_ids).update(packed_flag=False)
                item_packing_inline.delete()
                item_packing = ItemPacking.objects.filter(item_packing_id__in=item_pack_id)
                # Update MasterItemList and DispatchInstruction statuses
                update_list = []
                item_packing_obj = ItemPacking.objects.filter(item_packing_id__in=item_pack_id).first()
                if item_packing_obj:
                    item_obj = MasterItemList.objects.get(item_id=item_packing_obj.item_ref_id_id)
                    dil_id = item_obj.dil_id.dil_id  # Get dispatch id
                    item_obj.packed_quantity = max(item_obj.packed_quantity - 1, 0)
                    item_obj.item_status = "not_packed"
                    item_obj.item_status_no = 4
                    item_obj.packing_flag = 2
                    update_list.append(item_obj)
                    MasterItemList.objects.bulk_update(update_list, ['packed_quantity', 'item_status', 'packing_flag',
                                                                     'item_status_no'])
                    # Update dispatch status
                    DispatchInstruction.objects.filter(dil_id=dil_id).update(
                        dil_status="Packing In Progress",
                        dil_status_no=10, packed_flag=False
                    )
                # Updating & Deleting Item Packing
                if item_packing.exists():
                    item_packing_obj = item_packing.first()
                    if item_packing_obj.item_qty > 1:
                        item_packing.update(item_qty=F('item_qty') - 1)
                    else:
                        box_list = item_packing.values_list('box_code', flat=True)
                        if box_list.count() > 1:
                            BoxDetails.objects.filter(box_code__in=box_list).delete()
                        item_packing.delete()
                return Response({'success': 'packing details successfully deleted'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='add_item_to_box')
    def add_item_to_box(self, request, *args, **kwargs):
        try:
            data = request.data
            dispatch = DispatchInstruction.objects.filter(dil_id=data['dil_id'])
            for obj in data['item_list']:
                item_packing = ItemPacking.objects.create(
                    item_ref_id_id=obj['item_id'],
                    item_name=obj['material_description'],
                    item_qty=obj['entered_qty'],
                    is_parent=data['main_box'],
                    box_code=data['box_code'],
                    remarks=obj['remarks'],
                    created_by_id=request.user.id,
                )
                for inline_items in obj['inline_items']:
                    serial_no = inline_items['serial_no']
                    tag_no = inline_items['tag_no']
                    inline_item_list_id = inline_items['inline_item_id']
                    ItemPackingInline.objects.create(
                        inline_item_list_id_id=inline_item_list_id,
                        item_pack_id=item_packing,
                        serial_no=serial_no,
                        tag_no=tag_no,
                        box_no_manual=1,
                        created_by_id=request.user.id,
                        updated_by_id=request.user.id,
                    )
                    InlineItemList.objects.filter(inline_item_id=inline_item_list_id).update(packed_flag=True)
            # creating MasterItemList
            update_list = []
            for obj in data['item_list']:
                item_obj = MasterItemList.objects.get(item_id=obj['item_id'])
                item_obj.packed_quantity = obj['packed_qty'] + obj['entered_qty']
                packed_qty = obj['packed_qty'] + obj['entered_qty']
                if packed_qty == obj['quantity']:
                    item_obj.status = "packed"
                    item_obj.packing_flag = 4
                    item_obj.status_no = 5
                # appending latest records
                update_list.append(item_obj)
            MasterItemList.objects.bulk_update(update_list, ['packed_quantity', 'status', 'packing_flag', 'status_no'])
            # update the dispatch advice status
            master_list = MasterItemList.objects.filter(dil_id=data['dil_id'], status_no__lte=4).count()
            if master_list == 0:
                dispatch.update(
                    dil_status="Packed ,Ready For Load ",
                    dil_status_no=11, packed_flag=True,
                    packed_date=datetime.datetime.now()
                )
            # return serializer data
            query_set = self.queryset.latest('item_packing_id')
            serializer = self.serializer_class(query_set, context={'request': request})
            serializer_data = serializer.data
            return Response({'item_packing': serializer_data})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='add_box_into_box')
    def add_box_into_box(self, request, *args, **kwargs):
        try:
            data = request.data
            box_list = data['box_list']
            box_code = data['box_code']
            for box in box_list:
                box_details = BoxDetails.objects.filter(box_details_id=box["box_details_id"])
                box_details.update(parent_box=box_code, main_box=False)
            return Response({'message': 'Box code updated Successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
