from django.views import View
from common.http import AjaxJsonResponse, RequestBody, RequestGetParams
from components import request_decorator
from system.menu.services import MenuService


class MenuListView(View):

    def get(self, request):
        dict_value = RequestGetParams(request=request).get_data()
        res_datas = MenuService().menu_list(params=dict_value, user_id=request_decorator.user_id())
        return AjaxJsonResponse(data=res_datas)


class MenuTreeView(View):

    def get(self, request):
        dict_value = RequestGetParams(request=request).get_data()
        menu_service = MenuService()
        res_datas = menu_service.menu_list(params=dict_value, user_id=request_decorator.user_id())
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
        res_data = MenuService().update_menu(data, user_id=request_decorator.user_id(), user_name=request_decorator.username())
        return AjaxJsonResponse(data=res_data)

    def post(self, request):
        from_data = RequestBody(request).get_data()
        res_row = MenuService().add_menu(menu_dict=from_data, user_id=request_decorator.user_id(), user_name=request_decorator.username())
        return AjaxJsonResponse(data=res_row)
