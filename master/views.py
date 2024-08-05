from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import *


# Create your views here.
class RoleMasterViewSet(viewsets.ModelViewSet):
    queryset = RoleMaster.objects.filter(is_active=True)
    serializer_class = RoleMasterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query_set = self.queryset.filter(is_active=True)
        return query_set

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = RoleMasterSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = RoleMasterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = RoleMasterSerializer(instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ModuleMasterViewSet(viewsets.ModelViewSet):
    queryset = ModuleMaster.objects.all()
    serializer_class = ModuleMasterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query_set = self.queryset.filter(is_active=True)
        return query_set

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ModuleMasterSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = ModuleMasterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ModuleMasterSerializer(instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=False, url_path='get_menu_for_role_id_based')
    def getMenuForRoleIDBased(self, request, *args, **kwargs):
        try:
            role_id = request.data['role_id']
            arr = []

            module_ids = UserRole.objects.filter(role_id_id=role_id, add_access=True, delete_access=True,
                                                 view_access=True, edit_access=True).values_list('module_id_id',
                                                                                                 flat=True)

            filter_list = self.get_queryset().filter(module_id__in=module_ids)
            root_ids = filter_list.values_list('root', flat=True).distinct()
            root_ids = list(map(int, root_ids))
            module_ids = filter_list.values_list('module_id', flat=True)
            filter_list = self.get_queryset().filter(module_id__in=root_ids).values().order_by('sort_no')
            for index, obj in enumerate(filter_list):
                l_module_id = obj['module_id']
                module_name = obj['module_name']
                module_slug = obj['module_slug']
                root = obj['root']
                m_color = obj['m_color']
                m_icon_name = obj['m_icon_name']
                m_link = obj['m_link']
                # for root module
                module_id = self.get_queryset().filter(root=obj['module_id']).filter(module_id__in=module_ids)
                modules_list = module_id.values('module_id', 'module_name', 'module_slug', 'root', 'm_color',
                                                'm_icon_name',
                                                'm_link').order_by('sort_no')

                arr.append({"module_id": l_module_id,
                            "module_name": module_name,
                            "module_slug": module_slug,
                            "root": root,
                            "m_color": m_color,
                            "m_icon_name": m_icon_name,
                            "m_link": m_link,
                            "root_module": modules_list})
            return Response(arr)
        except Exception as e:
            return Response(str(e))

    @action(methods=['post'], detail=False, url_path='get_root_list_for_role_id_based')
    def getRootListRoleIDBased(self, request):
        try:
            role_id = request.data['role_id']
            arr = []
            array = []
            filter_data = UserRole.objects.filter(role_id_id=role_id).values_list('user_id', flat=True)
            filter_data = UserRole.objects.filter(user_id__in=filter_data)
            serializer = UserRoleSerializer(filter_data, many=True, context={'request': request})
            serializer = serializer.data
            for index, obj in enumerate(serializer):
                module = self.get_queryset().filter(module_id=obj['module_id'])
                root_id = module.values('root')[0]['root']
                if "ROOT" in root_id:
                    module_name_root = ""
                else:
                    module_name_root = self.get_queryset().filter(module_id=int(root_id)).values('module_name')[0][
                        'module_name']
                # for root module
                module_name = module.values('module_name')[0]['module_name']
                module_slug = module.values('module_slug')[0]['module_slug']
                root = module.values('root')[0]['root']
                m_color = module.values('m_color')[0]['m_color']
                m_icon_name = module.values('m_icon_name')[0]['m_icon_name']
                m_link = module.values('m_link')[0]['m_link']
                # binding root module with child module
                arr.append({"module_id": obj['module_id'],
                            "module_name": module_name,
                            "module_slug": module_slug,
                            "root": root,
                            "m_color": m_color,
                            "m_icon_name": m_icon_name,
                            "m_link": m_link,
                            "root_module_name": module_name_root})
                # for child module
                for i in arr:
                    if obj['module_id'] == i['module_id']:
                        array.append(i)
                        obj['user_module'] = array
                    array = []
            return Response(serializer)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, url_path='get_root_list_without_role_id_based')
    def getRootListRoleWithoutIDBased(self, request):
        arr = []
        filter_list = self.get_queryset().filter(root="ROOT")
        module_ids = filter_list.values_list('module_id', flat=True)

        for index, id in enumerate(module_ids):
            module_id = self.get_queryset().filter(root=id)
            modules = module_id.values('module_id', 'module_name', 'module_slug', 'root', 'm_color', 'm_icon_name',
                                       'm_link')
            module = self.get_queryset().filter(module_id=id)
            module_name = module.values('module_name')[0]['module_name']
            module_slug = module.values('module_slug')[0]['module_slug']
            root = module.values('root')[0]['root']
            m_color = module.values('m_color')[0]['m_color']
            m_icon_name = module.values('m_icon_name')[0]['m_icon_name']
            m_link = module.values('m_link')[0]['m_link']

            arr.append({"module_id": id,
                        "module_name": module_name,
                        "module_slug": module_slug,
                        "root": root,
                        "m_color": m_color,
                        "m_icon_name": m_icon_name,
                        "m_link": m_link,
                        "root_module": modules
                        })
        return Response(arr)


class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query_set = self.queryset.filter(is_active=True)
        return query_set

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserRoleSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = UserRoleSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserRoleSerializer(instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=False, url_path='create_multi_user_role')
    def create_multi_user_role(self, request, *args, **kwargs):
        try:
            data = request.data
            UserRole.objects.filter(role_id_id=data['role_id']).delete()
            for i in data['module_details']:
                UserRole.objects.create(
                    role_id_id=data['role_id'],
                    module_id_id=i['id'],
                    add_access=i['add'],
                    delete_access=i['delete'],
                    view_access=i['view'],
                    edit_access=i['edit']
                )
            return Response({"message": "User Role Created Successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class UserAccessViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = UserAccess.objects.all()
    serializer_class = UserAccessSerializer

    def get_queryset(self):
        query_set = self.queryset.filter(is_active=True)
        return query_set

    def list(self, request, *args, **kwargs):
        query_set = self.get_queryset()
        serializer = self.serializer_class(query_set, many=True, context={'request': request})
        serializer_data = serializer.data
        return Response(serializer_data)

    def create(self, request, *args, **kwargs):
        data = request.data
        user_access = self.queryset.filter(role_id_id=data['role_id'], emp_id_id=data['emp_id'])
        if user_access.exists():
            return Response({"message": "User Access Already Exists"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = UserAccessSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                serializer_data = serializer.data
                return Response(serializer_data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserAccessSerializer(instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)