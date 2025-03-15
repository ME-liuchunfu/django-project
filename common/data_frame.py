import logging

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, Page

logger = logging.getLogger(__name__)


class PageResult:
    """
    数据分页结果对象
    """

    def __init__(self, total: int = 0, code: int = 200, msg: str = 'success', datas: list = None):
        self.total: int = total
        if datas is None:
            datas = []
        self.rows: list = datas
        self.code: int = code
        self.msg: str = msg

    def set_data(self, datas: list = None):
        if datas is None:
            datas = []
        self.rows = datas

    def set_total(self, total: int):
        self.total = total

    def set_code(self, code: int):
        self.code = code

    def set_msg(self, msg: str):
        self.msg = msg

    def as_dict(self) -> dict:
        return {
            "code": self.code,
            "msg": self.msg,
            "total": self.total,
            "rows": self.rows
        }


class ParsePageResult:
    """
    数据分页器
    """

    def __init__(self, page_size: int = 10, cur_page: int = 1):
        self.page_size: int = page_size
        self.cur_page: int = cur_page
        self.convert_handler = None

    def set_page_size(self, page_size: int):
        self.page_size: int = page_size

    def set_cur_page(self, cur_page: int):
        self.cur_page: int = cur_page

    def set_convert_handler(self, convert_handler):
        self.convert_handler = convert_handler

    def page(self, data_query_set) -> PageResult:
        paginator = Paginator(data_query_set, self.page_size)
        try:
            # 根据页码获取对应的页面
            page_obj = paginator.get_page(self.cur_page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = None
        except Exception as e:
            page_obj = None
            logger.error(f'[分页处理异常]')
        data_list = self.__parse_handler(page_obj)
        return PageResult(total=paginator.count, datas=data_list)

    def __parse_handler(self, page_obj: Page) -> list:
        res_data_list = []
        if not page_obj:
            return res_data_list

        object_list = page_obj.object_list
        if not object_list or len(object_list) == 0:
            return res_data_list

        if self.convert_handler:
            for data in object_list:
                res_data_list.append(self.convert_handler(data))
        else:
            res_data_list = object_list

        return res_data_list

    def __call__(self, **kwargs) -> PageResult:
        for k, v in kwargs.items():
            if k in ['page_size', 'cur_page']:
                setattr(self, k, v)
        data_query_set = kwargs.get('data_query_set')
        return self.page(data_query_set)


def inject_page_params(req_dict: dict = None, parse_page: ParsePageResult = None):
    if req_dict is not None and parse_page is not None:
        page_num = req_dict.get("pageNum")
        if not page_num:
            page_num = req_dict.get("page_num")
        page_size = req_dict.get("pageSize")
        if not page_size:
            page_size = req_dict.get("page_size")
        parse_page.set_page_size(page_size)
        parse_page.set_cur_page(page_num)


def inject_sql_params_dict(req_dict: dict = None,
                           sql_param_dict: dict = None,
                           excloud_keys=None,
                           handler=None):
    """
    sql查询参数注入
    req_dict：request 参数
    sql_param_dict：sql参数结果
    excloud_keys: 排除字段
    handler：key 处理函数
    """
    if excloud_keys is None:
        excloud_keys = ['pageNum', 'page_num', 'pageSize', 'page_size']
    if req_dict is not None and sql_param_dict is not None:
        for k, v in req_dict.items():
            if k not in excloud_keys:
                if handler is not None:
                    cvt_key = handler(k)
                    sql_param_dict[cvt_key] = v
                else:
                    sql_param_dict[k] = v
