# -*- coding: UTF-8 -*-

"""
-------------------------------------------------------------------------------
Describe: 配置模块
Created At: 2020-08-27,  14:35
Author: 
-------------------------------------------------------------------------------
"""
from os import path as os_path
from configparser import ConfigParser
from json import load
from typing import List

from common.indicators import DeviceInfo
from src import logger, BASEDIR


class ConfigApi:
    def __init__(self, config_path):
        self.cfg = ConfigParser()
        with open(config_path, "r", encoding='utf-8') as f:
            self.cfg.read_file(f)
        logger.info('Read devices info at {}：'.format(config_path))

    def get_dev_info(self) -> List[DeviceInfo]:
        """
        从配置文件中读取设备配置
        :return:
        """
        result = []
        for section in self.cfg.sections():
            if 'device' in section.lower():
                dev = DeviceInfo(self.cfg.get(section, 'PLATFORM_VERSION'),
                                 self.cfg.get(section, 'UDID'),
                                 section,
                                 self.cfg.get('Setting', 'BUNDLE_ID'),
                                 self.cfg.get('Setting', 'XCODE_ORG_ID'))
                result.append(dev)
        return result

    def get_runtime_info(self):
        """
        获取测试任务运行时间配置
        :return:
        """
        return self.cfg.getint('Setting', 'RUN_TIME')

    def get_process_name(self):
        """
        获取观察的APP名称
        :return:
        """
        return self.cfg.get('Setting', 'PROCESS')

    @staticmethod
    def get_params_info(json_path: List[str]) -> List[str]:
        """
        从一组配置文件中读取任务的参数配置(json格式文件）
        :return:
        """
        result = []
        for file in json_path:
            try:
                with open(file, 'r') as f:
                    cfg = f.read()
                    result.append(cfg)
            except FileNotFoundError:
                continue
        return result

    def get_rtmp_url(self):
        """
        获取推流地址
        :return:
        """
        return self.cfg.get('Setting', 'RTMP_URL')

    @staticmethod
    def get_case_operation(operation_path, case_id):
        """
        获取operation 配置文件
        :param operation_path:
        :param case_id:
        :return:
        """
        with open(operation_path, 'r') as f:
            operation = load(f)
            return operation.get(case_id)

    @staticmethod
    def get_case_operation_by_dev(operation_path, case_id, dev_id):
        """
        多设备场景，获取指定设备的operations
        :param operation_path:
        :param case_id:
        :param dev_id:
        :return:
        """
        with open(operation_path, 'r') as f:
            operation = load(f)
            return operation.get(case_id).get(dev_id)

