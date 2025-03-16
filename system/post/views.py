from django.views import View

from common.http import AjaxJsonResponse, RequestGetParams, ParseRequestMetaUser, RequestBody, RequestPostParams
from system.post.services import PostService


class PostListView(View):

    """
    岗位管理
    """

    def get(self, request):
        req_data = RequestGetParams(request).get_data()
        res_data = PostService().post_list(req_data).as_dict()
        return AjaxJsonResponse(extra_dict=res_data)

    def post(self, request):
        req_data = RequestPostParams(request).get_data()
        response = PostService().export_post(req_data)
        return response


class PostInfoView(View):
    """
    岗位信息
    """

    def get(self, request, post_ids):
        res_data = PostService().post_info(post_id=int(post_ids))
        return AjaxJsonResponse(data=res_data)

    def delete(self, request, post_ids):
        post_ids = [ int(v) for v in post_ids.split(',') ]
        res_data = PostService().del_post(post_ids=post_ids)
        return AjaxJsonResponse(data=res_data)

    def post(self, request):
        user = ParseRequestMetaUser(request)
        req_dict= RequestBody(request).get_data()
        user_id = user.get_userid()
        user_name = user.get_username()
        res_data = PostService().add_post(user_id=user_id, user_name=user_name, req_dict=req_dict)
        return AjaxJsonResponse(data=res_data, code=200 if res_data > 0 else 500)

    def put(self, request):
        user = ParseRequestMetaUser(request)
        req_dict = RequestBody(request).get_data()
        user_id = user.get_userid()
        user_name = user.get_username()
        res_data = PostService().update_post(user_id=user_id, user_name=user_name, post=req_dict)
        return AjaxJsonResponse(data=res_data, code=200 if res_data > 0 else 500)