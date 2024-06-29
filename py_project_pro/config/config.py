# -*- coding: utf8 -*-


import platform


class ProdConfig(object):
    """
    开发环境配置信息
    """

    MYSQL_INFO = {
        "host": "127.0.0.1",
        "user": "wzd",
        "password": "993926Dd",
        "port": 3306,
        "database": "order_info",
        "pool_size": 20,
        "wait_timeout": 80,
    }





def get_config():
    return ProdConfig

