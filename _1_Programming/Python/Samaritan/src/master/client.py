from configparser import ConfigParser
from datetime import datetime
from time import sleep

from src.DataOperation.MasterDb import MasterDb
from src.master import CONFIG_PATH, DBPATH, PULL_CYCLE, \
    turn_timestr_to_timestamp

from src.master.query_data import pull_data, insert_data


def read_config():
    """
    从配置信息中读取服务器ip列表
    :return:
    """
    cfg = ConfigParser()
    cfg.read_file(open(CONFIG_PATH, "r"))
    sections = cfg.sections()
    ip_list = []
    for section in sections:
        if 'server' in section.lower():
            ip_list.append(cfg.get(section, 'ip'))
    return ip_list


def client(db, ip_list):
    """
    作为master client的主程序，根据配置中的节点IP拉取节点数据，
    :param db: 数据库
    :param ip_list: ip列表
    :return:
    """
    for slave in ip_list:
        start_time = db.select_latest_in_slave(slave)
        now_time = datetime.utcnow().timestamp()
        if not start_time:
            data = pull_data(slave, start_time)
            start_time = turn_timestr_to_timestamp(data[0][0])
        while now_time - start_time > PULL_CYCLE:
            data = pull_data(slave, start_time)
            insert_data(db, slave, data)
            start_time = db.select_latest_in_slave(slave)


if __name__ == '__main__':
    d = MasterDb(DBPATH)
    while True:
        IP_LIST = read_config()  # 每次执行前先获取一次配置,可以通过修改配置文件实时更新slave
        [d.create_slave(slave) for slave in IP_LIST]
        client(d, IP_LIST)
        sleep(PULL_CYCLE)
