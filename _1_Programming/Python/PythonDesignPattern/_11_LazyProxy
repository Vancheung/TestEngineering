# 虚拟代理

# 惰性初始化的修饰器
class LazyProperty():
    def __init__(self,method):
        self.method = method
        self.method_name = method.__name__
        # print('function overriden: {}'.format(self.fget))
        # print("function's name: {}".format(self.func_name))
        print('Initializing')

    def __get__(self, instance, owner):
        if not instance:
            return None
        value = self.method(instance)
        print('value {}'.format(value))
        setattr(instance,self.method_name,value)
        return value
class Test():
    def __init__(self):
        self.x = 'foo'
        self.y = 'bar'
        self._resource = None

    @LazyProperty
    def resource(self):
        print('initialzing self._resource which is: {}'.format(self._resource))
        self._resource = tuple(range(5))
        print('initialzing self._resource which is: {}'.format(self._resource))
        return self._resource

def client():
    t = Test()
    print(t.x)
    print(t.y)
    print('Begin lazy initialization')
    print(t.resource)

if __name__ == '__main__':
    client()
