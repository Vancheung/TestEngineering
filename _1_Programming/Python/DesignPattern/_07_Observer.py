# 抽象主题类
class Topic(object):
    def __init__(self):
        self.obs = []
        print('father init')

    def Attach(self, ob):
        self.obs.append(ob)

    def Detach(self, ob):
        self.obs.remove(ob)

    def Notify(self):
        for ob in self.obs:
            ob.Update()

# 抽象观察者类
class Observer(object):
    def Update(self):
        raise NotImplementedError()

# 具体主题
class ConcreteTopic(Topic):
    def __init__(self):
        # 继承父类的init方法
        super(ConcreteTopic,self).__init__() # 不加这一行的话，会直接重写父类的init
        print('son init')
        self.state = None

    def ChangeState(self, newState):
        self.state = newState
        self.Notify()

# 具体监听类
class ConcreteObserver(Observer):
    def __init__(self, topic):
        self.topic = topic

    def Update(self):
        print(self.topic.state)  # 耦合了Subject类，可以通过委托解耦

def client():
    topic = ConcreteTopic()
    obs = ConcreteObserver(topic)
    topic.Attach(obs)

    topic.ChangeState('New State')

if __name__ == '__main__':
    client()
