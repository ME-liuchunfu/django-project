import logging
from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, Page
from django.db.models import QuerySet
from django.utils import timezone

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

    def page(self, data_query_set: QuerySet) -> PageResult:
        count = 0
        try:
            paginator = Paginator(object_list=data_query_set, per_page=self.page_size)
            count = paginator.count
            # 根据页码获取对应的页面
            page_obj = paginator.get_page(self.cur_page)
        except PageNotAnInteger:
            page_obj = None
        except EmptyPage:
            page_obj = None
        except Exception as e:
            page_obj = None
            logger.error(f'[分页处理异常]')
        data_list = self.__parse_handler(page_obj)
        return PageResult(total=count, datas=data_list)

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
                    if cvt_key:
                        sql_param_dict[cvt_key] = v
                else:
                    sql_param_dict[k] = v


def sql_date_parse(date_str: str, format_str: str = '%Y-%m-%d'):
    naive_datetime = datetime.strptime(date_str, format_str)
    # 为日期时间对象添加时区信息
    aware_datetime = timezone.make_aware(naive_datetime)
    return aware_datetime


def parse_sql_columns(req_dict: dict = None, sql_params_dict: dict = None, columns: dict = None):
    """
    设置 sql区间查询
    """
    if req_dict is not None and sql_params_dict is not None:
        if columns is None:
            columns = {
                'create_time': {
                    "convert": sql_date_parse,
                    "format": "%Y-%m-%d",
                    "val": ['params[begin_time]', 'params[end_time]']
                },
            }

        for k, v in columns.items():
            range_flag = False
            for item in v['val']:
                if item in req_dict:
                    range_flag = True
                    break
            if range_flag:
                sql_params_dict[f'{k}__range'] = (
                    v['convert'](req_dict.get(v['val'][0]), v.get("format")),
                    v['convert'](req_dict.get(v['val'][1]), v.get("format"))
                )


def get_model_fields_name(model) -> list[str]:
    """
    获取所有模型字段
    """
    all_columns = [field.name for field in model._meta.get_fields()]
    return all_columns


def del_not_model_key(params_dict: dict = None, all_columns: list = None):
    """
    删除非模型字段 key
    """
    if params_dict is not None and all_columns is not None:
        keys = set(params_dict.keys())
        for k in keys:
            if k not in all_columns:
                del params_dict[k]