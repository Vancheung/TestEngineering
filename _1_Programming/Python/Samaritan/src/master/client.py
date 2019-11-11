from collections import namedtuple
from configparser import ConfigParser
from datetime import datetime
from os import listdir, path as os_path
from time import sleep

from src.DataOperation.MasterDb import MasterDb
from src.master import CONFIG_PATH, DBPATH, PULL_CYCLE, \
    turn_timestr_to_timestamp
from src.master.file2db import LinuxRecord

from src.master.query_data import pull_data, insert_data
from logging import basicConfig, DEBUG, debug

from src.master.sftp import SFTP


# basicConfig(level=DEBUG)


class Client:
    def __init__(self, config_path):
        self.cfg = ConfigParser()
        self.cfg.read_file(open(config_path, "r", encoding='utf-8'))
        debug('Read config at {}'.format(config_path))

    def get_win_slave(self):
        """
        从配置信息中读取服务器ip列表
        :return:
        """
        debug('Get windows slave info')
        return [self.cfg.get(section, 'ip') for section in self.cfg.sections()
                if 'server' in section.lower() and self.cfg.get(section,
                                                                'type') == 'windows']

    def get_linux_slave(self):
        debug('Get Linux slave info')
        result = []
        Slave = namedtuple('Slave', ['slave_ip', 'slave_user', 'slave_pwd'])
        for section in self.cfg.sections():
            if 'server' in section.lower() and self.cfg.get(section,
                                                            'type') == 'linux':
                slave = Slave(slave_ip=self.cfg.get(section, 'ip'),
                              slave_user=self.cfg.get(section, 'user'),
                              slave_pwd=self.cfg.get(section, 'pwd'))
                result.append(slave)
        return result

    def get_local_save_path(self):
        debug('Get save path info')
        return self.cfg.get('Setting', 'linux_filepath')

    def get_check_file(self):
        debug('Get file check.sh path')
        return self.cfg.get('Setting', 'check_filepath')

    def get_process_list(self):
        debug('Get file check.sh path')
        return self.cfg.get('Setting', 'PROCESS').split(',')


def get_win_data(db, ip_list):
    """
    根据配置中的节点IP拉取windows节点数据
    :param db: 数据库
    :param ip_list: ip列表
    :return:
    """
    for slave in ip_list:
        debug('Start get windows slave data at {}'.format(slave))
        start_time = db.select_latest_in_slave(slave)
        now_time = datetime.utcnow().timestamp()
        if not start_time:
            data = pull_data(slave, start_time)
            start_time = turn_timestr_to_timestamp(data[0][0])
        while now_time - start_time > PULL_CYCLE:
            data = pull_data(slave, start_time)
            if not data:
                break
            insert_data(db, slave, data)
            start_time = db.select_latest_in_slave(slave)


def get_linux_data(slave_list, localpath):
    """
    根据配置中的节点IP拉取linux节点数据
    :param slave_list:
    :param localpath:
    :return:
    """
    for slave in slave_list:
        debug('Start get linux slave data at {}'.format(slave.slave_ip))
        sftp = SFTP(slave)
        sftp.get_dir('/opt/perflog_{}'.format(slave.slave_ip), localpath)

        files = [os_path.join(localpath, slave, j) for j in
                 listdir(os_path.join(localpath, slave))]
        [r.record_data(localpath, f) for f in files]


def put_checksh(slave_list, shfile):
    remote_path = '/etc/cron.hourly/'
    for slave in slave_list:
        debug('Start get linux slave data at {}'.format(slave.slave_ip))
        sftp = SFTP(slave)
        sftp.put_file(shfile, remote_path)


def linux_file_to_db(linux_record, filepath):
    for slave in listdir(filepath):
        slave_ip = slave.split('_')[1]
        files = [os_path.join(filepath, slave, j) for j in
                 listdir(os_path.join(filepath, slave))]
        [linux_record.record_data(slave_ip, f) for f in files]


if __name__ == '__main__':
    d = MasterDb(DBPATH)
    client = Client(CONFIG_PATH)
    CHECKFILE = client.get_check_file()
    WIN_IP_LIST = client.get_win_slave()
    LINUX_IP_LIST = client.get_linux_slave()
    LOCALPATH = client.get_local_save_path()
    PROCESS = client.get_process_list()

    put_checksh(LINUX_IP_LIST, CHECKFILE)

    while True:
        [d.create_slave(slave) for slave in WIN_IP_LIST]
        get_win_data(d, WIN_IP_LIST)
        get_linux_data(LINUX_IP_LIST, LOCALPATH)

        # record linux to db
        r = LinuxRecord(d, PROCESS)
        linux_file_to_db(r, LOCALPATH)
        sleep(PULL_CYCLE)
