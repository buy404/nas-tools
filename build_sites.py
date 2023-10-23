import os.path
import pickle
import ruamel.yaml
from app.utils.path_utils import PathUtils
from config import Config
from web.backend.user import User


if __name__ == "__main__":
    _user = User()
    # 获取内置管理员用户对象
    _admin_user_data = _user._User__admin_user
    _admin_user_data.pop('password')
    _admin_user = _user.get(_admin_user_data.get('id'))

    # 内置索引器 Start ###############################################
    _indexers = {}
    _site_path = os.path.join(Config().get_inner_config_path(), "sites")
    _cfg_files = PathUtils.get_dir_files(in_path=_site_path, exts=[".yml"])
    for _cfg_file in _cfg_files:
        with open(_cfg_file, mode='r', encoding='utf-8') as f:
            print(_cfg_file)
            _site = ruamel.yaml.YAML().load(f)
            _indexers[_site.get('id')] = _site

    # bin 文件加密密钥
    _bin_encrypt_key = _admin_user._User__userauth._WlI5bfacg2__key
    # bin 文件加密方法
    _bin_encrypt_func = _admin_user._User__userauth._WlI5bfacg2__encrypt
    # user.sites.bin 文件
    _user_sites_bin_path = os.path.join(Config().get_root_path(), "web",
                                        "backend", "user.sites.bin")

    # 序列化为二进制数据
    _user_sites_decrypted_bytes = pickle.dumps(_indexers,
                                               pickle.HIGHEST_PROTOCOL)
    # 调用内置加密方法
    _user_sites_encrypted_str = _bin_encrypt_func(
        data=_user_sites_decrypted_bytes, key=_bin_encrypt_key)

    with open(_user_sites_bin_path, 'wb') as f:
        f.write(_user_sites_encrypted_str)
    # 内置索引器 End ###############################################

    # 用户菜单、权限相关 Start ###############################################
    _user_path = os.path.join(Config().get_inner_config_path(), "user_conf")
    _user_file = os.path.join(_user_path, 'user-conf.yml')
    with open(_user_file, mode='r', encoding='utf-8') as f:
        print(_user_file)
        _user_conf = ruamel.yaml.YAML().load(f)

    # RSS_SITE_GRAP_CONF Start ###############################################
    _grap_path = os.path.join(Config().get_inner_config_path(), "grap_conf")
    _grap_file = os.path.join(_grap_path, 'rss-site-grap-conf.yml')
    with open(_grap_file, mode='r', encoding='utf-8') as f:
        print(_grap_file)
        _grap_conf = ruamel.yaml.YAML().load(f)
    # RSS_SITE_GRAP_CONF End ###############################################

    with open(os.path.join(Config().get_inner_config_path(), "user_pri.dat"), 'wb') as f:
        pickle.dump({
            'user_pri': _user_conf,
            'brush_conf': _grap_conf
        }, f, pickle.HIGHEST_PROTOCOL)
    # 用户菜单、权限相关 End ###############################################
