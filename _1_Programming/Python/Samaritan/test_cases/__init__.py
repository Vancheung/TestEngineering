# -*- coding: UTF-8 -*-

"""
-------------------------------------------------------------------------------
Describe: 用例公共配置
Created At: 2020-09-23,  20:46
Author: 
-------------------------------------------------------------------------------
"""
from os import path as os_path
from src import BASEDIR

DB_PATH = os_path.join(BASEDIR, 'perf.db')
CONFIG_PATH = os_path.join(BASEDIR, 'test_cases/device.ini')
REPORT_PATH = os_path.join(BASEDIR, 'test_results/perf_result.csv')
SCREENSHOT_PATH = os_path.join(BASEDIR, 'test_results/screen_shot/')
