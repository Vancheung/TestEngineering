# -*- coding: UTF-8 -*-

"""
-------------------------------------------------------------------------------
Describe: 日志模块
Created At: 2020-08-26,  14:58
Author: 
-------------------------------------------------------------------------------
"""

from os import path, getenv
from json import load
import logging.config


def setup_logging(default_path='logging.json', default_level=logging.INFO, env_key='LOG_CFG'):
    """
    logging 设置
    :param default_path: 
    :param default_level: 
    :param env_key: 
    :return: 
    """
    p = getenv(env_key, None) if getenv(env_key, None) else default_path
    if path.exists(p):
        with open(p, 'rt') as f:
            config = load(f)
        try:
            logging.config.dictConfig(config)
        except Exception:
            logging.basicConfig(level=default_level)
    else:
        logging.basicConfig(level=default_level)

    return logging.getLogger()
