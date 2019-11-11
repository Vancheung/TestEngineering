from sqlite3 import connect

from src.DataOperation.sql_common import select_from_table, \
    create_table_factory, insert_factory, select_oldest_from_table
from src.slave import TOTAL_PERF, PROC_PERF


class SlaveDb:
    def __init__(self, dbpath):
        self.conn = connect(dbpath)
        self.init_table()

    def init_table(self):
        self.execute_sql(create_table_factory, 'total', TOTAL_PERF)
        self.execute_sql(create_table_factory, 'proc', PROC_PERF)

    def insert_total(self, item):
        """
        插入整机性能数据
        :param item:
        :return:
        """
        self.execute_sql(insert_factory, 'total', TOTAL_PERF, item)

    def insert_proc(self, item):
        """
        插入进程性能数据
        :param item:
        :return:
        """
        if isinstance(item, list) or isinstance(item, tuple):
            self.execute_many_sql(item, insert_factory, 'proc', PROC_PERF)
        else:
            self.execute_sql(insert_factory, 'proc', PROC_PERF, item)

    def select(self, table, item=None, start_time=None, end_time=None):
        """
        获取整表数据
        :param start_time: datetime.utcnow().timestamp()
        :param end_time: datetime.utcnow().timestamp()
        :param table: 表名(str)
        :param item: 列名(str)
        :return:
        """
        if start_time == 0 or start_time=='0':
            # 传入start_time参数并且参数值为0
            # 只发生在该节点第一次被加入slave时
            cursor = self.execute_sql(select_oldest_from_table, table)
        else:
            cursor = self.execute_sql(select_from_table, table, start_time,
                                      end_time, item)
        return cursor.fetchall()

    def execute_sql(self, func, *args, **kwargs):
        """
        执行sql语句
        :param func: 对应 sql_common中的某一个函数
        :param args:
        :param kwargs:
        :return:
        """
        c = self.conn.cursor()
        query = func(*args, **kwargs)
        try:
            cursor = c.execute(query)
            self.conn.commit()
        except Exception:
            raise
        return cursor

    def execute_many_sql(self, data, func, *args, **kwargs):
        """
        一次执行多条语句（当前只应用于插入）
        :param data: 数据（tuple或list）
        :param func: 执行的查询语句
        :param args:
        :param kwargs:
        :return:
        """
        c = self.conn.cursor()
        query = func(*args, **kwargs)
        try:
            cursor = c.executemany(query, data)
            self.conn.commit()
        except Exception:
            raise
        return cursor

    def get_result_0(self, func, *args, **kwargs):
        """
        获取执行结果中第0列的内容（用于select 某一列）
        :param func:
        :param args:
        :param kwargs:
        :return: list
        """
        return [col[0] for col in
                self.execute_sql(func, *args, **kwargs).fetchall()]

    def get_result_1(self, func, *args, **kwargs):
        """
        获取执行结果中第0行第0列个元素（用于获取时间）
        :param func:
        :param args:
        :param kwargs:
        :return: one element
        """
        return self.execute_sql(func, *args, **kwargs).fetchone()[0]
