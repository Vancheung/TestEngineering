# 代理类和实体类继承同一个抽象基类（或接口）
class Subject(object):
    def Request(self):
        raise NotImplementedError()

class RealSubject(Subject):
    def Request(self):
        print("真实请求")

class Proxy(Subject):
    def __init__(self):
        #代理类内部维护一个实体类的对象
        self.realSubject = RealSubject()
    
    # 功能实现时调用实体类的接口
    def Request(self):
        print("代理请求")
        self.realSubject.Request()

def client():
    proxy = Proxy()
    proxy.Request()


if __name__ == "__main__":
    client()
