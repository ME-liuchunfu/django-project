from django.views import View

from common.http import AjaxJsonResponse, RequestGetParams
from system.post.services import PostService


class PostListView(View):

    """
    岗位管理
    """

    def get(self, request):
        req_data = RequestGetParams(request).get_data()
        res_data = PostService().post_list(req_data).as_dict()
        return AjaxJsonResponse(extra_dict=res_data)