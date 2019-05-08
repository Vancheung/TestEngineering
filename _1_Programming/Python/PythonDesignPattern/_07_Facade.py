from abc import abstractmethod, ABCMeta
from enum import Enum

# 服务进程的不同状态
State = Enum('State', 'new running sleeping restart zombie')


class User():
    pass


class Process():
    pass


class File():
    pass


# Server抽象类（不能被实例化）
class Server(metaclass=ABCMeta):  # 继承抽象基类, 不能直接实例化
    # @abstractmethod 修饰抽象方法，必须重写，否则会报错
    @abstractmethod
    def __init__(self):
        pass

    def __str__(self):
        return self.name

    @abstractmethod
    def boot(self):
        pass

    @abstractmethod
    def kill(self, restart=True):
        raise NotImplementedError


# 文件服务
class FileServer(Server):
    def __init__(self):
        '''初始化文件服务进程要求的操作'''
        self.name = 'FileServer'
        self.state = State.new

    def boot(self):
        print('booting the {}'.format(self))
        '''启动文件服务进程要求的操作'''
        self.state = State.running

    def kill(self, restart=True):
        print('Killing {}'.format(self))
        '''终止文件服务进程要求的操作'''
        self.state = State.restart if restart else State.zombie

    # 本服务特有方法
    def create_file(self, user, name, permissions):
        '''检查访问权限的有效性、用户权限等'''
        print("trying to create the file '{}' for user '{}' with permissions {}".format(name, user, permissions))


# 进程服务
class ProcessServer(Server):
    def __init__(self):
        '''初始化进程服务进程要求的操作'''
        self.name = 'ProcessServer'
        self.state = State.new

    def boot(self):
        print('booting the {}'.format(self))
        '''启动进程服务进程要求的操作'''
        self.state = State.running

    def kill(self, restart=True):
        print('Killing {}'.format(self))
        '''终止进程服务进程要求的操作'''
        self.state = State.restart if restart else State.zombie

    def create_process(self, user, name):
        '''检查用户权限和生成PID等'''
        print("trying to create the process '{}' for user '{}'".format(name, user))

# 自行实现两个类
class WindowServer(Server):
    '''界面类'''
    def __init__(self):
        self.name = 'WindowServer'
        self.state = State.new

    def boot(self):
        print('booting the {}'.format(self))
        '''启动窗口服务进程要求的操作'''
        self.state = State.running

    def kill(self, restart=True):
        print('Killing {}'.format(self))
        self.state = State.restart if restart else State.zombie

class NetworkServer():
    '''网络类'''
    def __init__(self):
        self.name = 'NetworkServer'
        self.state = State.new

    def boot(self):
        print('booting the {}'.format(self))
        '''启动网络服务进程要求的操作'''
        self.state = State.running

    def kill(self, restart=True):
        print('Killing {}'.format(self))
        self.state = State.restart if restart else State.zombie

class OperatingSystem():
    '''外观'''
    def __init__(self):
        self.fs = FileServer()
        self.ps = ProcessServer()
        self.ws = WindowServer()
        self.ns = NetworkServer()
        # print(self.__dict__)

    def start(self):
        [i.boot() for i in (self.fs,self.ps,self.ws,self.ns)]

    # 包装方法作为客户端服务的访问点，客户端不需要知道具体由哪个类来执行
    def create_file(self,user,name,permission):
        return self.fs.create_file(user,name,permission)

    def create_process(self,user,name):
        return self.ps.create_process(user,name)

    # 新增方法
    def shutdown(self):
        # for i in self.__dict__:
        #     i.kill()
        [i.kill() for i in (self.fs,self.ps,self.ws,self.ns)]


def client():
    # file = FileServer()
    # file.boot()
    # server = Server() 抽象类不能实例化
    # # file.kill()
    os = OperatingSystem()
    os.start()
    os.create_file('foo','hello','-rw-r-r')
    os.create_process('bar','ls /tmp')
    os.shutdown()

if __name__ == '__main__':
    client()
