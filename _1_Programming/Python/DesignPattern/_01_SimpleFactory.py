#coding:utf-8
# 业务逻辑
# 基类
class Operation():
    def __init__(self,numA,numB):
        self.numA = numA
        self.numB = numB
# 加法类
class Op_Add(Operation):
    def __init__(self):
        pass
    def run(self):
        return self.numA+self.numB

# 减法类
class Op_Minus(Operation):
    def __init__(self):
        pass
    def run(self):
        return self.numA-self.numB

# 可扩展类

# 工厂方法：在实例化工厂类时再取初始化运算类的对象
def createOperate(op):
    #使用字典映射函数（python没有switch语句）
    operators = {'+':Op_Add,'-':Op_Minus} #扩展时增加字典
    return operators[op]

# 界面逻辑
class Calculate():
    def __init__(self,numA, numB, op):
        self.numA = numA
        self.numB = numB
        self.op = op
    def getResult(self):
        return createOperate(self.op).run(self)


if __name__ == "__main__":
    print(Calculate(3,5,'-').getResult())
