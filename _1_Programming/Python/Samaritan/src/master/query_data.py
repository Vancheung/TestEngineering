from typing import Tuple
from requests import get, codes

from src.master import turn_timestr_to_timestamp


def pull_data(ip, start_time: float) -> tuple:
    """
    从slave节点拉取total数据
    :param ip: slave节点ip
    :param start_time:拉取数据的开始时间
    :return: 响应的message部分
    """
    url = 'http://{}:5000/data'.format(ip)
    params = {
        'start_time': start_time
    }
    try:
        r = get(url=url, params=params)
    except Exception:
        raise
    return tuple(
        r.json().get('message')) if r.status_code == codes.ok and r.json().get(
        'status') == 'success' else None


def pull_proc_data(ip, start_time: float) -> tuple:
    """
    从slave节点拉取proc数据
    :param ip: slave节点ip
    :param start_time:拉取数据的开始时间
    :return: 响应的message部分
    """
    url = 'http://{}:5000/procdata'.format(ip)
    params = {
        'start_time': start_time
    }
    try:
        r = get(url=url, params=params)
    except Exception:
        raise
    return tuple(
        r.json().get('message')) if r.status_code == codes.ok and r.json().get(
        'status') == 'success' else None


def insert_data(db, ip, data: Tuple):
    """
    向数据库中逐行插入数据
    :param db: 数据库
    :param ip: slave节点的ip
    :param data: 数据内容（需要为tuple格式）
    :return:
    """
    data = turn_data_to_tuple(data)
    db.insert_to_slave_total(ip, tuple(data))


def insert_proc_data(db, ip, data: Tuple):
    """
    向数据库中逐行插入数据
    :param db: 数据库
    :param ip: slave节点的ip
    :param data: 数据内容（需要为tuple格式）
    :return:
    """
    data = turn_data_to_tuple(data)
    db.insert_to_slave_proc(ip, tuple(data))


def turn_data_to_tuple(data):
    """
    对sqlite fetchall方法取到的数据进行格式化
    :param data:
    :return:
    """
    for one_row in data:
        one_row[0] = turn_timestr_to_timestamp(one_row[0])
    return (tuple(one_row) for one_row in data)
