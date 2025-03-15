
from django.urls import path, include, re_path

from system.dict.views import DictDataType
from system.menu.views import MenuInfoView, MenuListView
from system.post.views import PostListView
from system.views import LoginView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'), # 登录
    re_path('dict/data/type/(?P<dict_type>.*)$', DictDataType.as_view(), name='dict_type'), # 字典
    path('menu/list', MenuListView.as_view(), name='menu_list'), # 菜单列表
    re_path('menu/(?P<menu_id>[0-9].*)$', MenuInfoView.as_view(), name='menu_info'), # 菜单信息 查询 & 删除
    path('menu', MenuInfoView.as_view(), name='menu_info_update'), # 菜单信息 修改
    path('menu', MenuInfoView.as_view(), name='menu_info_add'), # 菜单信息 新增

    # 岗位管理
    path('post/list', PostListView.as_view(), name='post_list'), # 岗位列表

]