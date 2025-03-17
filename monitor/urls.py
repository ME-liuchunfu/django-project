from django.urls import path

from monitor.operlog.views import OperLogListView, OperLogInfoView

urlpatterns = [
    # 操作日志记录
    path('logininfor/list', OperLogListView.as_view(), name='logininfor_list'), # 操作日志记录列表
    path('logininfor/export', OperLogListView.as_view(), name='logininfor_list_export'), # 操作日志记录信息 导出
    path('logininfor/<str:info_ids>', OperLogInfoView.as_view(), name='logininfor_info'), # 操作日志记录列表 查询 & 删除
    path('logininfor', OperLogInfoView.as_view(), name='logininfor_info_add'), # 操作日志记录 新增



]