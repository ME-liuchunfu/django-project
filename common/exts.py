"""
异常
"""


class PermiError(Exception):
    """权限异常"""

    def __init__(self, msg):
        self.msg = msg
        self.code = 403
        super().__init__(self.msg)

    def __str__(self):
        return str(self.msg)
