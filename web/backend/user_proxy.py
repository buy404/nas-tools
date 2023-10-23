from flask_login import UserMixin

from config import Config
from web.backend.user import User
from web.backend.indexer_helper import IndexerHelper

_user_conf = Config().user_conf
_user_pri = _user_conf.get('user_pri')


class UserProxy(UserMixin):

    _real_user = None

    id = None
    username = None
    admin = None
    level = None
    pris = None
    search = 0

    # is_active = None
    # is_anonymous = None
    # is_authenticated = None

    def __init__(self, user=None):
        if not user:
            self._real_user = User()
        else:
            self._real_user = user
            self.id = user.id
            self.username = user.username
            self.admin = user.admin
            if _user_pri.get('admin_user').get('id') == user.id:
                self.level = _user_pri.get('level')
                self.search = _user_pri.get('search')
                self.pris = ','.join(_user_pri.get('pris'))
            else:
                self.level = user.level
                self.search = user.search
                self.pris = user.pris

    def verify_password(self, password):
        """
        验证密码
        """
        return self._real_user.verify_password(password)

    def get_id(self):
        """
        获取用户ID
        """
        return self._real_user.get_id()

    def get(self, user_id):
        """
        根据用户ID获取用户实体，为 login_user 方法提供支持
        """
        user = self._real_user.get(user_id)
        if not user:
            return None
        return UserProxy(user)

    def get_user(self, user_name):
        """
        根据用户名获取用户对像
        """
        user = self._real_user.get_user(user_name)
        if not user:
            return None
        return UserProxy(user)

    def as_dict(self):
        return self._real_user.as_dict()

    def get_usermenus(self, ignore):
        """
        查询用户菜单
        """
        # return self._real_user.get_usermenus(ignore)
        _menus = _user_pri.get('menus')[:]
        _pris = self.get_topmenus()
        _index = 0
        while _index < len(_menus):
            if _menus[_index].get('name') not in _pris:
                _menus.pop(_index)
            else:
                _index += 1
        return _menus

    def get_authsites(self):
        """
        获取合作站点列表
        """
        return self._real_user.get_authsites()

    def get_services(self):
        """
        获取服务列表
        """
        # return self._real_user.get_services()
        return _user_pri.get('all_services')

    def get_topmenus(self):
        """
        用户管理页面查询可用权限列表
        """
        # return self._real_user.get_topmenus()
        return self.pris.split(',')

    def check_user(self, site, params):
        """
        用户认证
        """
        return User().check_user(site, params)
        # return True, '模拟认证成功'

    def get_users(self):
        """
        查询所有用户
        """
        return User().get_users()

    def add_user(self, name, password, pris):
        """
        添加用户
        """
        return User().add_user(name, password, pris)

    def delete_user(self, name):
        """
        删除用户
        """
        return User().delete_user(name)

    def get_public_sites(self):
        """
        获取所有公共站点
        """
        # return self._real_user.get_public_sites()
        return self._real_user._User__userauth._WlI5bfacg2__publicsites

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
        """
        获取单个索引器配置
        """
        return IndexerHelper().get_indexer(url,
                                           siteid,
                                           cookie,
                                           name,
                                           rule,
                                           public,
                                           proxy,
                                           parser,
                                           ua,
                                           render,
                                           language,
                                           pri)

    def get_brush_conf(self):
        """
        获取刷流配置（原 sites.dat 中 conf 部分，coonfig/grap_conf 下的内容）
        """
        # return self._real_user.get_brush_conf()
        return _user_conf.get('brush_conf')
