from flask_login import UserMixin
from werkzeug.security import check_password_hash

from app.helper import DbHelper
from config import Config


class User(UserMixin):
    """
    用户
    """
    __dbhelper = None
    __admin_user = None

    def __init__(self, user=None):
        self.__dbhelper = DbHelper()
        if user:
            self.id = user.get('id')
            self.username = user.get('name')
            self.password_hash = user.get('password')
            self.pris = user.get('pris')
        self.__admin_user = {
            "id": 0,
            "name": Config().get_config('app').get('login_user'),
            "password": Config().get_config('app').get('login_password')[6:],
            "pris": "我的媒体库,资源搜索,探索,站点管理,订阅管理,下载管理,媒体整理,服务,系统设置"
        }

    def verify_password(self, password):
        """
        验证密码
        """
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        """
        获取用户ID
        """
        return self.id

    def get(self, user_id):
        """
        根据用户ID获取用户实体，为 login_user 方法提供支持
        """
        if user_id is None:
            return None
        if self.__admin_user.get('id') == user_id:
            return User(self.__admin_user)
        for user in self.__dbhelper.get_users():
            if not user:
                continue
            if user.ID == user_id:
                return User({"id": user.ID, "name": user.NAME, "password": user.PASSWORD, "pris": user.PRIS})
        return None

    def get_user(self, user_name):
        """
        根据用户名获取用户对像
        """
        if self.__admin_user.get("name") == user_name:
            return User(self.__admin_user)
        for user in self.__dbhelper.get_users():
            if user.NAME == user_name:
                return User({"id": user.ID, "name": user.NAME, "password": user.PASSWORD, "pris": user.PRIS})
        return None

    def as_dict(self):
        pass

    def get_usermenus(self, ignore):
        pass

    def get_authsites(self):
        pass

    def get_services(self):
        pass

    def get_topmenus(self):
        pass

    def check_user(self, site, params):
        pass

    def get_users(self):
        pass

    def add_user(self, name, password, pris):
        pass

    def delete_user(self, name):
        pass

    def get_public_sites(self):
        pass

    def get_indexer(self,
                    url,
                    siteid=None,
                    cookie=None,
                    name=None,
                    rule=None,
                    public=None,
                    proxy=False,
                    parser=None,
                    ua=None,
                    render=None,
                    language=None,
                    pri=None):
        pass

    def get_brush_conf(self):
        pass
