# routers.py
"""
数据库路由
"""


class DatabaseRouter:
    """根据模型所在应用路由到不同数据库"""

    route_app_labels = {
        'system': 'config',  # system 应用的模型使用 config 数据库
        'monitor': 'default',  # monitor 应用的模型使用 default 数据库
    }

    default_db = "default"

    def db_for_read(self, model, **hints):
        """读操作路由"""
        if model._meta.app_label in self.route_app_labels:
            return self.route_app_labels[model._meta.app_label]
        return DatabaseRouter.default_db

    def db_for_write(self, model, **hints):
        """写操作路由"""
        if model._meta.app_label in self.route_app_labels:
            return self.route_app_labels[model._meta.app_label]
        return DatabaseRouter.default_db

    def allow_relation(self, obj1, obj2, **hints):
        """允许同一应用内的跨库关联"""
        app_label1 = obj1._meta.app_label
        app_label2 = obj2._meta.app_label

        if app_label1 == app_label2:
            return True
        elif app_label1 in self.route_app_labels or app_label2 in self.route_app_labels:
            return False
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """控制迁移命令的执行数据库"""
        if app_label in self.route_app_labels:
            return db == self.route_app_labels[app_label]
        return db == DatabaseRouter.default_db