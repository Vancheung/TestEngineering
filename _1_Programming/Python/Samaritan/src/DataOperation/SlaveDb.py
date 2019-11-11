from time import strftime, localtime

from src.slave import SELECT_LIMIT


def logging(func):
    """
    使用装饰器打印操作日志
    :param func:
    :return:
    """

    def wrapper(self, *args, **kwargs):
        print('Operation {}, at {}!'.format(func, strftime("%Y-%m-%d %H:%M:%S",
                                                           localtime())))
        return func(self, *args, **kwargs)

    return wrapper


def create_table_factory(tbl_type, tbl_name):
    """
    创建数据表的工厂函数
    :param tbl_type:数据表类型
    :param tbl_name:
    :return:
    """
    tbl_map = {
        'total': create_total_perf_table,
        'proc': create_proc_perf_table
        # 'master': create_master_slave_table
    }
    return tbl_map.get(tbl_type)(tbl_name)


def insert_factory(tbl_type, *args, **kwargs):
    """
    插入数据的工厂函数
    :param tbl_type:数据表类型
    :param args:
    :param kwargs:
    :return:
    """
    tbl_map = {
        'total': insert_to_total_perf,
        'proc': insert_to_proc_perf
    }
    return tbl_map.get(tbl_type)(*args, **kwargs)


@logging
def select_from_table(tbl_name, start_time=None, end_time=None, item=None,
                      time_column="TIME", select_limit=SELECT_LIMIT) -> str:
    """
    查询数据的函数（不需要区分数据表类型）
    :param time_column:
    :param select_limit:
    :param tbl_name:
    :param start_time:
    :param end_time:
    :param item:
    :return:
    """
    item = '*' if not item else item
    query = "SELECT * FROM {}".format(tbl_name)
    if start_time:
        query += " WHERE strftime('%s',[time]) > strftime('%s','{}')".format(
            strftime("%Y-%m-%d %H:%M:%S", localtime(float(start_time))))
    if end_time:
        query += " AND strftime('%s',[time]) < strftime('%s','{}')".format(
            strftime("%Y-%m-%d %H:%M:%S", localtime(float(end_time))))
    query += ' order by "TIME"'
    if select_limit:
        query += ' limit {}'.format(select_limit)
    return 'SELECT {}  FROM ( {} ) order by {}'.format(item, query,
                                                       time_column)


@logging
def select_oldest_from_table(tbl_name, time_column="TIME"):
    query = 'SELECT {} FROM {} order by {} limit 1;'.format(time_column,
                                                            tbl_name,
                                                            time_column)
    return query


@logging
def select_latest_from_table(tbl_name, time_column="TIME"):
    query = 'SELECT {} FROM {} order by {} DESC limit 1;'.format(
        time_column,
        tbl_name,
        time_column)
    return query


@logging
def create_total_perf_table(tbl_name) -> str:
    query = 'CREATE TABLE IF NOT EXISTS {}' \
            '(TIME TimeStamp PRIMARY KEY  NOT NULL DEFAULT CURRENT_TIMESTAMP,\n' \
            'CPU           REAL    NOT NULL,\n' \
            'MEMORY        REAL    NOT NULL,\n' \
            'DISK          REAL    ,\n' \
            'DISK_IO_READ  INT     ,      \n' \
            'DISK_IO_WRITE INT     , \n' \
            'NET_IO_RECV   INT     ,\n' \
            'NET_IO_SENT   INT     );'.format(tbl_name)
    return query


@logging
def create_proc_perf_table(tbl_name) -> str:
    return "CREATE TABLE IF NOT EXISTS {}" \
           "(TIME TimeStamp NOT NULL DEFAULT CURRENT_TIMESTAMP,\n" \
           "PID  INT,\n" \
           "USER       TEXT,\n" \
           "CPU        REAL    NOT NULL,\n" \
           "MEM        REAL    NOT NULL,\n" \
           "COMMAND    TEXT    NOT NULL);".format(tbl_name)


@logging
def insert_to_total_perf(tbl_name, item=None) -> str:
    if not item:
        return 'INSERT INTO {} VALUES (?,?,?,?,?,?,?,?)'.format(tbl_name)
    if len(item) == 3:
        return 'INSERT INTO {} (CPU,MEMORY,DISK) VALUES {}'.format(tbl_name,
                                                                   item) if \
            item[
                0] < 100 else 'INSERT INTO {} (TIME,CPU,MEMORY) VALUES {}'.format(
            tbl_name, item)
    if len(item) == 4:
        return 'INSERT INTO {} (TIME,CPU,MEMORY,DISK) VALUES {}'.format(
            tbl_name,
            item)
    if len(item) == 7:
        return 'INSERT INTO {}' \
               ' (CPU,MEMORY,DISK,DISK_IO_READ, DISK_IO_WRITE,NET_IO_SENT, NET_IO_RECV)' \
               ' VALUES {}'.format(tbl_name, item)
    if len(item) == 8:
        return 'INSERT INTO {}' \
               ' (TIME,CPU,MEMORY,DISK,DISK_IO_READ, DISK_IO_WRITE,NET_IO_SENT, NET_IO_RECV)' \
               ' VALUES {}'.format(tbl_name, item)


@logging
def insert_to_proc_perf(tbl_name, item=None, hasTIME=False) -> str:
    if not item:
        if hasTIME:
            return 'INSERT INTO {} (TIME,PID, USER, CPU, MEM, COMMAND) VALUES (?,?,?,?,?,?)'.format(
                tbl_name)
        return 'INSERT INTO {} (PID, USER, CPU, MEM, COMMAND) VALUES (?,?,?,?,?)'.format(
            tbl_name)
    if len(item) == 6:
        return 'INSERT INTO {} (TIME, PID, USER, CPU, MEM, COMMAND) VALUES {}'.format(
            tbl_name, tuple(item))


def select_tables_name():
    return 'SELECT name FROM sqlite_master WHERE type="table"'

@logging
def select_item_by_pid(tbl_name, pid, item):
    return 'SELECT {} FROM {} where "PID"={}'.format(item, tbl_name, pid)


@logging
def select_info_of_pid(tbl_name):
    return 'SELECT DISTINCT PID,COMMAND,USER FROM {} where PID in (SELECT PID from {} group by PID)'.format(
        tbl_name, tbl_name)
