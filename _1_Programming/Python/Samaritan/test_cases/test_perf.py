# -*- coding: UTF-8 -*-

"""
-------------------------------------------------------------------------------
Describe: 手动执行性能测试
Created At: 2020-09-23,  21:28
Author: 
-------------------------------------------------------------------------------
"""

import unittest
from random import randint

from common.config_utils import ConfigApi
from common.db_utils import DatabaseApi
from common.indicators import TaskInfo
from perf.ios_performance import IosPerfCollector
from perf.view_data import record_avg
from test_cases import CONFIG_PATH, DB_PATH, REPORT_PATH


class TestCases(unittest.TestCase):
    """ pre steps """

    def setUp(self) -> None:
        self.cfg = ConfigApi(CONFIG_PATH)

    """ test cases """

    def test_manual(self):
        dev = self.cfg.get_dev_info()[0]
        run_time = self.cfg.get_runtime_info()
        process = self.cfg.get_process_name()
        db_api = DatabaseApi('sqlite', DB_PATH)
        db_api.create_table()  # 未初始化数据库则新建数据表
        batch = randint(10000, 99999)
        task = TaskInfo('case_999_手工测试', process, batch)

        # 启动性能数据获取
        ios_perf = IosPerfCollector(dev.session, task.start_time)
        ios_perf.start_instruments(run_time * 1000)
        ios_perf.decode_trace(task.app_name)
        data = ios_perf.analyse_data(task)

        for d in data:
            db_api.insert_data(d)

        record_avg(db_api, REPORT_PATH)

    """ after steps"""

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
