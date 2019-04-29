# 抽象工厂接口
class AbstractFactory():
    def __init__(self):
        pass
    def CreateProductA(self):  # 客户端通过抽象接口操纵实例
        raise NotImplementedError
    def CreateProductB(self):
        raise NotImplementedError

# 具体工厂类1：定义了同一个操作的不同实现
class ConcreteFactory1(AbstractFactory):
    def CreateProductA(self):
        print('SQL Server,Query user')
    def CreateProductB(self):
        print('MySQL,Query user')

# 具体工厂类2
class ConcreteFactory2(AbstractFactory):
    def CreateProductA(self):
        print('SQL Server,delete user')
    def CreateProductB(self):
        print('MySQL,delete user')


def client(sql):
    # 可以通过反射实现
    if sql=="SQL Server":
        # AbstractProductA：抽象产品
        ConcreteFactory1().CreateProductA() # 对抽象产品的具体分类的实现
        ConcreteFactory2().CreateProductA()
    else:
        # AbstractProductB
        ConcreteFactory1().CreateProductB()
        ConcreteFactory2().CreateProductB()


if __name__ == '__main__':
    sql = 'SQL Server' # 改变具体工厂即可使用不同配置
    client(sql)
