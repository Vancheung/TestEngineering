# Python数据结构（1）——Python内置类型list、set、dict原理浅析

## list（列表）

### 1、Python接口

list是一个基本序列类型，在**builtins.py**文件中定义如下

```
Built-in mutable sequence.

If no argument is given, the constructor creates a new empty list.
The argument must be an iterable if specified.
```

list定义了以下接口：

```python
def append(self, *args, **kwargs): # real signature unknown
    """ Append object to the end of the list. """
    pass

def clear(self, *args, **kwargs): # real signature unknown
    """ Remove all items from list. """
    pass

def copy(self, *args, **kwargs): # real signature unknown
    """ Return a shallow copy of the list. """
    pass

def count(self, *args, **kwargs): # real signature unknown
    """ Return number of occurrences of value. """
    pass

def extend(self, *args, **kwargs): # real signature unknown
    """ Extend list by appending elements from the iterable. """
    pass

def index(self, *args, **kwargs): # real signature unknown
    """
    Return first index of value.
    
    Raises ValueError if the value is not present.
    """
    pass

def insert(self, *args, **kwargs): # real signature unknown
    """ Insert object before index. """
    pass

def pop(self, *args, **kwargs): # real signature unknown
    """
    Remove and return item at index (default last).
    
    Raises IndexError if list is empty or index is out of range.
    """
    pass

def remove(self, *args, **kwargs): # real signature unknown
    """
    Remove first occurrence of value.
    
    Raises ValueError if the value is not present.
    """
    pass

def reverse(self, *args, **kwargs): # real signature unknown
    """ Reverse *IN PLACE*. """
    pass

def sort(self, *args, **kwargs): # real signature unknown
    """ Stable sort *IN PLACE*. """
    pass
```

### 2、CPython实现

看一下[CPython](https://github.com/python/cpython/blob/master/Objects/listobject.c)的实现。CPython中使用动态数组（而非链表）来存储列表。指向这个数组的指针及其长度被保存在一个列表头结构中，添加或删除元素时，采用了动态分配的方式resize数组大小。

动态分配原理：（来自[Coursera算法课](https://d3c33hcgiwev3.cloudfront.net/_3293220668bef735d367a188452c32dc_13StacksAndQueues.pdf?Expires=1568937600&Signature=UM1d~xeE5UA3b9Dbx0uz0tdZbMv~il3TE~WOKQGxzRaBGPwQ7f7WDEdeQ7SLY7HkiqYNr-tcpxptRhUyEghQBa8yWuKHOhdtBKZAtTI2a9BzZD~PXfXYaiNggIWxLbUbmMAUZxNN9pECuTwcBH9rz5j8OOOMvenhpYDiiLoqIt4_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A )）

- push(): double size of array s[] when array is full. 
- pop(): halve size of array s[] when array is **one-quarter** full 

当 数组满时，push新元素，则重新分配一个2倍于当前数组的空间；当pop移除元素时，在数组元素个数为数组大小的1/4时，将数组缩小至原来的1/2.

（为什么是1/4？如果在当前数组元素数为1/2的时候resize，则在数组满时反复做push-pop-push-pop，每次都需要重新调整数组大小，开销极大。）

### 3、复杂度

（1）append()和pop()操作的复杂度是O(1)，在特殊情况下需要调用list_resize调整数组大小

（2）insert(index,value)操作的复杂度是O(n), 因为在插入时，index之后所有的元素都需要后移一位。

（3）remove(value)操作的复杂度是O(n)，在remove之后会做一个切片操作 list_ass_slice() 。

（4）slice切片操作复杂度是O(k)，k为切片后的元素个数。

补充一段关于切片操作的说明：

切片运算符[:]返回一个序列的切片。**切片过程是切下列表的一部分，创建新的列表，将切下的部分复制到新列表。**

切片既可以作为独立对象被“取出”原序列，也可以留在原序列，作为一种占位符使用。

“**非纯占位符**”的切片是非空列表，对它进行操作（赋值与删除），将会影响原始列表。即非纯占位符可以实现列表的替换。

```
li = [1, 2, 3, 4]

# 不同位置的替换
li[:3] = [7,8,9] # [7, 8, 9, 4]
li[3:] = [5,6,7] # [7, 8, 9, 5, 6, 7]
li[2:4] = ['a','b'] # [7, 8, 'a', 'b', 6, 7]

# 非等长替换
li[2:4] = [1,2,3,4] # [7, 8, 1, 2, 3, 4, 6, 7]
li[2:6] = ['a']  # [7, 8, 'a', 6, 7]

# 删除元素
del li[2:3] # [7, 8, 6, 7]
```

（5）sort()使用的是[Timesort](https://en.wikipedia.org/wiki/Timsort):

> **Timsort** is a [hybrid](https://en.wikipedia.org/wiki/Hybrid_algorithm) [stable](https://en.wikipedia.org/wiki/Category:Stable_sorts) [sorting algorithm](https://en.wikipedia.org/wiki/Sorting_algorithm), derived from [merge sort](https://en.wikipedia.org/wiki/Merge_sort) and [insertion sort](https://en.wikipedia.org/wiki/Insertion_sort), designed to perform well on many kinds of real-world data.

最坏情况复杂度O(nlogn），最好情况是O(n），平均是O(nlogn）。

（6）x in list操作复杂度是O(n)，因为需要遍历整个列表才能判断是否存在匹配元素。

### 4、元组（tuple）

元组是不可变的列表，一旦创建后就不能修改。

## dict（字典）

### 1、Python接口

```python
"""
dict() -> new empty dictionary
dict(mapping) -> new dictionary initialized from a mapping object's
    (key, value) pairs
dict(iterable) -> new dictionary initialized as if via:
    d = {}
    for k, v in iterable:
        d[k] = v
dict(**kwargs) -> new dictionary initialized with the name=value pairs
    in the keyword argument list.  For example:  dict(one=1, two=2)
"""
```

字典将一组唯一的键映射到相应的值。

### 2、CPython实现

CPython使用伪随机探测(pseudo-random probing)的散列表(hash table)作为字典的底层数据结构。由于这个实现细节，只有**可哈希的**对象才能作为字典的键。 

Python中所有不可变的内置类型都是可哈希的。可变类型（如列表，字典和集合）就是不可哈希的，因此不能作为字典的键。 

一个好的hash函数使到哈希桶中的值只有一个，若多个key hash到了同一个哈希桶中，称之为哈希冲突。查找值时，会先定位到哈希桶中，再遍历hash桶。

### 3、复杂度

在hash基本没有冲突的情况下get, set, delete, in复杂度都是O(1)，但是在最坏情况复杂度要高得多，为O(N)。

## set（集合）

### 1、Python接口

Set是一种可变的、无序的、有限的集合，其元素是唯一的、不可变的（可哈希的）对象。 （frozenset(): 不可变的集合）

```python
"""
set() -> new empty set object
set(iterable) -> new set object

Build an unordered collection of unique elements.
"""
```

### 2、自定义的类通过set()去重原理

关于set()函数去重的原理。set()调用的是类的\__hash__ 方法。

如果hash值相等，会去调用类的\__eq__方法。

看下这段代码：

```python
class Foo:
    def __init__(self,name,count):
        self.name = name
        self.count = count
    def __hash__(self):
        print("%s调用了哈希方法"%self.name)
        return hash(self.count)
    def __eq__(self, other):
        print("%s调用了eq方法"%self.name)
        return self.name == other.name

f1 = Foo('f1',1)
f2 = Foo('f2',1)
f3 = Foo('f3',3)
ls = [f1,f2,f3]
print(set(ls))
```

输入结果为：

```python
f1调用了哈希方法
f2调用了哈希方法
f1调用了eq方法
f3调用了哈希方法
{<__main__.Foo object at 0x00A4CE30>, <__main__.Foo object at 0x01255410>, <__main__.Foo object at 0x0123DF70>}
```

调用set()的时候，根据self.count做hash，f1和f2的count值相同，所以返回了同一个hash值，但系统不会因为hash值相同就认为两个元素相同，还需要去调用类的eq去比较。当eq是基于self.name来做判断的，则name不同说明是两个不同的对象，结果不会合并。如果修改一下代码，让eq基于self.count来做判断：

```python
def __eq__(self, other):
    print("%s调用了eq方法"%self.name)
    return self.count == other.count
```

输出结果：

```python
f1调用了哈希方法
f2调用了哈希方法
f1调用了eq方法
f3调用了哈希方法
{<__main__.Foo object at 0x036DCE30>, <__main__.Foo object at 0x03785410>}
```

即f1和f2被认为是相同的元素了。

所以，set()的去重原理可以简述为：

1、两个对象的hash值不同时，被认为是不同的元素。

2、两个对象的hash值相同时，调用类的\__eq__方法，返回True则认为两个对象是相同的，去重。

在自定义类的时候，重写类的\__eq__方法，就可以调用set()函数对一组类的对象进行去重。

### 3、复杂度

与list对比，set的优势在于 in 操作的复杂度是O(1)，因为set是先通过散列函数查找对应元素的。

## 

### 
