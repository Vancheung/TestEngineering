# 从函数式编程的角度理解Python的map、reduce、filter

## 一、函数式编程

函数式编程是一种编程范式，将计算机运算视为函数运算，并且避免使用程序状态及易变对象。

**函数式编程的特征**

- **stateless**：函数不维护任何状态。
- **immutable**：输入数据发生变化时，返回新的数据集。

- **惰性求值**：表达式不在它被绑定到变量之后就立即求值，而是在该值被取用的时候求值。
- **确定性**：所谓确定性，就是像在数学中那样，`f(x) = y` 这个函数无论在什么场景下，都会得到同样的结果。

应用函数式编程，函数之间没有共享的变量，而是通过参数和返回值传递数据，可以重点关注做什么而非怎么做。

根据 **Algorithm = Logic +Control** ，在Python中使用map、reduce、filter，实际上改变的是 Control 的部分，即改变算法执行的策略，而不修改真正的业务Logic。

## 二、关键字

### 0. lambda

Python中可以用 [`lambda`](https://docs.python.org/zh-cn/3/reference/expressions.html#lambda) 关键字来创建一个小的**匿名函数**。

例如，这个lambda函数返回两个参数的和： `lambda a, b: a+b` 。

Lambda函数可以在需要函数对象的任何地方使用。在语法上，仅限于单个表达式。从语义上来说，它们只是正常函数定义的语法糖。

### 1. map

先看一个示例，下面的代码使用常规的面向过程方式，将一个字符串中所有小写字母转换为大写：

```python
lowname = ['hello','world']
upper_name =[] 
for i in range(len(lowname)):
    upper_name.append( lowname[i].upper() )
```

面向过程的写法通过一个循环读取所有输入，依次进行转换。

而函数式的写法，将转换过程抽象成一个函数，然后在调用时不需要使用循环，而是使用map关键字:

```python
def toUpper(item):
      return item.upper()
upper_name = map(toUpper, ['hello','world'])
```

在builtins.py文件中，可以查看map的定义：

```
map(func, *iterables) --> map object

Make an iterator that computes the function using arguments from each of the iterables.  Stops when the shortest iterable is exhausted.
```

即，map将func函数应用于传入序列的每个元素，并将结果作为新的list返回。map抽象了运算规则，使代码更易阅读。

函数func可以为一个具体的函数，也可以为一个lambda函数，例如下面的代码会把nums列表中每一个数乘3。

```python
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] 
newnums = map(lambda x: x*3, nums)
```

func参数的类型是一个function对象，只需要写函数名，不需要加括号。


### 2. reduce

在Python3中，使用reduce需要先从functool中引入，在_functools.py中可以查看reduce函数的定义。

```python
reduce(function, sequence[, initial]) -> value

Apply a function of two arguments cumulatively to the items of a sequence,
from left to right, so as to reduce the sequence to a single value.
For example, reduce(lambda x, y: x+y, [1, 2, 3, 4, 5]) calculates ((((1+2)+3)+4)+5).  If initial is present, it is placed before the items of the sequence in the calculation, and serves as a default when the
sequence is empty.
```

reduce对在参数序列中的元素，执行函数function，这个函数必须接收两个参数，reduce把结果继续与序列的下一个元素进行累积计算。

再看一个简单的示例，对一个列表中所有元素求和，非函数式编程的写法如下：

```python
nums = [2, -5, 9, 7, -2, 5, 3, 1, 0, -3, 8]
result = 0
for i in nums:
    result += i
```

使用reduce，可以隐藏数组遍历求和控制流程，让代码的业务逻辑更清晰：

```python
from functools import reduce
nums = [2, -5, 9, 7, -2, 5, 3, 1, 0, -3, 8]
result = reduce(lambda x,y:x+y, nums)
```

当函数变复杂时，reduce的收益就会更明显，例如，将序列转换为整数：

```python
from functools import reduce
nums = [2, 5, 9, 7, 2, 5, 3, 1, 0, 3, 8]
result = reduce(lambda x,y:x*10+y, nums)
# result = 25972531038
```

### 3. filter

filter应用于过滤序列，以一个判断函数和可迭代对象作为参数，返回序列中满足判断函数的元素组成的列表。

```
filter(function or None, iterable) --> filter object

Return an iterator yielding those items of iterable for which function(item) is true. If function is None, return the items that are true.
```

例如，过滤出一个列表中所有奇数：

```python
def is_odd(n):
    return n % 2 == 1
newlist = filter(is_odd, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
```

函数式编程三套件map、reduce、filter，都属于简化控制流程的函数。适当使用可以使代码更清晰易读，更聚焦于业务处理逻辑。例如，写一个计算数组中所有正数平均值的函数，使用面向过程的写法如下：

```python
# 计算数组中正数的平均值
num = [2, -5, 9, 7, -2, 5, 3, 1, 0, -3, 8]

def calcute_average(num):
    positive_num_cnt = 0
    positive_num_sum = 0
    average = 0
    for i in range(len(num)):
        if num[i] > 0:
            positive_num_cnt += 1
            positive_num_sum += num[i]

    if positive_num_cnt > 0:
        average = positive_num_sum / positive_num_cnt

    return average
```

而使用函数式编程写法如下：

```python
def calcute_average2(num):
    positive_num = list(filter(lambda x: x > 0, num)) # 过滤正数
    return reduce(lambda x, y: x + y, positive_num) / len(positive_num)  # average = 正数列表求和/正数个数
```

注意：python3中filter函数的返回值为一个filter对象，需要转换成list对象才能使用reduce，而python2中可以直接写

`positive_num = filter(lambda x: x > 0, num)`

可以看到，这种方法通过去掉循环体，解耦了控制逻辑与业务逻辑，去掉了控制逻辑中的临时变量，代码重点在描述“做什么”。




