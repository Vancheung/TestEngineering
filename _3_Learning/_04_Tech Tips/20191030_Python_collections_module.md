# 【Python标准库】【2】collection——容器数据类型

collection类似C++ 的STL，提供了一些通用的容器类。借助这些容器可以实现一些复杂的数据结构和功能。

## 1、deque

deques是双向队列（double ended queue），支持从两端append和pop操作，两个方向的开销都是O(1)。而list的pop(0)操作，弹出最左侧元素时，会引起O(n)内存移动的操作。

指定长度：在初始化deque时限定最大长度，例如：

q  = deque(maxlen=10)

当队列满时，新加入一项，就会从另一端弹出一项。

```python
>>> q = deque(maxlen=10)
>>> [q.append(i) for i in range(10)]
[None, None, None, None, None, None, None, None, None, None]
>>> q
deque([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], maxlen=10)
>>> q.append(11)
>>> q
deque([1, 2, 3, 4, 5, 6, 7, 8, 9, 11], maxlen=10)
>>> q.appendleft(12)
>>> q
deque([12, 1, 2, 3, 4, 5, 6, 7, 8, 9], maxlen=10)
```

deque的append、pop、clear、index操作与list基本相同。

copy操作会创建浅拷贝，对于通过copy创建的新deque，所做修改不会影响到原deque。

```python
>>> q
deque([2, 1])
>>> r = q.copy()
>>> r
deque([2, 1])
>>> r.append(3)
>>> r
deque([2, 1, 3])
>>> q
deque([2, 1])
```

当deque设定了最大长度时，队列满时insert操作会抛出异常

```false
>>> q = deque(maxlen = 3)
>>> [q.append(i) for i in range(3)]
[None, None, None]
>>> q
deque([0, 1, 2], maxlen=3)
>>> q.insert(2,11)
Traceback (most recent call last):
  File "<input>", line 1, in <module>
IndexError: deque already at its maximum size
>>> q = deque(maxlen = 4)
>>> [q.append(i) for i in range(3)]
[None, None, None]
>>> q
deque([0, 1, 2], maxlen=4)
>>> q.insert(2,11)
>>> q
deque([0, 1, 11, 2], maxlen=4)
```

reverse() 将deque逆序排列。返回 None 。

rotate(n=1)
向右循环移动 n 步。 如果 n 是负数，就向左循环。如果deque不是空的，向右循环移动一步就等价于 d.appendleft(d.pop()) ， 向左循环一步就等价于 d.append(d.popleft()) 。

```python
>>> q
deque([0, 1, 11, 2], maxlen=4)
>>> q.reverse()
>>> q
deque([2, 11, 1, 0], maxlen=4)
>>> q.rotate(2)
>>> q
deque([1, 0, 2, 11], maxlen=4)
>>> q.rotate(-1)
>>> q
deque([0, 2, 11, 1], maxlen=4)
>>> q.rotate(5)
>>> q
deque([1, 0, 2, 11], maxlen=4)
```

通过rotate可以定义一个deque的切片操作：

```python
def delete_nth(d, n):
    d.rotate(-n)
    d.popleft()
    d.rotate(n)
```

定义deque的时候传入一个可迭代对象和长度n，可以获取最后n个元素

```python
>>> l = [1,2,3,4,5]
>>> deque(l,2)
deque([4, 5], maxlen=2)
```

## 2、defaultdict

[`defaultdict`](https://docs.python.org/zh-cn/3/library/collections.html#collections.defaultdict) 是内置 [`dict`](https://docs.python.org/zh-cn/3/library/stdtypes.html#dict) 类的子类。它重载了一个方法并添加了一个可写的实例变量，其余的功能与 [`dict`](https://docs.python.org/zh-cn/3/library/stdtypes.html#dict) 类相同。第一个参数 [`default_factory`](https://docs.python.org/zh-cn/3/library/collections.html#collections.defaultdict.default_factory) 提供了一个初始值。它默认为 `None` 。 

构造多值字典：构造一个字典时，如果需要将一个键映射到多个值，那么就需要将这多个值放到另外的容器中， 比如列表或者集合里面。 需要保持元素的插入顺序就应该使用list， 如果想去掉重复元素并且不关心元素顺序就使用set。 

```python
from collections import defaultdict

d = defaultdict(list)
d['a'].append(1)
d['a'].append(2)
d['b'].append(4)

d = defaultdict(set)
d['a'].add(1)
d['a'].add(2)
d['b'].add(4)
```

计数：通过int构造defaultdict，可以用来统计文档中字母或单词的个数。例如，以下是一个简单的统计词频的代码：

```python
from collections import defaultdict

with open('input.txt') as f:
    d = defaultdict(int)
    for key in f.read().split(' '):
        key = key.strip(',').strip('.')
        d[key] += 1
    print(d)
```

当一个单词首次出现时，d[key]查询失败，default_factory就会调用int()来提供一个默认值，int()总是返回0. 之后的自增操作会建立对每一个单词的计数。

统计字母频率：

```python
from collections import defaultdict

with open('input.txt') as f:
    d = defaultdict(int)
    for key in f.read():
        key = key.lower()
        d[key] += 1
    print(d)
```

## 3、OrderedDict

有序字典（OrderedDict ) 通过维护一个根据键插入顺序排序的双向链表，实现了额外的排序相关操作的功能。

每次当一个新的元素插入进来的时候， 它会被放到链表的尾部。迭代时字典会保持元素被插入的顺序。

对于一个已经存在的键的重复赋值不会改变键的顺序，但move_to_end()操作支持将元素移动到任意一端，所以可以在每次重新赋值时，使用move_to_end将元素移到末尾。例如，一个可以记录最后插入顺序的有序字典实现：

```python
class LastUpdatedOrderedDict(OrderedDict):
    'Store items in the order the keys were last added'

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)
```

popitem(last=True)：last=True时弹出最后一个元素，否则弹出第一个元素。

```python
>>> from collections import OrderedDict
>>> d = OrderedDict()
>>> d['foo'] = 1
... d['bar'] = 2
... d['spam'] = 3
... d['grok'] = 4
>>> d
OrderedDict([('foo', 1), ('bar', 2), ('spam', 3), ('grok', 4)])
>>> d.popitem()
('grok', 4)
>>> d.popitem(last=False)
('foo', 1)
```

OrderedDict的相等操作会检查顺序：

```python
>>> d
OrderedDict([('foo', 1), ('bar', 2), ('spam', 3), ('grok', 4)])
>>> d2
OrderedDict([('grok', 4), ('foo', 1), ('bar', 2), ('spam', 3)])
>>> d==d2
False
```

OrderedDict适合频繁处理重新排序操作，但一个OrderedDict的大小是普通字典的两倍，在空间复杂度和迭代、更新操作上性能会差一点。

## 4、ChainMap

ChainMap支持接受多个字典，并将它们在逻辑上变为一个字典。这些字典并不是真的合并在一起了， `ChainMap` 类只是在内部创建了一个容纳这些字典的列表 并重新定义了一些常见的字典操作来遍历这个列表。 

访问maps属性可以获取到这个列表：

```python
>>> c
ChainMap({'a': 10, 'b': 2}, {'c': 3, 'd': 4})
>>> c.maps
[{'a': 10, 'b': 2}, {'c': 3, 'd': 4}]
>>> type(c.maps)
<class 'list'>
```

如果出现重复键，那么第一次出现的映射值会被返回，对于字典的更新或删除操作总是影响的是列表中第一个字典。ChainMap不创建新的字典，因此对原字典操作后的结果会在映射中体现：

```python
>>> c = ChainMap(d1,d2)
>>> c
ChainMap({'a': 1, 'b': 2}, {'c': 3, 'd': 4})
>>> d1['a'] =10 
>>> c
ChainMap({'a': 10, 'b': 2}, {'c': 3, 'd': 4})
```

ChainMap实际管理的是一个映射，可以对这个映射进行操作。

例如，new_child()方法可以在ChainMap头部中加入新的字典，但这个操作返回的是一个新的映射，并不影响原ChainMap对象。

```python
>>> from collections import ChainMap
>>> d1 = {'a':1,'b':2}
>>> d2 = {'c':3,'d':4}
>>> c = ChainMap(d1,d2)
>>> c
ChainMap({'a': 1, 'b': 2}, {'c': 3, 'd': 4})
>>> c.new_child({'e':1})
ChainMap({'e': 1}, {'a': 1, 'b': 2}, {'c': 3, 'd': 4})
>>> c
ChainMap({'a': 1, 'b': 2}, {'c': 3, 'd': 4})
```

parents()返回一个包含所有的当前实例的映射，除了第一个

```python
>>> c
ChainMap({'a': 1, 'b': 2}, {'c': 3, 'd': 4}, {'e': 1})
>>> c.parents
ChainMap({'c': 3, 'd': 4}, {'e': 1})
>>> c
ChainMap({'a': 1, 'b': 2}, {'c': 3, 'd': 4}, {'e': 1})
```

## 5、Counter

Counter 对象接受任意的由可哈希（hashable）元素构成的序列对象， 提供快速和方便的计数。 在底层实现上，Counter对象是dict的子类，将元素映射到它出现的次数上 ，元素作为字典key，它们的计数存储为值。

如果引用的键没有任何记录，就返回一个0，而不是弹出一个 KeyError.

可以设置计数器的值，如果值为0，这个元素并不会从Counter中删除，想要删除可以使用 **del**实现

```python
>>> from collections import Counter
>>> c = Counter(['a','b'])
>>> c['c']
0
>>> c['a']
1
>>> c['a'] = 0
>>> c
Counter({'b': 1, 'a': 0})
>>> del c['a']
>>> c
Counter({'b': 1})
```

Counter可以结合数学运算的 '+'，'-' ，'&'，'|'

```python
>>> c1 = Counter(['a','b'])
>>> c2 = Counter(['b','c'])
>>> c1+c2
Counter({'b': 2, 'a': 1, 'c': 1})
>>> c1-c2
Counter({'a': 1})
>>> c1&c2
Counter({'b': 1})
>>> c1|c2
Counter({'a': 1, 'b': 1, 'c': 1})
```

Counter的elements()方法会返回一个迭代器，每个元素重复出现其计数值的次数，计数值小于1的元素会被忽略。用这种方式可以生成列表：

```python
>>> c = Counter(a=4, b=2, c=0, d=-2)
>>> [x for x in c.elements()]
['a', 'a', 'a', 'a', 'b', 'b']
```

most_common(n)方法会返回一个列表，包含n个最常见的元素及其出现次数，当n=None时会返回计数器中所有元素。对于出现次数相同的元素，按首次出现的次序排列：

```python
>>> Counter('abracadabra').most_common(3)
[('a', 5), ('b', 2), ('r', 2)]
>>> Counter('abracadabra').most_common()
[('a', 5), ('b', 2), ('r', 2), ('c', 1), ('d', 1)]
```

## 6、namedtuple

命名元组（namedtuple）给普通元组添加通过名字获取值的能力。

collection.namedtuple()是一个工厂函数，当新建一个命名元组时，需要传递一个类型名和需要的字段给它，然后它就会返回一个类。可以初始化这个类，为你定义的字段传递值等。并且namedtuple的实例支持所有普通元组的操作。

```python
>>> from collections import namedtuple
>>> Subscriber = namedtuple('Subscriber', ['addr', 'joined'])
>>> sub = Subscriber('jonesy@example.com', '2012-10-19')
>>> sub
Subscriber(addr='jonesy@example.com', joined='2012-10-19')
>>> sub.addr
'jonesy@example.com'
>>> sub.joined
'2012-10-19'
```

使用namedtuple替代普通元组的下标操作，可以让操作不依赖记录的结构。例如，当列表结构改变时，只需要调整namedtuple的顺序，不需要改动计算的部分：

```python
# Stock = namedtuple('Stock', ['name', 'shares', 'price'])
Stock = namedtuple('Stock', ['name', 'price', 'shares'])

def compute_cost(records):
    total = 0.0
    for rec in records:
        s = Stock(*rec)
        total += s.shares * s.price        
    return total
```

当需要一个很大的包含字典的数据结构，并且内容不需要改动时，命名元组也可以用来替代字典。如果真的需要改变属性的值，那么可以使用命名元组实例的 _replace() 方法，创建一个全新的命名元组并将对应的字段用新的值取代：

```python
>>> s = Stock('ACME', 100, 123.45)
>>> s
Stock(name='ACME', shares=100, price=123.45)
>>> s.shares = 75
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
AttributeError: can't set attribute
>>> s = s._replace(shares=75)
>>> s
Stock(name='ACME', shares=75, price=123.45)
```

将字典转换为namedtuple方法：

```python
from collections import namedtuple

Stock = namedtuple('Stock', ['name', 'shares', 'price', 'date', 'time'])

# Create a prototype instance
stock_prototype = Stock('', 0, 0.0, None, None)

# Function to convert a dictionary to a Stock
def dict_to_stock(s):
    return stock_prototype._replace(**s)

a = [{'name': 'ACME', 'shares': 100, 'price': 123.45},
{'name': 'ACME', 'shares': 100, 'price': 123.45, 'date': '12/17/2012'}]
print([dict_to_stock(i) for i in a])
```

