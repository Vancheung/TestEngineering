# -*- coding: UTF-8 -*-

"""
-------------------------------------------------------------------------------
Describe: 数据库模块
Created At: 2020-09-01,  10:20
Author: 
-------------------------------------------------------------------------------
"""
import sqlite3

import pymysql

from common.indicators import Indicators
from src import logger, BASEDIR


class DatabaseApi:
    """
    数据操作api接口，与具体的数据库种类解耦。调用时直接使用本模块提供的接口

    在进行数据库操作时，使用类似  c.execute('SELECT * FROM table_name WHERE symbol=?', t)  的执行格式，使用逗号传入可变参数
    而非百分号，可以有效避免sql注入风险。（但占位符不可用于替代列名或表名）
    """

    def __init__(self, db_type: str, db_name: str):
        logger.info(db_name)
        if 'sqlite' in db_type.lower():
            self.db_api = SqliteDb(db_name)
        # elif 'mysql' in db_type.lower():
        #     self.db_api = MysqlDb(db_name)
        else:
            logger.error('Wrong database type!')
            raise TypeError('Wrong database type!')

    def create_table(self):
        return self.db_api.create_table()

    def select_column(self, *args):
        if len(args) == 1 and args[0] == 'task_id':
            return self.db_api.select_task_ids()
        return self.db_api.select_one_column_by_task_id(*args)

    def insert_data(self, data: Indicators):
        return self.db_api.insert_perf_data(data)

    def get_tables_name(self):
        pass

    def get_columns_name(self):
        pass

    def select_tables_name(self):
        return self.db_api.select_tables_name()


class SqliteDb:
    """
    在Sqlite Database的实现
    """

    def __init__(self, db_name: str):
        try:
            self.conn = sqlite3.connect(db_name)
        except NameError:
            logger.error('No such database.'
                         ' You need to create database manually, try to execute "create database perf.db;"')
            return

    def execute(self, sql: str, *args):
        """
        执行sql语句
        :param sql:
        :param args: tuple传参，避免sql注入
        :return:
        """
        logger.debug((sql, args))
        c = self.conn.cursor()
        try:
            cursor = c.execute(sql, args) if args else c.execute(sql)
            self.conn.commit()
            return cursor
        except Exception as e:
            logger.error(e)

    def create_table(self):
        """
        创建数据表
        :return:
        """
        create_competitor_performance = '''CREATE TABLE competitor_performance(
                   id INTEGER PRIMARY KEY AUTOINCREMENT, -- '主键'
                   platform VARCHAR(100) NOT NULL DEFAULT 'iOS',
                   task_id VARCHAR(100) NOT NULL , -- '测试执行的任务ID'
                   app_name VARCHAR(100), --  'app_name',
                   cpu FLOAT DEFAULT 0, --  'app_cpu占比',
                   mem FLOAT DEFAULT 0, --  '内存使用',
                   fps FLOAT DEFAULT 0, --  'fps',         
                   gpu FLOAT DEFAULT 0, --  'gpu占比',
                   io_read FLOAT DEFAULT 0, --  'io读',
                   io_write FLOAT DEFAULT 0, --  'io写'
                   time datetime DEFAULT CURRENT_TIMESTAMP --  '插入时间'
                   );  -- ='性能结果统计' '''

        try:
            self.execute(create_competitor_performance)
        except Exception as e:
            logger.info(e)

    def select_task_ids(self):
        """
        获取所有task id
        :return:
        """
        sql = "select task_id from competitor_performance"
        return set([row[0] for row in self.execute(sql).fetchall()])

    def select_one_column_by_task_id(self, task_id, item):
        """
        根据task id筛选某一列数据，返回一个列表
        :param task_id:
        :param item:
        :return:
        """
        sql = "select %s from competitor_performance where task_id = '%s'" % (item, task_id)
        data = self.execute(sql)
        return [col[0] for col in data] if data else []

    def select_column_names(self, tbl_name):
        """
        获取表中所有列名
        :param tbl_name:
        :return:
        """
        sql = 'PRAGMA table_info ([%s]);' % tbl_name
        cursor = self.execute(sql)
        return_data = cursor.fetchall()
        return [d[1] for d in return_data]

    def select_tables_name(self):
        """
        获取表名
        :return:
        """
        cursor = self.execute('SELECT name FROM sqlite_master WHERE type="table";')
        return cursor.fetchall()

    def insert_perf_data(self, data: Indicators):
        """
        插入性能数据
        :param data: {task_id:"",apk_name:"",Indicators.values:*dict}
        :return:
        """
        sql = "insert into competitor_performance (task_id,app_name,cpu,mem,fps,gpu,io_read,io_write,time) " \
              "values (?,?,?,?,?,?,?,?,?)"
        self.execute(sql, data.task_id, data.values.get('app_name'),
                     data.values.get(Indicators.CPU), data.values.get(Indicators.MEM), data.values.get(Indicators.FPS),
                     data.values.get(Indicators.GPU), data.values.get(Indicators.IO_READ),
                     data.values.get(Indicators.IO_WRITE),
                     data.timestamp)

