# -*- coding: UTF-8 -*-

"""
-------------------------------------------------------------------------------
Describe: 使用instruments监控iOS的性能数据
Created At: 2020-08-25,  21:03
Author: 
-------------------------------------------------------------------------------
"""
import threading
from os import path as os_path
from subprocess import Popen, PIPE, STDOUT
from time import sleep
from typing import List

from common.indicators import Indicators, TaskInfo
from src import logger, BASEDIR
from test_cases import SCREENSHOT_PATH

TRACE_TEMPLATE = os_path.join(BASEDIR, "trace_template/PerformanceTemplate.tracetemplate")


class IosPerfCollector:
    def __init__(self, dev_info: dict, start_time):
        self.device = dev_info
        self.save_path = os_path.join(BASEDIR, r"test_results/%s" % start_time)

    def start_instruments(self, run_time):
        """
        启动Instruments
        :return:
        """
        logger.info(BASEDIR)
        cmd = "instruments -t %s -w %s -l %s -D %s" % (
            TRACE_TEMPLATE, self.device.get("udid"), run_time, self.save_path + '.trace')
        logger.info(cmd)
        logger.info('Collecting %s begin......' % self.device.get("udid"))
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
        for line in p.stdout.readlines():
            logger.info(line.decode('utf-8'))
        p.wait()
        p.stdout.close()
        logger.info('Collecting %s end......' % self.device.get("udid"))

    def decode_trace(self, app_name):
        """
        解析trace文件，写入到文件
        :return:
        """
        cmd = '%s %s %s %s' % (
            os_path.join(BASEDIR, 'src/perf/TraceDecoder'), self.save_path + '.trace', self.save_path + '.txt',
            app_name)
        logger.info(cmd)
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
        for line in p.stdout.readlines():
            logger.debug(line.decode('utf-8'))
        p.wait()
        p.stdout.close()

    @staticmethod
    def to_mb(perf) -> float:
        """
        数据单位为kib或gib，统一转换到mb
        :param perf: eg: 190 Mib
        :return:
        """
        data_value, data_type = perf.split(' ')
        if 'k' in data_type.lower():
            return float(data_value) / 1024.0
        elif 'g' in data_type.lower():
            return float(data_value) * 1024.0
        elif 'm' in data_type.lower():
            return float(data_value)
        logger.error('Wrong data type [%s]', data_type)

    @staticmethod
    def time_to_second(time_value) -> int:
        """
        时间转换为秒数
        :param time_value: mm:ss.xxx.xxx
        :return:
        """
        try:
            return int(time_value.split(':')[0]) * 60 + int(time_value.split(':')[1].split('.')[0])
        except Exception:
            logger.error('Wrong time format')
            raise

    @staticmethod
    def merge_data_by_time(list_cpus: List[Indicators], list_gpus: List[Indicators]) -> List[Indicators]:
        """
        合并两个记录列表（暂时不用）
        :param list_cpus: 记录cpu/mem/io数据的列表
        :param list_gpus: 记录gpu/fps的列表
        :return:
        """
        i, j = 0, 0
        while i < len(list_cpus) and j < len(list_gpus):
            if list_cpus[i] == list_gpus[j]:
                list_cpus[i].update(list_gpus[j].values)
                i += 1
                j += 1
                continue
            elif list_cpus[i] < list_gpus[j]:
                i += 1
                continue
            else:
                list_cpus.insert(i, list_gpus[j])
                j += 1
                continue

        return list_cpus

    def analyse_data(self, task_info: TaskInfo, src_name=None) -> List[Indicators]:
        """
        分析数据
        :param task_info: 调用任务的信息，包括一个task_id(在外部生成，对于同一个任务的一组记录来说，具有唯一性)和start_time(启动时间)
        :param src_name: 传入srcname则使用传入的值（调试使用）
        :return: 返回一个列表
        """
        data = []
        if not src_name:
            src_name = self.save_path + '.txt'
        logger.info('Analyze file %s', src_name)
        with open(src_name, 'r') as file:
            lines = file.readlines()
            max_retry_time = 5
            retry = 0
            while retry < max_retry_time:
                try:
                    for line in lines:
                        if task_info.app_name in line:
                            times, values = self.decode_cpus(line)
                        elif 'GPU' in line:
                            times, values = self.decode_gpus(line)
                        else:
                            continue
                        ind = Indicators(task_info, times, values)
                        data.append(ind)
                    break
                except ValueError:
                    retry += 1
                    logger.error('Retry %s time ,file name = %s', retry, src_name)
                    continue
        if not data and retry >= max_retry_time:
            logger.error('Analyse file [%s] fail.', src_name)
            raise ValueError
        return data

    def decode_gpus(self, line: str) -> (int, dict):
        """
        GPU FPS 类型的行数据解析
        :param line:
        :return:
        """
        performances = line.split()
        try:
            times = self.time_to_second(performances[0])
        except ValueError:
            times = 0
        values = {
            "fps": float(performances[1]) if performances[1].strip('%').isdigit() else 0,
            "gpu": float(performances[3].strip('%')) if performances[3].strip('%') != 'n/a' else 0
        }
        return times, values

    def decode_cpus(self, line: str) -> (int, dict):
        """
        CPU MEM IO类型的行数据解析
        :param line:
        :return:
        """
        performances = line.split(',')
        try:
            times = self.time_to_second(performances[0])
        except ValueError:
            times = 0
        values = {
            "io_read": self.to_mb(performances[-3]),
            "io_write": self.to_mb(performances[-4]),
            "mem": self.to_mb(performances[10]),
            "cpu": float(performances[6].strip('%')) if performances[6] != 'n/a' else 0
        }
        return times, values


class IosPerfThread(threading.Thread):
    """
    使用多线程方式运行
    """
    def __init__(self, appium, param, operation, ios_perf: IosPerfCollector, task, run_time):
        threading.Thread.__init__(self)
        self.appium = appium
        self.param = param
        self.op = operation
        self.ios_perf = ios_perf
        self.task = task
        self.run_time = run_time

    def run(self):
        """
        执行性能测试的线程
        :return:
        """
        self.appium.operate(self.op, self.param)
        self.appium.screen_shot(SCREENSHOT_PATH + self.task.task_id + '.png')

        sleep(30)
        logger.info("Starting Thread at %s" % self.task.task_id)
        self.ios_perf.start_instruments(self.run_time)
        logger.info("End Thread at %s" % self.task.task_id)
        try:
            self.appium.quit()
        except Exception as e:
            logger.info(e)
