# -*- coding: UTF-8 -*-

"""
-------------------------------------------------------------------------------
Describe: 时间相关组件
Created At: 2020-08-25,  21:24
Author: 
-------------------------------------------------------------------------------
"""

from time import strftime, localtime, time


def time_now_stamp(time_format=None):
    """
    返回当前时间，未指定格式则默认返回 "年月日_时分秒"
    :param time_format:
    :return:
    """
    return strftime('%Y%m%d_%H%M%S', localtime(time())) if not time_format else strftime(time_format, localtime(time()))


def timestamp_now_10():
    """
    以秒为单位，返回当前时间
    :return:
    """
    now = time()
    return int(now), strftime('%Y%m%d_%H%M%S', localtime(time()))


if __name__ == '__main__':
    print(time_now_stamp())
    print(timestamp_now_10())
