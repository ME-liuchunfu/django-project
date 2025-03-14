from system.models import SysUser
from system.serializers.models import SysUserSerializer


class UserInfoDto:

    def __init__(self, user = None, roles: tuple[str] = tuple(), permissions: tuple[str] = tuple()):
        self.data = {}
        if not user:
            user = {}
        elif isinstance(user, SysUser):
            user = SysUserSerializer(user).data

        if isinstance(user, dict):
            if "username" in user and "userName" not in user:
                user['userName'] = user.get("username")
            if "user_id" in user and "userId" not in user:
                user['userId'] = user.get("user_id")

        self.data['user'] = user

        self.data['roles'] = roles
        self.data['permissions'] = permissions


    def __get__(self, key):
        return self.data.get(key)


    def get_data(self) -> dict:
        return self.data


    def __call__(self):
        return self.data


    def __str__(self):
        return self.data.__str__()
