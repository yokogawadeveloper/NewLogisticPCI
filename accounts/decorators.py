from master.serializers import *
from master.models import *


def get_user_menu(role_id):
    try:
        arr = []
        module_ids = UserRole.objects.filter(role_id_id=role_id, add_access=True, delete_access=True,
                                             view_access=True, edit_access=True).values_list('module_id_id',
                                                                                             flat=True)

        filter_list = ModuleMaster.objects.filter(module_id__in=module_ids)
        root_ids = filter_list.values_list('root', flat=True).distinct()
        root_ids = list(map(int, root_ids))
        module_ids = filter_list.values_list('module_id', flat=True)
        filter_list = ModuleMaster.objects.filter(module_id__in=root_ids).values().order_by('sort_no')
        for index, obj in enumerate(filter_list):
            l_module_id = obj['module_id']
            module_name = obj['module_name']
            module_slug = obj['module_slug']
            root = obj['root']
            m_color = obj['m_color']
            m_icon_name = obj['m_icon_name']
            m_link = obj['m_link']
            # for root module
            module_id = ModuleMaster.objects.filter(root=obj['module_id']).filter(module_id__in=module_ids)
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
        return arr
    except Exception as e:
        return str(e)


def get_root_list(role_id):
    try:
        arr = []
        array = []
        filter_data = UserRole.objects.filter(role_id_id=role_id).values_list('user_id', flat=True)
        filter_data = UserRole.objects.filter(user_id__in=filter_data)
        serializer = UserRoleSerializer(filter_data, many=True)
        serializer = serializer.data

        for index, obj in enumerate(serializer):
            module = ModuleMaster.objects.filter(module_id=obj['module_id'])
            root_id = module.values('root')[0]['root']
            if "ROOT" in root_id:
                module_name_root = ""
            else:
                module_name_root = ModuleMaster.objects.filter(module_id=int(root_id)).values('module_name')[0][
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
                        "root_module_name": module_name_root
                        })

            # for child module
            for i in arr:
                if obj['module_id'] == i['module_id']:
                    array.append(i)
                    obj['user_module'] = array
                array = []
            return serializer

    except Exception as e:
        return str(e)
