import os
import yaml
from urllib.parse import quote
from .log_settings import logger


# cur_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
# env_path = os.path.join(cur_path, "env.yaml")
home_path = os.environ['HOME']
env_path = os.path.join(home_path, '.env', 'lrtest_env.yaml')


try:
    with open (env_path, 'r', encoding='utf-8') as f:
        config_data = yaml.load(f, Loader=yaml.FullLoader)
except:
    logger.error("load env.yaml fail!!!")


# 获取api_route_depends
def get_api_route_depends():
    try:
        api_route_depends = config_data["api_route_depends"]
        return api_route_depends
    except:
        logger.error('api_route_depends config error!!!')


# 获取database_url
def get_database_url():
    try:
        host = config_data["mysql"]["host"]
        port = config_data["mysql"]["port"]
        user = quote(config_data["mysql"]["user"])
        password = quote(config_data["mysql"]["password"])
        database = config_data["mysql"]["database"]
        return f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8'
    except:
        logger.error('mysql config error!!!')


# 获取七牛配置
def get_qiniu_config():
    try:
        bucket = config_data["qiniu"]["bucket"]
        access_key = config_data["qiniu"]["access_key"]
        secret_key = config_data["qiniu"]["secret_key"]
        callback_url = config_data["qiniu"]["callback_url"]
        external_link_base = config_data["qiniu"]["external_link_base"]
        return {
            "bucket": bucket,
            "access_key": access_key,
            "secret_key": secret_key,
            "callback_url": callback_url,
            "external_link_base": external_link_base
        }
    except:
        logger.error('qiniu config error!!!')