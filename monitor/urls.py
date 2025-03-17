from django.urls import path

from monitor.logininfor.views import LogininforListView, LogininforInfoView
from monitor.operlog.views import OperLogListView, OperLogInfoView

urlpatterns = [
    # 操作日志记录
    path('operlog/list', OperLogListView.as_view(), name='operlog_list'), # 操作日志记录列表
    path('operlog/clean', OperLogListView.as_view(), name='operlog_list_clean'), # 清空操作日志记录列表
    path('operlog/export', OperLogListView.as_view(), name='operlog_list_export'), # 操作日志记录信息 导出
    path('operlog/<str:oper_ids>', OperLogInfoView.as_view(), name='operlog_info'), # 操作日志记录列表 查询 & 删除
    path('operlog', OperLogInfoView.as_view(), name='operlog_info_add'), # 操作日志记录 新增


    # 登录日志记录
    path('logininfor/list', LogininforListView.as_view(), name='logininfor_list'), # 登录日志记录列表
    path('logininfor/clean', LogininforListView.as_view(), name='logininfor_list_clean'), # 清空登录日志记录列表
    path('logininfor/export', LogininforListView.as_view(), name='logininfor_list_export'), # 登录日志记录信息 导出
    path('logininfor/<str:info_ids>', LogininforInfoView.as_view(), name='logininfor_info'), # 登录日志记录列表 查询 & 删除
    path('logininfor', LogininforInfoView.as_view(), name='logininfor_info_add'), # 登录日志记录 新增


]