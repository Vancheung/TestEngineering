from sqlite3 import connect
from time import localtime, strftime

from src.slave import TOTAL_PERF, PROC_PERF, SELECT_LIMIT


class Db():
    def __init__(self, dbpath):
        self.conn = connect(dbpath)
        c = self.conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS ' + TOTAL_PERF +
                  '               (TIME TimeStamp PRIMARY KEY  NOT NULL DEFAULT CURRENT_TIMESTAMP,\n'
                  '               CPU           REAL    NOT NULL,\n'
                  '               MEMORY        REAL    NOT NULL,\n'
                  '               DISK          REAL    NOT NULL,\n'
                  '               DISK_IO_READ  INT     NOT NULL,      \n'
                  '               DISK_IO_WRITE INT     NOT NULL, \n'
                  '               NET_IO_RECV   INT     NOT NULL,\n'
                  '               NET_IO_SENT   INT     NOT NULL);')
        c.execute('CREATE TABLE IF NOT EXISTS ' + PROC_PERF +
                  '               (TIME INT PRIMARY KEY     NOT NULL,\n'
                  '               P_NAME        TEXT    NOT NULL,\n'
                  '               CPU           REAL    NOT NULL,\n'
                  '               MEMORY        REAL    NOT NULL);')
        print('Open database Successful...')

    def insert_total(self, item):
        """
        插入整机性能数据
        :param table:
        :param item:
        :return:
        """
        # self.init_table_total() if not self.is_table_exist(TOTAL_PERF) else None
        try:
            # print(item)
            c = self.conn.cursor()
            c.execute("INSERT INTO " + TOTAL_PERF + " (CPU,MEMORY,DISK,DISK_IO_READ, DISK_IO_WRITE,NET_IO_SENT, NET_IO_RECV) \
                    VALUES " + item)
            self.conn.commit()
        except Exception as e:
            raise e

    def insert_proc(self, item):
        """
        插入进程性能数据
        :param table:
        :param item:
        :return:
        """
        # self.init_table_proc() if not self.is_table_exist(PROC_PERF) else None
        try:
            # print(item)
            c = self.conn.cursor()
            c.execute("INSERT INTO " + PROC_PERF + " (NAME,CPU,MEMORY) \
                            VALUES " + item)
            self.conn.commit()
        except Exception as e:
            raise e

    def select(self, table, item=None, start_time=None, end_time=None):
        """
        获取整表数据
        :param start_time: datetime.utcnow().timestamp()
        :param end_time: datetime.utcnow().timestamp()
        :param table: 表名(str)
        :param item: 列名(str)
        :return:
        """
        c = self.conn.cursor()
        item = '*' if not item else item
        query = "SELECT * FROM " + table
        if start_time:
            stime = strftime("%Y-%m-%d %H:%M:%S", localtime(start_time))
            query += " WHERE time([time]) > time('" + stime + "')"
        if end_time:
            etime = strftime("%Y-%m-%d %H:%M:%S", localtime(end_time))
            query += " AND time([time]) < time('" + etime + "') "
        query += ' order by "TIME" DESC limit ' + str(SELECT_LIMIT)

        query = "SELECT " + item + ' FROM (' + query + ') order by "TIME" ASC'
        try:
            cursor = c.execute(query)
            self.conn.commit()
        except Exception as e:
            raise e
        return cursor.fetchall()
