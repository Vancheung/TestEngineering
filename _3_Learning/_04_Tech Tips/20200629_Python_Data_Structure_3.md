# Python数据结构与算法（3）——排序算法

##  1、自定义key函数，然后使用builtin的sorted函数来排序。

（1）当被排序对象为常用数据类型，排序规则为自定义的规则时，编写一个cmp函数，传入两个参数，函数返回值为-1(小于)、0（等于）、1（大于），在python3中调用key=functools.cmp_to_key(cmp)进行转换。

例：输入一个整数数组，输出结果按照奇数在前，偶数在后，且奇数由大到小，偶数由小到大的顺序排列。

```python
import functools


def my_sort(nums):
    return sorted(nums, key=functools.cmp_to_key(cmp))


def cmp(a, b):
    if a % 2 != b % 2:
        return -1 if a % 2 == 1 else 1
    if a % 2 == 1:
        return 1 if a < b else -1
    return -1 if a <= b else 1
```

（2）当被排序类型为自定义的类时，重写类的lt()/eq()/gt()方法，实现自定义类的排序。

例：将Person对象按age参数排序。

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __lt__(self, other):
        return self.age < other.age

    def __repr__(self):
        return 'Person name: {}, Person age: {}.'.format(self.name, self.age)


if __name__ == '__main__':
    persons = []
    for i in range(10, 1, -1):
        persons.append(Person(str(i), i))
    print(persons)
    print(sorted(persons))

```

## 2、手动实现排序函数

（1）python的sorted函数使用了Timsort算法。 Timsort是结合了合并排序（merge sort）和插入排序（insertion sort）而得出的排序算法。

（2）归并排序。归并排序的核心是二分法和递归。

首先，定义递归出口：当输入数组nums的长度小于等于1时，直接返回输入数组。

```python
def merge_sort(input_nums):
    if len(input_nums) <= 1:
        return input_nums   
```

其次，定义循环条件：将数组从中间一分为二，对左右数组分别进行归并排序，再将两个有序数组合并。

```python
middle = len(input_nums) // 2
a = merge_sort(input_nums[middle:])
b = merge_sort(input_nums[:middle])
return merge(a, b)
```

第三步，定义merge函数的输入和输出：输入是两个待合并的有序数组，由于merge_sort函数返回的是一个有序数组，因此merge函数的输出也应该是数组。结果数组的长度等于两个输入数组长度之和，空间占用为O(n)。

```python
def merge(nums_a, nums_b):
    result = [int] * (len(nums_a) + len(nums_b))
    # some code
    return result
```

第四步，完成排序函数。使用两个指针分别遍历数组nums_a和nums_b，比较当前值的大小，并将小的插入结果数组。（cmp函数为自定义的比较函数，为True则说明a在b的左边，否则a在b的右边）。当其中一个指针已经走到该数组尾部时，将另一

个数组剩余部分直接插入结果数组。

```python
idx_a, idx_b, idx_result = 0, 0, 0
while idx_a < len(nums_a) and idx_b < len(nums_b):
    if cmp(nums_a[idx_a], nums_b[idx_b]):
        result[idx_result] = nums_a[idx_a]
        idx_a += 1
    else:
        result[idx_result] = nums_b[idx_b]
        idx_b += 1
    idx_result += 1
if idx_a < len(nums_a):
    result[idx_result:] = nums_a[idx_a:]
if idx_b < len(nums_b):
    result[idx_result:] = nums_b[idx_b:]
```

完整代码如下，此代码为1中奇偶排序的扩展版。

```python
def merge(nums_a, nums_b):
    result = [int] * (len(nums_a) + len(nums_b))
    idx_a, idx_b, idx_result = 0, 0, 0
    while idx_a < len(nums_a) and idx_b < len(nums_b):
        if cmp(nums_a[idx_a], nums_b[idx_b]):
            result[idx_result] = nums_a[idx_a]
            idx_a += 1
        else:
            result[idx_result] = nums_b[idx_b]
            idx_b += 1
        idx_result += 1
    if idx_a < len(nums_a):
        result[idx_result:] = nums_a[idx_a:]
    if idx_b < len(nums_b):
        result[idx_result:] = nums_b[idx_b:]
    return result


def merge_sort(input_nums):
    if len(input_nums) <= 1:
        return input_nums
    middle = len(input_nums) // 2
    a = merge_sort(input_nums[middle:])
    b = merge_sort(input_nums[:middle])
    return merge(a, b)


def cmp(a, b):
    """
    :param a:
    :param b:
    :return: True-a,b; False-b,a, a==b:True
    """
    if a % 2 != b % 2:
        return a % 2 == 1
    return not a < b if a % 2 == 1 else a <= b
```

（3）快速排序。快速排序的核心是，选中一个数字，然后遍历整个数组，比它小的移到它前面，比它大的移到它后面，然后把这个数字放到正确的位置，再对当前数组左边和右边的子数组进行递归。

为避免数组大量移动，每次可以选择被排序数组中最后一个数字作为基数，移动开销会低于选第一个数字。

对于随机性比较高的数组，快速排序的时间复杂度趋于O(nlogn)，每次递归时子数组的长度趋近数组的一半，复杂度接近归并排序，而对于有序数组，每次递归时子数组长度为n-1，时间复杂度趋于O(n^2)。

第一步，定义递归出口：当数组长度小于等于1时，直接返回数组。

```python
def quick_sort(input_nums):
    if len(input_nums) <= 1:        
    	return input_nums
```

第二步，定义循环条件：获取当前数组末尾最后一个元素的正确位置，然后分别对该元素左边和右边的子数组递归进行quick_sort。由于对形参的修改并不会传出到函数外，因此需要用quick_sort的结果数组分别替换左右子数组。由于快排的原地排序性，不管数组是否执行了递归，最终都需要返回输入数组，因此将前面的递归出口调整为：数组长度>1时先递归再返回输入数组，否则直接返回输入数组。

```python
def quick_sort(input_nums):
    if len(input_nums) > 1:
        idx = partition(input_nums) # 获取数组末尾元素正确的位置
        input_nums[:idx] = quick_sort(input_nums[:idx])
        input_nums[idx + 1:] = quick_sort(input_nums[idx + 1:])
    return input_nums
```

第三步，定义partition函数的输入和输出：输入为需要操作的数组，输出为该数组末尾元素的正确位置坐标。使用两个指针i和j，i始终指向数组的分界点，j用来遍历整个数组（不包括最后一个元素）。当j遍历完之后，交换当前i指向的值和最后一个数字。

例如：[5,7,6,3,4] ->[3,7,6,5,4], i=1

```python
def partition(array):
    end = array[len(array) - 1]
    i, j = 0, 0
    while j < len(array) - 1:
        # some code
    array[len(array) - 1] = array[i]
    array[i] = end
    return i
```

第四步，实现while循环中的操作。当array[j]小于结尾元素时，如果i、j相等，则i、j分别后移一位，否则交换i、j指向的值，再后移i、j；如果array[j]不小于结尾元素，则直接后移j。

```python
while j < len(array) - 1:
    if cmp(array[j], end):
        if i==j:
            i += 1
            j += 1
        else:
            # swap array[i],array[j]
            i += 1
            j += 1
    else:
        j += 1
```

将重复逻辑优化一下:

```python
while j < len(array) - 1:
    if cmp(array[j], end):
        if i != j:
            array[i], array[j] = array[j], array[i]
        i += 1
    j += 1
```

完整代码如下：

```python
def quick_sort(input_nums):
    if len(input_nums) > 1:
        idx = partition(input_nums)
        input_nums[:idx] = quick_sort(input_nums[:idx])
        input_nums[idx + 1:] = quick_sort(input_nums[idx + 1:])
    return input_nums


def partition(array):
    end = array[len(array) - 1]
    i, j = 0, 0
    while j < len(array) - 1:
        if cmp(array[j], end):
            if i != j:  # 当结尾元素已经归位时，降低交换操作的开销
                array[i], array[j] = array[j], array[i]
            i += 1  # i总是指向第一个大于x的数字位置
        j += 1
    array[len(array) - 1] = array[i]
    array[i] = end
    return i


def cmp(a, b):
    """
    :param a:
    :param b:
    :return: True-a,b; False-b,a, a==b:True
    """
    if a % 2 != b % 2:
        return a % 2 == 1
    return not a < b if a % 2 == 1 else a <= b
```

