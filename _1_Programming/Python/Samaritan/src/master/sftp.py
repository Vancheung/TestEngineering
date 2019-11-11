from logging import debug
from os import listdir, mkdir
from os import path as os_path
from stat import S_ISDIR

from paramiko import Transport, SFTPClient

BUF_SIZE = 32 * 1024


class SFTP(object):
    def __init__(self, asset, timeout=30):
        """
        请将asset封装成一个namedtuple
        :param asset:
        :param timeout:
        """
        self.ip = asset.slave_ip
        self.username = asset.slave_user
        self.password = asset.slave_pwd
        self.timeout = timeout
        self.Transport = Transport(sock=(self.ip, 22))
        debug('Connecting to {}'.format(self.ip))
        self.Transport.connect(username=self.username, password=self.password)
        self.sftp = SFTPClient.from_transport(self.Transport)

    # 断开连接
    def close(self):
        debug('Disconnecting to {}'.format(self.ip))
        self.Transport.close()

    def __get_all_files_from_remote_dir(self, remote_dir):
        all_files = list()
        if remote_dir[-1] == '/':
            remote_dir = remote_dir[0:-1]
        # 获取当前指定目录下的所有目录及文件，包含属性值
        files = self.sftp.listdir_attr(remote_dir)
        for x in files:
            # remote_dir目录中每一个文件或目录的完整路径
            filename = remote_dir + '/' + x.filename
            # 如果是目录，则递归处理该目录
            if S_ISDIR(x.st_mode):
                all_files.extend(self.__get_all_files_from_remote_dir(filename))
            else:
                all_files.append(filename)
        return all_files

    # 获取本地指定目录下的所有文件
    def __get_all_files_from_local_dir(self, local_dir):
        all_files = []
        files = listdir(local_dir)
        for x in files:
            filename = os_path.join(local_dir, x)
            if os_path.isdir(filename):
                all_files.extend(self.__get_all_files_from_local_dir(filename))
            else:
                all_files.append(filename)
        return all_files

    # get单个文件
    def get_file(self, remote_file, local_file):
        # 获取remote_file的属性值
        r_file = self.sftp.lstat(remote_file)
        if S_ISDIR(r_file.st_mode):
            debug('{} is a directory'.format(remote_file))
            return
        if os_path.isdir(local_file):
            filename = remote_file.split('/')[-1]
            local_file = os_path.join(local_file, filename)
        debug('file {} is downloading...'.format(remote_file))
        self.sftp.get(remote_file, local_file)

    # put单个文件
    def put_file(self, local_file, remote_file):
        r_file = self.sftp.lstat(remote_file)
        if S_ISDIR(r_file.st_mode):
            filename = local_file.split('/')[-1]
            remote_file = os_path.join(remote_file, filename)
        if os_path.isdir(local_file):
            debug('{} is a directory'.format(local_file))
            return
        debug('file {} is uploading...'.format(local_file))
        self.sftp.put(local_file, remote_file)
        self.sftp.chmod(remote_file, 777)


    # get 目录
    def get_dir(self, remote_dir, local_dir):
        all_files = self.__get_all_files_from_remote_dir(remote_dir)
        if not os_path.exists(local_dir):
            mkdir(local_dir)
        for x in all_files:
            filename = x.split('/')[-1]
            r_d = os_path.dirname(x).split('/')
            base_d = remote_dir.split('/')
            l_d = os_path.join(local_dir,
                               '/'.join(list(set(r_d) ^ set(base_d))))
            if not os_path.exists(l_d):
                mkdir(l_d)
            local_filename = os_path.join(l_d, filename)
            debug('file {} is downloading...'.format(filename))
            self.sftp.get(x, local_filename)

    # put目录
    def put_dir(self, local_dir, remote_dir):
        # 去掉路径字符穿最后的字符'/'，如果有的话
        if remote_dir[-1] == '/':
            remote_dir = remote_dir[0:-1]

        # 获取本地指定目录及其子目录下的所有文件
        all_files = self.__get_all_files_from_local_dir(local_dir)
        # 依次put每一个文件
        for x in all_files:
            filename = os_path.split(x)[-1]
            if os_path.isdir(x):
                l_d = x.split('/')
            else:
                l_d = os_path.dirname(x).split('/')

            base_d = local_dir.split('/')
            r_dir = os_path.join(remote_dir,
                                 '/'.join(list(set(l_d) ^ set(base_d))))
            try:
                self.sftp.lstat(r_dir)
            except Exception as e:
                mkdir(r_dir)
            if os_path.isdir(x): continue
            remote_filename = os_path.join(r_dir, filename)
            debug('file {} is uploading...'.format(x))
            self.sftp.put(x, remote_filename)
