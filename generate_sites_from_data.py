import os.path
import pickle
import ruamel.yaml
from app.utils.path_utils import PathUtils
from config import Config
from web.backend.user import User


if __name__ == "__main__":
    # 站点配置 Start ###############################################
    _user = User()
    # 获取内置管理员用户对象
    _admin_user_data = _user._User__admin_user
    _admin_user_data.pop('password')
    _admin_user = _user.get(_admin_user_data.get('id'))

    # RSS_SITE_GRAP_CONF Start ###############################################
    _grap_path = os.path.join(Config().get_inner_config_path(), "grap_conf")
    if not os.path.exists(_grap_path):
        os.makedirs(_grap_path, mode=0o777, exist_ok=True)
    _grap_file = os.path.join(_grap_path, 'rss-site-grap-conf.yml')

    # 读取内置配置
    _grap_conf = _admin_user._User__userauth._WlI5bfacg2__brushconf

    if os.path.exists(_grap_file):
        with open(_grap_file, mode='r', encoding='utf-8') as f:
            _old_grap = ruamel.yaml.YAML().load(f)
        if _grap_conf == _old_grap:
            print('RSS_SITE_GRAP_CONF 未改变')
        else:
            with open(_grap_file, mode='w', encoding='utf-8') as f:
                ruamel.yaml.YAML().dump(_grap_conf, f)
            print('RSS_SITE_GRAP_CONF 已修改: %s' % _grap_file)
    else:
        with open(_grap_file, mode='w', encoding='utf-8') as f:
            ruamel.yaml.YAML().dump(_grap_conf, f)
        print('RSS_SITE_GRAP_CONF 已创建: %s' % _grap_file)
    # RSS_SITE_GRAP_CONF End ###############################################

    # 内置索引器 Start ###############################################
    _site_path = os.path.join(Config().get_inner_config_path(), "sites")
    if not os.path.exists(_site_path):
        os.makedirs(_site_path, mode=0o777, exist_ok=True)

    # bin 文件加密密钥
    _bin_encrypt_key = _admin_user._User__userauth._WlI5bfacg2__key
    # bin 文件解密方法
    _bin_decrypt_func = _admin_user._User__userauth._WlI5bfacg2__decrypt
    # user.sites.bin 文件
    _user_sites_bin_path = os.path.join(Config().get_root_path(), "web",
                                        "backend", "user.sites.bin")

    # 读取 user.sites.bin
    with open(_user_sites_bin_path, 'rb') as f:
        _user_sites_encrypted_str = f.read()
    # 调用内置解密方法解密为二进制数据
    _user_sites_decrypted_bytes = _bin_decrypt_func(
        data=_user_sites_encrypted_str, key=_bin_encrypt_key)
    # 加载二进制数据（反序列化）
    _indexers = pickle.loads(_user_sites_decrypted_bytes)

    for _site in _indexers.values():
        _cfg_file = os.path.join(_site_path, '%s.yml' % _site.get('id'))
        if os.path.exists(_cfg_file):
            with open(_cfg_file, mode='r', encoding='utf-8') as f:
                _old_site = ruamel.yaml.YAML().load(f)
            if _site == _old_site:
                print('%s 配置未改变' % _site.get('id'))
                continue
        with open(_cfg_file, mode='w', encoding='utf-8') as f:
            ruamel.yaml.YAML().dump(_site, f)
        print(_cfg_file)

    _cfg_files = PathUtils.get_dir_files(in_path=_site_path, exts=[".yml"])
    print(
        'sites.data 文件中共读取出 %d 项配置，在 sites 文件夹中当前有 %d 个文件' % (
            len(_indexers), len(_cfg_files)
        )
    )
    # 内置索引器 End ###############################################
    # 站点配置 End ###############################################
