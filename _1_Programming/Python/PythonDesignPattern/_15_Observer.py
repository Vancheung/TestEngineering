class Publisher:
    def __init__(self):
        self.observers = [] # 观察者列表

    # 增加观察者
    def add(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)
        else:
            print('Failed to add: {}'.format(observer))

    # 移除观察者
    def remove(self, observer):
        try:
            self.observers.remove(observer)
        except ValueError:
            print('Failed to remove: {}'.format(observer))

    # 通知观察者
    def notify(self):
        [o.notify(self) for o in self.observers]


class DefaultFormatter(Publisher):
    def __init__(self, name):
        Publisher.__init__(self)  # 子类继承父类的init方法
        self.name = name
        self._data = 0  # 下划线表示不应该直接访问这个变量

    def __str__(self):
        # type(self).__name__避免硬编码类名
        return "{}: '{}' has data = {}".format(type(self).__name__, self.name, self._data)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_value):
        try:
            self._data = int(new_value)
        except ValueError as e:
            print('Error: {}'.format(e))
        else:
            self.notify()

# 观察者1： 16进制格式化
class HexFormatter:
    def notify(self, publisher):
        print("{}: '{}' has now hex data = {}".format(type(self).__name__, publisher.name, hex(publisher.data)))

# 观察者2： 2进制格式化
class BinaryFormatter:
    def notify(self, publisher):
        print("{}: '{}' has now bin data = {}".format(type(self).__name__,publisher.name, bin(publisher.data)))

# 新增：观察者3： 8进制格式化
class OctalFormatter:
    def notify(self, publisher):
        print("{}: '{}' has now bin data = {}".format(type(self).__name__,publisher.name, oct(publisher.data)))


def main():
    df = DefaultFormatter('test1')
    print(df)
    print()

    hf = HexFormatter()
    df.add(hf) # 关联第一个观察者
    df.data = 3
    print(df)
    print()

    bf = BinaryFormatter()
    df.add(bf) # 关联第二个观察者
    df.data = 21 # 修改值之后两个观察者都会同步更新
    print(df)
    print()

    df.remove(hf) # 移除一个观察者
    df.data = 40
    print(df)
    print()

    df.remove(hf) # 移除不存在的观察者
    df.add(bf) # 添加已存在的观察者

    df.data = 'hello' # data改为错误的类型
    print(df)
    print()

    df.data = 15.8 #浮点数只取整数部分
    print(df)


def client():
    name = input('Please enter the name of your number: ')
    df = DefaultFormatter(name)
    hf = HexFormatter()
    df.add(hf)  # 关联第一个观察者
    bf = BinaryFormatter()
    df.add(bf)  # 关联第二个观察者
    of = OctalFormatter()
    df.add(of)  # 关联第三个观察者

    while True:
        number = input('Please enter a number: ')
        df.data = number
        print(df)

if __name__ == '__main__':
    # main()
    client()
