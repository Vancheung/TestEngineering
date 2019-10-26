from sqlite3 import IntegrityError

from plotly import utils

from src.DataOperation.SlaveDb import SlaveDb
from src.DataOperation.sql_common import create_table_factory, \
    select_from_table, insert_factory, select_latest_from_table, \
    select_column_names, select_tables_name
from src.master import MASTER_SLAVE, SLAVE_PREFIX, SLAVE_SUFFIX_TOTAL, \
    SLAVE_SUFFIX_PROC, turn_timestamp_to_timestr
import plotly.graph_objs as go
from plotly.offline import iplot, plot


class MasterDb(SlaveDb):
    def init_table(self):
        # self.execute_sql(create_table_factory, 'master', MASTER_SLAVE)
        pass

    def select_latest(self):
        cursor = self.execute_sql(select_from_table, MASTER_SLAVE,
                                  time_column='LATEST_PULL_TIME',
                                  select_limit=1)
        return cursor.fetchone()[0]

    def create_slave(self, ip):
        total_tbl_name = SLAVE_PREFIX + ip.replace('.',
                                                   '_') + SLAVE_SUFFIX_TOTAL
        proc_tbl_name = SLAVE_PREFIX + ip.replace('.', '_') + SLAVE_SUFFIX_PROC
        self.execute_sql(create_table_factory, 'total', total_tbl_name)
        self.execute_sql(create_table_factory, 'proc', proc_tbl_name)

    def select_latest_in_slave(self, ip):
        """
        从slave节点数据表中查找最新的一条记录
        :param ip: slave节点的ip
        :return:
        """
        total_tbl_name = SLAVE_PREFIX + ip.replace('.',
                                                   '_') + SLAVE_SUFFIX_TOTAL
        try:
            cursor = self.execute_sql(select_latest_from_table, total_tbl_name)
            result = cursor.fetchone()
        except Exception:
            raise
        return 0 if not result else result[0]

    def insert_to_slave_total(self, ip, items: tuple):
        total_tbl_name = SLAVE_PREFIX + ip.replace('.',
                                                   '_') + SLAVE_SUFFIX_TOTAL
        try:
            self.execute_many_sql(items, insert_factory, 'total',
                                  total_tbl_name)
        except IntegrityError:
            pass

    def insert_to_slave_proc(self, ip, item=None):
        proc_tbl_name = SLAVE_PREFIX + ip.replace('.', '_') + SLAVE_SUFFIX_PROC
        self.execute_sql(insert_factory, 'proc', proc_tbl_name, item)

    def select_all_from_slave(self, ip, item):
        try:
            cursor1 = self.select_all_total(ip, item)

        except Exception:
            raise
        return cursor1.fetchall()  # , cursor2.fetchall()

    def select_all_total(self, ip, item):
        total_tbl_name = SLAVE_PREFIX + ip.replace('.',
                                                   '_') + SLAVE_SUFFIX_TOTAL
        return self.execute_sql(select_from_table, total_tbl_name, item=item,
                                select_limit=None)

    def select_all_proc(self, ip, item):
        proc_tbl_name = SLAVE_PREFIX + ip.replace('.',
                                                  '_') + SLAVE_SUFFIX_PROC
        return self.execute_sql(select_from_table, proc_tbl_name, item=item,
                                select_limit=None)

    def get_col_names(self, ip):
        """
        返回数据表中所有字段名（total表）
        :param ip:
        :return:
        """
        total_tbl_name = SLAVE_PREFIX + ip.replace('.',
                                                   '_') + SLAVE_SUFFIX_TOTAL
        result = self.execute_sql(select_column_names,
                                  total_tbl_name).fetchall()
        return [col[1] for col in result]

    def get_table_names(self):
        """
        返回数据库中所有表名
        :return:
        """
        try:
            result = self.execute_sql(select_tables_name).fetchall()
            return [col[0] for col in result]
        except Exception:
            raise

    def select_time(self, slave_ip):
        data = self.select_all_from_slave(slave_ip, 'TIME')
        return [turn_timestamp_to_timestr(i[0]) for i in data]

    def select_item(self, slave_ip, item):
        data = self.select_all_from_slave(slave_ip, item)
        return [i[0] for i in data]

    def draw(self, ip):
        """
        对外提供绘制图片的接口
        :param ip: slave节点的ip
        :return: json格式数据
        """
        x = self.select_time(ip)
        data = []
        items = ['CPU', 'MEMORY', 'DISK']
        for i in items:
            y = self.select_item(ip, i)
            trace = go.Scatter(
                x=x,
                y=y,
                mode='lines',
                name=i
            )
            data.append(trace)
        from json import dumps as json_dumps
        graphJSON = json_dumps(data, cls=utils.PlotlyJSONEncoder)

        return graphJSON
