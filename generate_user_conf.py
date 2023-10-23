import copy
import os.path
import pickle
import ruamel.yaml
from config import Config
from web.backend.user import User
from web.backend.user_proxy import UserProxy


def load_by_data_file():
    """
    从 dat 文件读取
    """
    with open(os.path.join(Config().get_inner_config_path(), "user_pri.dat"), 'rb') as f:
        return pickle.load(f)


def load_by_text_and_system():
    """
    从程序提取 + 手写数据（从旧版本-v2.9.1获得）
    """
    _user = User()
    # 获取内置管理员用户对象
    _admin_user_data = _user._User__admin_user
    _admin_user_data.pop('password')
    _admin_user = _user.get(_admin_user_data.get('id'))
    # 默认权限集
    _default_pris = _admin_user.get_topmenus()
    # 默认开放的用户菜单
    _default_user_menus = _admin_user.get_usermenus()
    # 默认开放的服务
    _default_services = _admin_user.get_services()
    # 默认授权等级
    _default_level = _admin_user.level
    # 默认是否开启搜索
    _default_search = _admin_user.search
    # 合作站点列表
    _auth_sites = _admin_user.get_authsites()
    for _siteName, _siteData in _auth_sites.items():
        _params = _siteData.get('params')
        for _paramKey, _paramData in _params.items():
            _encrypted = _paramData.get('encrypted')
            if _encrypted:
                _paramData['encrypted'] = 'a function'

    # 默认所有公共站点
    _default_public_sites = _admin_user.get_public_sites()

    _user_proxy = UserProxy(user=_admin_user)
    # 全部用户菜单
    _all_user_menus = _admin_user._User__userauth._WlI5bfacg2__usermenus
    # 全部服务
    _all_services = _admin_user._User__userauth._WlI5bfacg2__services

    # 全部权限集（顶层菜单显示顺序由此控制）
    _all_pris = [
        '我的媒体库',
        '资源搜索',
        '探索',
        '站点管理',
        '订阅管理',
        '下载管理',
        '媒体整理',
        '服务',
        '系统设置',
    ]
    # 判断所有顶层菜单是否都已知，如果出现新的菜单抛异常
    _top_menu_names = [_menu['name'] for _menu in _all_user_menus]
    for pri in _top_menu_names:
        assert pri in _all_pris
    # 判断是否所有已知服务都存在
    for pri in _all_pris:
        assert pri in _top_menu_names

    # 声明已知服务
    _known_services = [
        'rssdownload',
        'subscribe_search_all',
        'pttransfer',
        'sync',
        'blacklist',
        'rsshistory',
        'nametest',
        'ruletest',
        'nettest',
        'backup',
        'processes',
    ]
    # 判断所有服务是否都已知，如果出现新的未知的服务抛异常
    for service_id, _ in _all_services.items():
        assert service_id in _known_services
    # 判断是否所有已知服务都存在
    for service_id in _known_services:
        assert _all_services[service_id]

    # 菜单内容数据
    _all_menu_dict = read_menu(_all_user_menus)
    _default_menu_dict = read_menu(_default_user_menus)
    replace_list_in_menu(_all_user_menus, _default_menu_dict, _all_menu_dict)
    replace_list_in_menu(_default_user_menus,
                         _default_menu_dict,
                         _all_menu_dict,
                         True)
    clean_list_dict(_default_user_menus)
    clean_list_dict(_all_user_menus)

    # 授权等级
    _level = 999
    # 开启搜索
    _search = 1

    _public_sites = _admin_user._User__userauth._WlI5bfacg2__publicsites

    # Trackers列表
    _trackers = [
        "udp://tracker.opentrackr.org:1337/announce",
        "udp://9.rarbg.com:2810/announce",
        "udp://opentracker.i2p.rocks:6969/announce",
        "https://opentracker.i2p.rocks:443/announce",
        "udp://tracker.torrent.eu.org:451/announce",
        "udp://tracker1.bt.moack.co.kr:80/announce",
        "udp://tracker.pomf.se:80/announce",
        "udp://tracker.moeking.me:6969/announce",
        "udp://tracker.dler.org:6969/announce",
        "udp://p4p.arenabg.com:1337/announce",
        "udp://open.stealth.si:80/announce",
        "udp://movies.zsw.ca:6969/announce",
        "udp://ipv4.tracker.harry.lu:80/announce",
        "udp://explodie.org:6969/announce",
        "udp://exodus.desync.com:6969/announce",
        "https://tracker.nanoha.org:443/announce",
        "https://tracker.lilithraws.org:443/announce",
        "https://tr.burnabyhighstar.com:443/announce",
        "http://tracker.mywaifu.best:6969/announce",
        "http://bt.okmp3.ru:2710/announce"
    ]

    return {
        # 1. 全部菜单，放在最前面，用来形成 yaml 引用块
        'menus': _all_user_menus,

        # 2. 全部服务定义，放在最前面，用来形成 yaml 引用块
        'all_services': _all_services,

        # 认证站点定义
        'auth_sites': _auth_sites,

        # 默认管理员账户配置
        'default': {
            'level': _default_level,
            'search': _default_search,
            'pris': _default_pris,
            'menus': _default_user_menus,
            'services': _default_services,
            'public_sites': _default_public_sites,
        },
        # 默认管理员账户
        'admin_user': _admin_user_data,
        # 要修改的认证等级
        'level': _level,
        # 开启搜索
        'search': _search,
        # 要修改的默认管理员权限
        'pris': _all_pris,

        # 所有公共站点
        'public_sites': _public_sites,

        # Trackers列表
        'trackers': _trackers
    }


def replace_list_in_menu(menus: list, default_dict, all_dict, default=False):
    _index = 0
    while _index < len(menus):
        # 获取当前下标的菜单
        _menu = menus[_index]

        _menu_name = _menu.get('name')
        # 从默认菜单中获取菜单
        _default_dict = None
        if default_dict:
            _default_dict = default_dict.get(_menu_name)
        # 从全部菜单中获取菜单，根据名字获取，此处一定非空
        _dict = all_dict.get(_menu_name)

        # 获取子菜单，如果没有则无需后续判断，直接更新菜单数据
        _dict_menu = _dict.get('list_dict')
        if not _dict_menu:
            menus[_index] = _default_dict if _default_dict else _dict
            _index += 1
            continue

        # 优先选择默认菜单中的数据，但需要进行一些判断
        if not _default_dict:
            _curr_menu = _dict
            _default_menu = None
        # 判断默认菜单中的数据是否都已经在全部菜单的对象中声明了
        else:
            # 一定非空，如果为空，debug检查数据
            _default_menu = _default_dict.get('list_dict')
            _dict_keys = _dict_menu.keys()
            for _default_name, _ in _default_menu.items():
                # 断言，如果报错，需要编辑全部菜单的数据来添加未包含的菜单项
                assert _default_name in _dict_keys
            # 如果默认菜单的子菜单有缺失，使用全部菜单的数据
            if not default and len(_default_menu) < len(_dict_menu):
                _curr_menu = _dict
            else:
                _curr_menu = _default_dict
        # 替换当前下标的菜单数据为声明对象中的
        menus[_index] = _curr_menu

        # 递归调用处理子菜单
        replace_list_in_menu(_curr_menu.get('list'), _default_menu, _dict_menu)
        _index += 1


def read_menu(menus):
    _menu_dict = {}
    for _menu in copy.deepcopy(menus):
        _menu_name = _menu.get('name')
        _menu_dict[_menu_name] = _menu
        _sub_menus = _menu.get('list')
        if _sub_menus:
            _menu['list_dict'] = read_menu(_sub_menus)
    return _menu_dict


def clean_list_dict(menus):
    for _menu in menus:
        _dict = _menu.get('list_dict')
        if _dict:
            _menu.pop('list_dict')
            clean_list_dict(_menu.get('list'))


def write_yml_file(user_conf, file_name):
    _user_path = os.path.join(Config().get_inner_config_path(), "user_conf")
    if not os.path.exists(_user_path):
        os.makedirs(_user_path, mode=0o777, exist_ok=True)
    _user_file = os.path.join(_user_path, 'user-conf-to-diff.yml')

    if os.path.exists(_user_file):
        with open(_user_file, mode='r', encoding='utf-8') as f:
            _old_user = ruamel.yaml.YAML().load(f)
        if user_conf == _old_user:
            print('user_pri_conf 未改变')
        else:
            with open(_user_file, mode='w', encoding='utf-8') as f:
                ruamel.yaml.YAML().dump(user_conf, f)
            print('user_pri_conf 已修改: %s' % _user_file)
    else:
        with open(_user_file, mode='w', encoding='utf-8') as f:
            ruamel.yaml.YAML().dump(user_conf, f)
        print('user_pri_conf 已创建: %s' % _user_file)


if __name__ == "__main__":
    """
    用户菜单、权限相关
    """

    # 从程序提取 + 手写数据（从旧版本-v2.9.1获得）
    _user_conf = load_by_text_and_system()
    # 写入文件
    write_yml_file(_user_conf, 'user-conf-to-diff.yml')

    # 从 dat 文件读取
    # _user_conf = load_by_data_file()
    # 写入文件
    # write_yml_file(_user_conf, 'user-conf.yml')
