
from django.urls import path, include, re_path

from system.dict.views import DictDataType
from system.menu.views import MenuInfoView, MenuListView, MenuTreeView
from system.post.views import PostListView, PostInfoView
from system.role.views import RoleListView, RoleInfoView, RoleStatusView, RoleDataView
from system.views import LoginView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'), # 登录
    re_path('dict/data/type/(?P<dict_type>.*)$', DictDataType.as_view(), name='dict_type'), # 字典
    path('menu/list', MenuListView.as_view(), name='menu_list'), # 菜单列表
    path('menu/treeselect', MenuTreeView.as_view(), name='menu_tree'), # 菜单下拉树
    re_path('menu/(?P<menu_id>[0-9].*)$', MenuInfoView.as_view(), name='menu_info'), # 菜单信息 查询 & 删除
    path('menu', MenuInfoView.as_view(), name='menu_info_update'), # 菜单信息 修改
    path('menu', MenuInfoView.as_view(), name='menu_info_add'), # 菜单信息 新增

    # 岗位管理
    path('post/list', PostListView.as_view(), name='post_list'), # 岗位列表
    path('post/export', PostListView.as_view(), name='post_list_export'), # 岗位信息 导出
    path('post/<int:post_id>', PostInfoView.as_view(), name='post_info'), # 岗位列表 查询 & 删除
    path('post', PostInfoView.as_view(), name='post_info_add'), # 岗位信息 新增

    # 角色管理
    path('role/list', RoleListView.as_view(), name='role_list'), # 角色列表
    path('role/export', RoleListView.as_view(), name='role_list_export'), # 角色信息 导出
    path('role/changeStatus', RoleStatusView.as_view(), name='role_info_status'), # 角色信息 状态变更
    path('role/deptTree/<int:role_id>', RoleDataView.as_view(), name='role_info_data'), # 角色信息 数据
    path('role/<int:role_id>', RoleInfoView.as_view(), name='role_info'), # 角色列表 查询 & 删除
    path('role', RoleInfoView.as_view(), name='role_info_add'), # 角色信息 新增

]