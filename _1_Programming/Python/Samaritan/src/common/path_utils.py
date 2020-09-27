# -*- coding: UTF-8 -*-

"""
-------------------------------------------------------------------------------
Describe:  项目路径管理
Created At: 2020-08-25,  21:52
Author: 
-------------------------------------------------------------------------------
"""
import sys
import os


class PathUtil(object):
    """
    路径处理工具类
    """

    def __init__(self):
        # 判断调试模式
        debug_vars = dict((a, b) for a, b in os.environ.items()
                          if a.find('IPYTHONENABLE') >= 0)
        # 根据不同场景获取根目录
        if len(debug_vars) > 0:
            """当前为debug运行时"""
            self.root_path = sys.path[2]
        elif getattr(sys, 'frozen', False):
            """当前为exe运行时"""
            self.root_path = os.getcwd()
        else:
            """正常执行"""
            self.root_path = sys.path[1]
        # 替换斜杠
        self.root_path = self.root_path.replace("\\", "/")

    def join_path_to_basedir(self, file_name):
        """
        按照文件名拼接资源文件路径
        :param file_name:
        :return:
        """
        return os.path.join(self.root_path, file_name)

    def mkdir_if_not_exist(self, dir_name):
        """
        创建文件夹
        :param dir_name:
        :return:
        """
        if os.path.exists(dir_name) or os.path.exists(self.join_path_to_basedir(dir_name)):
            pass
        print('%s not exist! Creating...' % dir_name)
        os.mkdir(dir_name)
        print('Create %s success!' % dir_name)
