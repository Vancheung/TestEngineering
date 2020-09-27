# -*- coding: UTF-8 -*-

"""
-------------------------------------------------------------------------------
Describe: 数据结构类
Created At: 2020-09-01,  10:20
Author: 
-------------------------------------------------------------------------------
"""

from src.common.time_utils import timestamp_now_10
from src import logger


class DeviceInfo:
    """
    设备数据结构
    """

    def __init__(self, platform_version, udid, device_name, bundle_id, xcode_org_id):
        self.session = {
            "platformName": "ios",
            "platformVersion": platform_version,
            "udid": udid,
            "deviceName": device_name,
            "automationName": "XCUITest",
            "bundleId": bundle_id,
            "xcodeOrgId": xcode_org_id,
            "xcodeSigningId": "iPhone Developer"
        }

    def __repr__(self):
        return str(self.session)


class TaskInfo:
    """
    任务数据结构
    """

    def __init__(self, task_type, app_name, batch):
        """

        :param task_type: 指定测试任务的场景
        :param app_name: 测试的app名称
        """
        # 在运行一个任务的时候已经指定了启动时间（int），最后一位为秒
        self.start_time, self.start_time_str = timestamp_now_10()
        # task_id作为数据库查询时的关键字，由任务id+任务启动时间+5位随机数组成
        self.task_id = '%s_%s_%s' % (task_type, self.start_time_str, batch)
        self.app_name = app_name

    def __repr__(self):
        return ','.join([self.start_time, self.task_id, self.app_name])


class Indicators:
    """
    性能数据结构
    """
    CPU = 'cpu'
    SYS_CPU = 'sys_cpu'
    MEM = 'mem'
    BATTERY = 'battery'
    TEMPERATURE = 'temperature'
    ENV_TEMP = "env_temperature"
    UP_BYTES = 'up_bytes'
    DOWN_BYTES = 'down_bytes'
    GPU = 'gpu'
    FPS = 'fps'
    IO_READ = 'io_read'
    IO_WRITE = 'io_write'

    def __init__(self, task_info: TaskInfo, timestamp: int, values: dict):
        self.task_id = task_info.task_id
        self.timestamp = task_info.start_time + timestamp
        self.values = values
        self.values.update({'app_name': task_info.app_name})

    def __eq__(self, other):
        """
        根据时间戳来比较是否为同一组数据
        :param other:
        :return:
        """
        if not isinstance(other, Indicators):
            logger.error('Wrong type of %s', type(other))
        return self.timestamp == other.timestamp

    def __lt__(self, other):
        if not isinstance(other, Indicators):
            logger.error('Wrong type of %s', type(other))
        return self.timestamp < other.timestamp

    def tolist(self):
        data_list = [{"timestamp": self.timestamp}]
        for k, v in self.values:
            data_list.append({k, v})
        return data_list

    def update(self, add_values: dict):
        """
        更新values内容
        :param add_values:
        :return:
        """
        self.values.update(add_values)

    def __repr__(self):
        return ','.join([self.task_id, str(self.timestamp), str(self.values)])


class ParamInfo:
    """
    参数配置模板文件
    """
    def __init__(self,**kwargs):
        # 默认配置
        self.params = kwargs

    def update(self, **kwargs):
        """
        修改自定义配置
        :param kwargs:
        :return:
        """
        for arg in kwargs:
            for key in self.params.keys():
                if self.params.get(key).get(arg) is not None:
                    self.params.get(key)[arg] = kwargs[arg]
           
