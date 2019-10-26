from time import mktime, strptime, strftime, localtime

DBPATH = 'master.db'
CONFIG_PATH = 'config.ini'
MASTER_SLAVE = 'tbl_master_slave'
SLAVE_PREFIX = 'tbl_slave_'
SLAVE_SUFFIX_TOTAL = '_total'
SLAVE_SUFFIX_PROC = '_proc'
PULL_CYCLE = 1800  # 拉取数据的时间间隔


def turn_timestr_to_timestamp(x):
    return mktime(strptime(x, "%Y-%m-%d %H:%M:%S"))


def turn_timestamp_to_timestr(x: int):
    return strftime("%Y-%m-%d %H:%M:%S", localtime(x))


def get_ip_from_tbl_name(tbl):
    result = ''
    for i in tbl.split('_'):
        if i.isdigit():
            result += '.{}'.format(i)
    return result.lstrip('.')
