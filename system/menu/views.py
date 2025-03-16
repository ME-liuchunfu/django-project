from django.http import QueryDict
from django.views import View

from common.http import AjaxJsonResponse, ParseRequestMetaUser, ParseJson, RequestBody, RequestGetParams
from system.menu.services import MenuService


class MenuListView(View):

    def get(self, request):
        dict_value = RequestGetParams(request=request).get_data()
        user_id = ParseRequestMetaUser(request).get_userid()
        res_datas = MenuService().menu_list(params=dict_value, user_id=user_id)
        return AjaxJsonResponse(data=res_datas)



class MenuTreeView(View):

    def get(self, request):
        dict_value = RequestGetParams(request=request).get_data()
        user_id = ParseRequestMetaUser(request).get_userid()
        menu_service = MenuService()
        res_datas = menu_service.menu_list(params=dict_value, user_id=user_id)
        res_datas = menu_service.build_menu_treeselect(res_datas)
        return AjaxJsonResponse(data=res_datas)



class MenuInfoView(View):

    def get(self, request, menu_id):
        res_data = MenuService().menu(menu_id=menu_id)
        return AjaxJsonResponse(data=res_data)

    def delete(self, request, menu_id):
        res_data = MenuService().del_menu(menu_id=menu_id)
        return AjaxJsonResponse(data=res_data)


    def put(self, request):
        data = RequestBody(request).get_data()
        user = ParseRequestMetaUser(request)
        user_id = user.get_userid()
        user_name = user.get_username()
        res_data = MenuService().update_menu(data, user_id=user_id, user_name=user_name)
        return AjaxJsonResponse(data=res_data)


    def post(self, request):
        from_data = RequestBody(request).get_data()
        user = ParseRequestMetaUser(request)
        user_id = user.get_userid()
        user_name = user.get_username()
        res_row = MenuService().add_menu(menu_dict=from_data, user_id=user_id, user_name=user_name)
        return AjaxJsonResponse(data=res_row)