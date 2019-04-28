# 策略基类
class Strategy():
    def __init__(self,price,num):
        self.prices = price*num  # 抽象出公共操作

    def AlgorithmInterface(self):
        raise NotImplementedError # 抽象类

class ConcreteStrategyA(Strategy):
    def AlgorithmInterface(self):
        print('A')
        return self.prices*0.8

class ConcreteStrategyB(Strategy):
    def AlgorithmInterface(self):
        print('B')
        return self.prices*0.5
# 扩展性：
# class newStrategy(Strategy):
#     def AlgorithmInterface(self):
#         pass

class CashContext():
    def __init__(self,price,num,cond):
        self.price = price
        self.num = num
        # 使用简单工厂实例化具体策略
        strategies = {'8折': ConcreteStrategyA, '5折': ConcreteStrategyB}
        # 扩展：增加映射{}
        # strategies.setdefault('newstrategy',default=newStrategy)
        if strategies.__contains__(cond):
            self.strategy = strategies[cond]
        else:
            print('No such discount')
            raise Exception

    def getResult(self):
        return self.strategy(self.price,self.num).AlgorithmInterface()


# 页面逻辑
def client(price,num,discount):
    return CashContext(price,num,discount).getResult()

if __name__ == '__main__':
    print(client(5,3,'5折'))
    print(client(5,6,'1折'))
