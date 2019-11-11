from codecs import open
from time import time, sleep
from sys import version

if version > '3':
    from configparser import ConfigParser
else:
    from ConfigParser import ConfigPapengcrser

from src.DataOperation.SlaveDb import SlaveDb
from src.slave import CONFIG_PATH, DBPATH
from src.slave.perf import total_perf, proc_perf


def client(dbpath):
    """
    记录性能数据，运行时长为RUNTIME，时间间隔为INTERVAL
    :return:
    """
    start_time = time()
    d = SlaveDb(dbpath)
    if RUNTIME <= 0:
        while True:
            record(d)
    while time() - start_time < RUNTIME:
        record(d)


def record(d):
    """
    记录性能数据操作
    :return:
    """
    d.insert_total(total_perf())
    if PROCESS:
        for i in PROCESS:
            d.insert_proc(proc_perf(i))
    sleep(INTERVAL)


if __name__ == '__main__':
    cfg = ConfigParser()
    cfg.read_file(open(CONFIG_PATH, "r", "utf-8-sig"))
    RUNTIME = cfg.getint('Setting', 'RUNTIME')
    INTERVAL = cfg.getint('Setting', 'INTERVAL')
    PROCESS = cfg.get('Setting', 'PROCESS').split(',')
    client(DBPATH)
