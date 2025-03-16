
from django.urls import path, include, re_path

from system.config.views import ConfigListView, ConfigInfoView
from system.dict.views import DictDataType
from system.menu.views import MenuInfoView, MenuListView, MenuTreeView
from system.post.views import PostListView, PostInfoView
from system.role.views import RoleListView, RoleInfoView, RoleStatusView, RoleDataView
from system.dept.views import DeptListView, DeptInfoView, DeptExcludeView
from system.views import LoginView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'), # 登录
    re_path('dict/data/type/(?P<dict_type>.*)$', DictDataType.as_view(), name='dict_type'), # 字典
    path('menu/list', MenuListView.as_view(), name='menu_list'), # 菜单列表
    path('menu/treeselect', MenuTreeView.as_view(), name='menu_tree'), # 菜单下拉树
    re_path('menu/(?P<menu_id>[0-9].*)$', MenuInfoView.as_view(), name='menu_info'), # 菜单信息 查询 & 删除
    path('menu', MenuInfoView.as_view(), name='menu_info_update'), # 菜单信息 修改

    # 岗位管理
    path('post/list', PostListView.as_view(), name='post_list'), # 岗位列表
    path('post/export', PostListView.as_view(), name='post_list_export'), # 岗位信息 导出
    path('post/<str:post_ids>', PostInfoView.as_view(), name='post_info'), # 岗位列表 查询 & 删除
    path('post', PostInfoView.as_view(), name='post_info_add'), # 岗位信息 新增

    # 角色管理
    path('role/list', RoleListView.as_view(), name='role_list'), # 角色列表
    path('role/export', RoleListView.as_view(), name='role_list_export'), # 角色信息 导出
    path('role/changeStatus', RoleStatusView.as_view(), name='role_info_status'), # 角色信息 状态变更
    path('role/deptTree/<int:role_id>', RoleDataView.as_view(), name='role_info_data'), # 角色信息 数据
    path('role/<str:role_ids>', RoleInfoView.as_view(), name='role_info'), # 角色列表 查询 & 删除
    path('role', RoleInfoView.as_view(), name='role_info_add'), # 角色信息 新增

    # 部门管理
    path('dept/list', DeptListView.as_view(), name='post_list'), # 部门列表
    path('dept/list/exclude/<int:dept_id>', DeptExcludeView.as_view(), name='post_list_exclude'), # 查询部门列表（排除节点）
    path('dept/export', DeptListView.as_view(), name='post_list_export'), # 部门信息 导出
    path('dept/<int:post_id>', DeptInfoView.as_view(), name='post_info'), # 部门列表 查询 & 删除
    path('dept', DeptInfoView.as_view(), name='post_info_add'), # 部门信息 新增


    # 参数设置
    path('config/list', ConfigListView.as_view(), name='config_list'), # 参数设置列表
    path('config/refreshCache', ConfigListView.as_view(), name='config_list_refreshCache'), # 参数设置列表 刷新缓存
    path('config/export', ConfigListView.as_view(), name='config_list_export'), # 参数设置信息 导出
    path('config/<str:config_ids>', ConfigInfoView.as_view(), name='config_info'), # 参数设置列表 查询 & 删除
    path('config', ConfigInfoView.as_view(), name='config_info_add'), # 参数设置 新增

]