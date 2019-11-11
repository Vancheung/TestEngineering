from sqlite3 import IntegrityError

from plotly import utils

from src.DataOperation.SlaveDb import SlaveDb
from src.DataOperation.sql_common import create_table_factory, \
    select_from_table, insert_factory, select_latest_from_table, \
    select_tables_name, select_item_by_pid, select_info_of_pid
from src.master import SLAVE_PREFIX, SLAVE_SUFFIX_TOTAL, SLAVE_SUFFIX_PROC, \
    turn_timestamp_to_timestr
from plotly.graph_objects import Scatter


class MasterDb(SlaveDb):
    def init_table(self):
        pass

    def create_slave(self, ip):
        """
        根据slave的ip创建对应total和proc表
        :param ip:
        :return:
        """
        total_tbl_name = SLAVE_PREFIX + ip.replace('.',
                                                   '_') + SLAVE_SUFFIX_TOTAL
        proc_tbl_name = SLAVE_PREFIX + ip.replace('.', '_') + SLAVE_SUFFIX_PROC
        try:
            self.execute_sql(create_table_factory, 'total', total_tbl_name)
            self.execute_sql(create_table_factory, 'proc', proc_tbl_name)
        except Exception:
            raise

    def select_latest_in_slave(self, ip):
        """
        从slave节点数据表中查找最新的一条记录
        :param ip: slave节点的ip
        :return:
        """
        total_tbl_name = SLAVE_PREFIX + ip.replace('.',
                                                   '_') + SLAVE_SUFFIX_TOTAL
        try:
            return self.get_result_1(select_latest_from_table, total_tbl_name)
        except TypeError:
            return 0

    def insert_to_slave_total(self, ip, items: tuple):
        total_tbl_name = SLAVE_PREFIX + ip.replace('.',
                                                   '_') + SLAVE_SUFFIX_TOTAL
        try:
            self.execute_many_sql(items, insert_factory, 'total',
                                  total_tbl_name)
        except IntegrityError:
            pass

    def insert_to_slave_total_single(self, ip, item):
        total_tbl_name = SLAVE_PREFIX + ip.replace('.',
                                                   '_') + SLAVE_SUFFIX_TOTAL
        try:
            self.execute_sql(insert_factory, 'total',
                             total_tbl_name, item)
        except IntegrityError:
            pass

    def insert_to_slave_proc(self, ip, items: tuple, isSingle=False):
        proc_tbl_name = SLAVE_PREFIX + ip.replace('.', '_') + SLAVE_SUFFIX_PROC
        try:
            if isSingle:
                self.execute_sql(insert_factory, 'proc', proc_tbl_name, items)
            else:
                self.execute_many_sql(items, insert_factory, 'proc',
                                      proc_tbl_name, hasTIME=True)
        except IntegrityError:
            pass

    def insert_to_slave_proc_single(self, ip, item=None):
        proc_tbl_name = SLAVE_PREFIX + ip.replace('.', '_') + SLAVE_SUFFIX_PROC
        self.execute_sql(insert_factory, 'proc', proc_tbl_name, item)

    def get_table_names(self):
        """
        返回数据库中所有表名
        :return:
        """
        try:
            return self.get_result_0(select_tables_name)
        except Exception:
            raise

    def select_item(self, slave_ip, pid=None, item=None):
        """
        获取某一列的值
        :param slave_ip: slave节点ip
        :param pid: 为空则获取total表，否则获取proc表中对应pid
        :param item: 为空则获取全部元素
        :return: item为时间则转换为时间戳，其他原样返回为一个列表
        """
        tbl_name = '{}{}{}'.format(SLAVE_PREFIX, slave_ip.replace('.', '_'),
                                   SLAVE_SUFFIX_TOTAL if not pid else SLAVE_SUFFIX_PROC)
        try:
            data = self.get_result_0(select_item_by_pid, tbl_name, pid=pid,
                                     item=item) if pid else self.get_result_0(
                select_from_table, tbl_name, item=item, select_limit=None)
            return turn_timestamp_to_timestr(data) if item == 'TIME' else data
        except Exception:
            raise

    def get_pids_and_name(self, slave_ip):
        """
        获取proc表中所有的pid和对应的pname
        :param slave_ip: 节点ip
        :return: 所有pid：pname组成的字典
        """
        proc_tbl_name = SLAVE_PREFIX + slave_ip.replace('.',
                                                        '_') + SLAVE_SUFFIX_PROC
        try:
            return self.execute_sql(select_info_of_pid,
                                    proc_tbl_name).fetchall()
        except Exception:
            raise

    def draw(self, ip, pid=None):
        """
        对外提供绘制图片的接口
        :param pid: 指定绘制某个进程id（不指定则绘制整机）
        :param ip: slave节点的ip
        :return: json格式数据
        """
        x = self.select_item(ip, pid, item='TIME')
        items = ['CPU', 'MEM'] if pid else ['CPU', 'MEMORY', 'DISK']
        data = [
            Scatter(x=x, y=(self.select_item(ip, pid, item=i)), mode='lines',
                    name=i) for i in items]
        from json import dumps as json_dumps
        return json_dumps(data, cls=utils.PlotlyJSONEncoder)
