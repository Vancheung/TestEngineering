# 【Python标准库】【3】内建对象bulitins.py

## 1、数字操作

（1）abs——返回数字绝对值

（2）divmod——取除+取余，返回(x//y, x%y)

```python
>>> divmod(10,3)
(3, 1)
```

（3）pow——返回x ** y (with two arguments) or x ** y % z (with three arguments)

（4）round——返回浮点数的四舍五入值。

```python
>>> round(2.675, 2) 
2.67
```

**按我们的想法返回结果应该是 2.68，可结果却是 2.67，为什么？**

这跟浮点数的精度有关。我们知道在机器中浮点数不一定能精确表达，因为换算成一串 1 和 0 后可能是无限位数的，机器已经做出了截断处理。那么在机器中保存的2.675这个数字就比实际数字要小那么一点点。这一点点就导致了它离 2.67 要更近一点点，所以保留两位小数时就近似到了 2.67。

## 2、进制转换

（1）ascii——返回输入内容编码后的格式，例如：

```python
>>> ascii('abc123')
"'abc123'"
>>> ascii('张')
"'\\u5f20'"
>>> ascii(123)
'123'
```

（2）bin——将int类型转为2进制。

（3）chr——将数字格式的编码值转换为Unicode字符

```python
>>> chr(65)
'A'
>>> chr(0x5f20)
'张'
```

（4）format——格式化字符串

（5）hex——将int类型转换为16进制

（6）oct——将int类型转换为8进制

（7）ord——返回字符的Unicode值

## 3、类与对象

（1）all——所有迭代对象为真（或不为空）

（2）any——迭代对象中任意一个为真（或不为空）

（3）hash——返回对象的哈希值。 **hash()** 函数可以应用于数字、字符串和对象，不能直接应用于 list、set、dictionary。单次运行时，同一个对象的hash值相同，再次运行时，hash值会改变，不能视为固定值。

（4）id——对象的唯一id（CPython中返回的是对象的内存地址）

（5）isinstance——对象是否为已知的类型或其子类（可以是一个类型元组）

```python
>>>a = 2
>>> isinstance (a,int)
True
>>> isinstance (a,str)
False
>>> isinstance (a,(str,int,list))    # 是元组中的一个返回 True
True
>>> class A:
...     pass
>>> a = A()
>>> class B(A):
...     pass
>>> b = B()
>>> isinstance(a,A)
True
>>> isinstance(b,B)
True
>>> isinstance(b,A)
True
```

（6）issubclass—— 判断参数 class 是否是类型参数 classinfo 的子类。classinfo可以是一个tuple。

## 4、调试

（1）breakpoint—— 会中断当前程序并进入 [`pdb`](https://docs.python.org/3/library/pdb.html#module-pdb) 调试器 

（2）compile—— 将字符串编译为字节代码 

（3）eval——将字符串作为Python表达式来求值。不符合安全编程规范要求，禁止使用。

（4）exec——将字符串作为有效python代码来执行。不符合安全编程规范要求，禁止使用。

（5）exit——退出解释器

（6）help—— 查看函数或模块用途的详细说明

（7）quit——退出解释器

（8）repr——返回对象的string格式

## 5、属性

```python
>>> class A:
...     def __init__(self):
...         self.x = 1
...         self.y = 2
...         
>>> a = A()
```

（1）callable——是否可调用。

可调用：类（默认继承了call方法）、方法、函数、lambda函数

不可调用：常量、类的实例

```python
>>> callable(a)
False
>>> callable(a.x)
False
>>> callable(A)
True
```

（2）delattr——删除对象的属性

```python
>>> a.x
1
>>> delattr(a,'x')
>>> a.x
Traceback (most recent call last):
  File "<input>", line 1, in <module>
AttributeError: 'A' object has no attribute 'x'

```

（3）dir—— 函数不带参数时，返回当前范围内的变量、方法和定义的类型列表；带参数时，返回参数的属性、方法列表。如果参数包含方法__dir__()，该方法将被调用。如果参数不包含__dir__()，该方法将最大限度地收集参数信息。 

module：返回模块的属性

类的对象：（递归地）返回属性

其他对象：属性、类属性、基类属性

```python
>>> dir(a)
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'x', 'y']
```

（4）getattr——获取对象的属性

```python
>>> getattr(a,'x')
1
>>> getattr(a,'z')
Traceback (most recent call last):
  File "<input>", line 1, in <module>
AttributeError: 'A' object has no attribute 'z'
```

（5）hasattr——对象是否存在某属性

```python
>>> hasattr(a,'x')
True
>>> hasattr(a,'b')
False
```

（6）setattr——设置对象的属性、值。setattr(x, 'y', v) is equivalent to ``x.y = v''

（7）vars——无参数时：返回当前作用域的属性和属性值；参数为对象时，返回对象的属性和属性值

## 6、作用域

L（local）-> E(enclosing) -> G(global) -> B(builtin)：局部作用域>闭包函数外的函数中>全局作用域>内建作用域

 Python 中只有模块（module），类（class）以及函数（def、lambda）才会引入新的作用域。

（1）globals——当前作用域内的全局变量

（2）locals——当前作用域内的局部变量

## 7、输入输出

（1）input—— 接受一个标准输入数据，返回为 string 类型

（2）open——以流的形式打开文件，返回一个file对象。支持以文本格式或二进制格式打开。

（3）print——打印到控制台

```python
print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)
```

- objects -- 复数，表示可以一次输出多个对象。输出多个对象时，需要用 , 分隔。
- sep -- 用来间隔多个对象，默认值是一个空格。
- end -- 用来设定以什么结尾。默认值是换行符 \n，我们可以换成其他字符串。
- file -- 要写入的文件对象。
- flush -- 输出是否被缓存通常决定于 file，但如果 flush 关键字参数为 True，流会被强制刷新。

## 8、迭代器

（1）iter——为支持迭代的集合对象生成迭代器。

（2）next——返回迭代器的下一个元素。

```python
>>> l = [1,2,3]
>>> a = iter(l)
>>> next(a)
1
>>> next(a)
2
>>> next(a)
3
>>> next(a)
Traceback (most recent call last):
  File "<input>", line 1, in <module>
StopIteration
```

## 9、容器

（1）max——返回可迭代类型或多个参数中最大的值

（2）min——返回可迭代类型或多个参数中最小的值

（3）len——返回容器的长度（元素个数）

（4）sorted——给容器中内容排序（reverse=True，逆序）

```python
>>> a = [1,3,2]
>>> sorted(a)
[1, 2, 3]
>>> a
[1, 3, 2]
>>> sorted(a,reverse=True)
[3, 2, 1]
```

（5）sum——容器中所有值求和

