from common.http import AjaxJsonResponse


def json_page_not_found_view(request, exception):
    """
    404 not found
    :param request:
    :param exception:
    :return:
    """
    return AjaxJsonResponse(code=404, msg='资源未找到', status=404)