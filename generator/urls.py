from django.urls import path

from generator.gen.views import GenViewList, GenDbList

urlpatterns = [
    # gen 列表
    path('list', GenViewList.as_view(), name='gen_list'), # gen列表
    path('db/list', GenDbList.as_view(), name='gen_db_list'), # gen db列表
    path('importTable', GenViewList.as_view(), name='gen_import'), # gen导入列表
]