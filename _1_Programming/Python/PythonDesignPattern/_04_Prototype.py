import copy
from collections import OrderedDict
# Prototype 类实现了原型设计模式
class Prototype():
    def __init__(self):
        self.objects = dict()

    # register 和 unregister 方便在字典中追踪被克隆的对象
    def register(self,identifier,obj):
        self.objects[identifier] = obj
    def unregister(self,identifier):
        del self.objects[identifier]

    def clone(self,identifier,**attr):  # 使用变长列表attr，可以在克隆时只传递真正需要变更的属性变量
        found = self.objects.get(identifier)
        if not found:  # 字典的key不存在时，抛出异常
            raise ValueError('Incorrect object identifier: {}'.format(identifier))
        obj = copy.deepcopy(found)  # 深复制对象
        obj.__dict__.update(attr)  # 更新属性变量
        return obj

# 书籍类
class Book():
    def __init__(self, name, authors, price, **rest):
        '''rest的例子有: 出版商、长度、 标签、出版日期'''
        self.name = name
        self.authors = authors
        self.price = price  # 单位为美元
        self.__dict__.update(rest) # 使用**变参列表来自定义参数

    def __str__(self):
        mylist = []
        ordered = OrderedDict(sorted(self.__dict__.items())) # 强制保证元素有序
        for i in ordered.keys():
            mylist.append('{}: {}'.format(i, ordered[i])) # 把每个属性加入mylist
            if i == 'price':
                mylist.append('$') # 对价格属性则新增$符号
            mylist.append('\n')
        return ''.join(mylist)
        # return str(mylist)  # 另一种方法


def client():
    b1 = Book('The C Programming Language', ('Brian W. Kernighan', 'Dennis M.Ritchie'),
              price=118, publisher='Prentice Hall', length=228, publication_date='1978-02-22',
              tags=('C', 'programming', 'algorithms', 'data structures'))
    prototype = Prototype()
    cid = 'k&r-first'
    prototype.register(cid, b1) # b1注册到原型字典
    b2 = prototype.clone(cid, name='The C Programming Language(ANSI)', price=48.99,
                         length=274, publication_date='1988-04-01', edition=2)  # 在原型字典中查找b1，深拷贝b1，然后执行参数更新，再把return的obj给b2
    for i in (b1, b2):
        print(i)  # 调用__str__()打印b1和b2的所有属性
        # print(type(i))  # <class '__main__.Book'>
    print("ID b1 : {} != ID b2 : {}".format(id(b1), id(b2)))

if __name__ == '__main__':
    client()
