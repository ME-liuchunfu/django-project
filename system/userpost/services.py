import logging

from manage import settings
from system.models import SysUserPost

logger = logging.getLogger(settings.APP_LOGGER_NAME)


class UserPostService:

    def insert_user_post(self, user_id: int = None, post_ids: list | set | tuple = None):
        try:
            if user_id and post_ids:
                datas = []
                for post_id in post_ids:
                    datas.append({
                        'user_id': user_id,
                        'post_id': post_id
                    })
                datas = [SysUserPost(**data) for data in datas]
                SysUserPost.objects.bulk_create(datas)
        except Exception as e:
            logger.error(f'[新增用户岗位]异常, user_id={user_id}, post_ids={post_ids}', exc_info=True)

    def del_user_post(self, user_id: int = None):
        try:
            if user_id:
                SysUserPost.objects.filter(user_id=user_id).delete()
        except Exception as e:
            logger.error(f'[删除岗位信息]异常, user_id={user_id}', exc_info=True)

    def post_list_by_user_id(self, user_id: int = None) -> list:
        res_datas = []
        try:
            if user_id:
                query_set = SysUserPost.objects.filter(user_id=user_id).all()
                if query_set and len(query_set) > 0:
                    for data in query_set:
                        res_datas.append(data.post_id)
        except Exception as e:
            logger.error(f'[查询用户岗位信息]异常, user_id:{user_id}', exc_info=True)
        return res_datas