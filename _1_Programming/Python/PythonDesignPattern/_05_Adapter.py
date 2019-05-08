# 原始类
class Computer():
    def __init__(self,name):
        self.name = name

    def __str__(self):
        return 'The {} computer'.format(self.name)

    def execute(self):
        return 'Execute a program'

# 新增的两个类（具有不兼容的接口）
class Synthesizer():
    def __init__(self,name):
        self.name = name

    def __str__(self):
        return 'The {} synthesizer'.format(self.name)

    def play(self):
        return 'is playing an electronic song'

class Human():
    def __init__(self,name):
        self.name = name

    def __str__(self):
        return '{} the human'.format(self.name)

    def speak(self):
        return 'say hello'

# 适配器
class Adapter():
    def __init__(self,obj, adapted_methods):
        self.obj = obj  # obj是想要适配的对象
        self.__dict__.update(adapted_methods)  # adapted_methods是一个字典，键是客户端需要调用的方法，值是被调用的方法

    def __str__(self):
        return str(self.obj) # 调用类自身的__str__()方法

def client():
    objects = [Computer('Asus')]

    # 不兼容的对象，使用adapter类适配他们
    # 对human和synth对象，实际上客户端不知道如何调用他们的execute方法
    synth = Synthesizer('moog')
    objects.append(Adapter(synth,dict(execute=synth.play))) # 建立execute方法（键）和play方法（值）的映射

    human = Human('Bob')
    objects.append(Adapter(human,dict(execute=human.speak)))

    for i in objects:
        # 封装后客户端可以始终调用已知的execute方法，不需要关心具体类的接口差别
        print(type(i)) # objects[0]:Computer, objects[1]&[2]: Adapter
        print('{} {}'.format(str(i),i.execute()))
        # print(i.name) # 'Adapter' object has no attribute 'name'

if __name__ =='__main__':
    client()
