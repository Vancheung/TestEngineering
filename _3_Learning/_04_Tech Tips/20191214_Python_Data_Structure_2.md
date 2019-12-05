# Python数据结构（2）——简单数据结构的实现

常见的数据结构包括：数组、字符串、队列、堆、栈、链表、树、图、哈希表等。

python系统库的list、set、dict以及collection容器类实现了一些常用数据结构，借助这些已有的库，还可以实现更多的常用数据结构。

文中部分数据结构的接口和实现参考了《算法（第四版）》，可能存在部分不符合python命名规范的情况。

## 一、数组

数组是最常用的数据结构之一，在python中，list、tuple都可以实现数组的功能，具体使用list还是tuple可以根据实际情况来抉择。通常在希望对数组内容进行增删改时使用list，而只对数组进行查询时使用tuple。

数组的主要功能是根据下标定位元素，列表和元组都可以使用 [index] 方式来定位元素，较为简单，不再赘述。

```python
>>> list = ['a','b','c']
>>> list[0]
'a'
>>> tuple = ('d','e')
>>> tuple[1]
'e'
```

## 二、字符串（String）

Python中使用str类来进行字符串操作，具体实现的接口可以查阅[官方文档](https://docs.python.org/zh-cn/3/library/stdtypes.html#text-sequence-type-str)。

注意：字符串为不可变的对象，所有针对字符串的操作（如：str+= 、 ''.join() ）实际上都是创建了新的字符串对象。python底层使用一种高效的方式：原地扩充，来避免反复分配内存和对象拷贝。

## 三、队列

队列一般是指先进先出（FIFO）的数据结构。

在Python中，list虽然可以通过append()和pop(0)来实现队列的接口，但是pop(0)操作会引起内存移动，时间复杂度为O(n)。

而collections.deque实现的是双向队列，从两端增删元素的复杂度都是O(1)。

因此，可以使用collections.deque类实现队列的接口，具体实现如下：

```python
class Queue:
    def __init__(self):
        self.myque = deque()

    def enqueue(self, item):
        self.myque.append(item)

    def dequeue(self):
        if self.isEmpty():
            raise IndexError("Queue underflow")
        return self.myque.popleft()

    def peek(self):
        x = self.dequeue()
        self.myque.appendleft(x)
        return x

    def isEmpty(self):
        return len(self) == 0

    def __len__(self):
        return len(self.myque)

    def __repr__(self):
        rep = ' '.join([str(i) for i in self.myque])
        return 'size: {}\nqueue:{}'.format(len(self), rep)
```

在Java中实现类似的接口，需要使用泛型编程，而在python中，并没有检查item对象的类型，因此队列中的元素可能是任何对象。另外，deque不支持直接获取最后一个元素，对于peek方法（获取最后一个元素的值，但不从队列中弹出），可以使用deque.pop()获取到该元素，再把该元素重新加入队列。

## 四、栈

栈是后进先出（LIFO）结构，可以直接使用python的list来实现。

```python
class Stack:
    def __init__(self):
        self.mystack = []

    def push(self, item):
        self.mystack.append(item)

    def pop(self):
        if self.isEmpty():
            raise IndexError("Stack underflow")
        return self.mystack.pop()

    def peek(self):
        return self.mystack[-1]

    def isEmpty(self):
        return len(self) == 0

    def __len__(self):
        return len(self.mystack)

    def __repr__(self):
        rep = ' '.join([str(i) for i in self.mystack])
        return 'size: {}\nstack:{}'.format(len(self), rep)
```

## 五、链表（Linked List）

### 1、链表节点的数据结构

链表节点主要包含当前节点的值，和一个指向下一节点的指针，简单定义如下：

```python
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

    def __eq__(self, other):
        return isinstance(other, ListNode) and self.val == other.val

    def __iter__(self):
        return self

    def __next__(self):
        return self.next

    def __repr__(self):
        return str(self.val)
```

通过自定义\_\_eq\_\_()，实现节点的泛型。ListNode本身应该是可迭代的对象，通过实现\_\_iter\_\_() 方法和\_\_next\_\_()方法，可以使用循环遍历ListNode。

而一个链表类的基本接口定义如下：

```python
class LinkedList:
    def __init__(self):
        pass

    def add(self):
        pass

    def remove(self, x):
        pass

    def search(self, x) -> int:
        pass

    def __len__(self):
        pass

    def is_empty(self):
        pass
```

由于链表通常需要迭代访问，因此定义一个_\_iter\_\_() 方法：

```python
    def __iter__(self):
        for node in self.iter_node():
            yield node.val

    def iter_node(self):
        curr = self.head
        while curr:
            yield curr
            curr = curr.next
```

### 2、单链表

单链表需要实现增删改查的基本操作。

单链表的插入可以分为头插法和尾插法，头插法是将新节点插入到链表头部，时间和空间复杂度都为O(1)；尾插法将新节点插入链表尾部，时间复杂度为O(n)。具体实现如下：

```python
    def addFirst(self, item):
        new_node = ListNode(item)
        new_node.next = self.head
        self.head = new_node
        self.counter += 1

    def addLast(self, item):
        new_node = ListNode(item)
        self.counter += 1
        if not self.head:
            self.head = new_node
            return
        curr = self.head
        while next(curr):
            curr = next(curr)
        curr.next = new_node
```

链表的查找、删除操作都需要遍历链表，时间复杂度为O(n)

```python
    def search(self, x):
        if self.is_empty():
            raise IndexError('Empty Linked List')
        curr = self.head
        index = 0
        while curr:
            if curr.val == x:
                return index
            curr = curr.next
            index += 1
        raise IndexError('No such Element')
        
    def remove(self, x):
        if self.is_empty():
            raise IndexError('Empty Linked List')
        if self.head.val == x:
            self.head = self.head.next
            self.counter-=1
            return
        prev = self.head
        for node in self.iter_node():
            if node.val == x:
                prev.next = node.next
                del node
                self.counter -= 1
                return
            prev = node
        raise IndexError('No such Element')
```

### 3、双链表

双链表支持从两端插入和删除，推荐直接使用python的collections.deque().

自定义的python双链表的节点和数据结构如下：

```python
class ListNode:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


class DoubleLinkedList:
    def __init__(self):
        self.head = ListNode(None)
        self.tail = ListNode(None)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.counter = 0
```

双链表的操作如下：

```python
# 插入列表尾部    
    def append(self, value):        
        new_node = ListNode(value)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            self.counter += 1
            return
        new_node.prev = self.tail
        self.tail.next = new_node
        self.counter += 1
        self.tail = new_node

    # 插入列表头部
    def appendleft(self, value):        
        new_node = ListNode(value)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            self.counter += 1
            return
        new_node.next = self.head
        self.head.prev = new_node
        self.counter += 1
        self.head = new_node

    def find(self, value):
        cur = self.head.next
        while cur and cur.value != value:
            cur = cur.next
        return cur

    # 删除一个节点
    def remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
        self.counter -= 1
```

## 六、堆（Heap）

### 1、二叉堆（Binary Heap）

[堆队列（优先级队列）](https://docs.python.org/zh-cn/3/library/heapq.html)是一个二叉树，它的每个父节点的值都只会小于或大于所有孩子节点（的值）。 Python lib/heapq.py中，通过使用数组实现了下标从0开始的“最小堆”。

heapq的堆是通过数组来实现的，其中的元素从 0 开始计数，对于所有的 *k* 都有 `a[k] <= a[2*k+1]` 且 `a[k] <= a[2*k+2]`。 为了便于比较，不存在的元素被视为无穷大。  `a[0]` 总是其中最小的元素。 

#### 1、插入节点：

在数组末尾插入一个元素，然后对该元素进行自下而上的调整 操作，时间复杂度为O(logn)。

在heapq中的实现：

```python
def heappush(heap, item):
    """Push item onto heap, maintaining the heap invariant."""
    heap.append(item)
    _siftdown(heap, 0, len(heap)-1)
```

其中，调整操作_siftdown()的实现：如果堆的有序状态因为某个节点比它的父节点小而打破，则交换两个节点的值，向上遍历，直到遇到一个更小的父节点则结束。

```python
def _siftdown(heap, startpos, pos):
    newitem = heap[pos]
    # Follow the path to the root, moving parents down until finding a place
    # newitem fits.
    while pos > startpos:
        parentpos = (pos - 1) >> 1
        parent = heap[parentpos]
        if newitem < parent:
            heap[pos] = parent
            pos = parentpos
            continue
        break
    heap[pos] = newitem
```

#### 2、弹出节点：

弹出并返回 *heap* 的最小的元素 ：先调用list的pop()，获取列表最后一个元素，如果pop()操作后的数组非空，则把获取到的元素放到数组根节点，然后自上而下调整堆。复杂度为O(logn）

```python
def heappop(heap):
    """Pop the smallest item off the heap, maintaining the heap invariant."""
    lastelt = heap.pop()    # raises appropriate IndexError if heap is empty
    if heap:
        returnitem = heap[0]
        heap[0] = lastelt
        _siftup(heap, 0)
        return returnitem
    return lastelt
```

其中，调整操作_siftup()的实现：如果堆的有序状态因为某个节点比它的子节点大而破坏了，那么可以通过将它和它的子节点中较小的一个交换位置，来恢复堆的有序性。交换可能会打破子节点的有序状态，因此需要不断向下修复，直到该节点的子节点都比它小或到达了堆的底部。heapq中的做法是，先与两个子节点中较小的交换位置，直到下沉到叶节点，再对该叶节点进行一次siftdown()操作。

```python
def _siftup(heap, pos):
    endpos = len(heap)
    startpos = pos
    newitem = heap[pos]
    # Bubble up the smaller child until hitting a leaf.
    childpos = 2*pos + 1    # leftmost child position
    while childpos < endpos:
        # Set childpos to index of smaller child.
        rightpos = childpos + 1
        if rightpos < endpos and not heap[childpos] < heap[rightpos]:
            childpos = rightpos
        # Move the smaller child up.
        heap[pos] = heap[childpos]
        pos = childpos
        childpos = 2*pos + 1
    # The leaf at pos is empty now.  Put newitem there, and bubble it up
    # to its final resting place (by sifting its parents down).
    heap[pos] = newitem
    _siftdown(heap, startpos, pos)
```

#### 3、其他接口

`heapify`(*x*) ：线性时间内（O(len(n))，将list原地转换成堆。当对一个列表做多次堆操作时，可以将其先转换成堆，可以加快执行速度。

`heappushpop`(*heap*, *item*) : 将 item 放入堆中，然后弹出并返回 heap 的最小元素。该组合操作比先调用  heappush() 再调用 heappop() 运行起来更有效率。 用这个操作可以将新元素和原有堆中最小元素中，较大的那个留在堆中。

`heapreplace`(*heap*, *item*) ： 弹出并返回 *heap* 中最小的一项，同时推入新的 *item*。 堆的大小不变。 这个单步骤操作比 [`heappop()`](https://docs.python.org/zh-cn/3/library/heapq.html#heapq.heappop) 加 [`heappush()`](https://docs.python.org/zh-cn/3/library/heapq.html#heapq.heappush) 更高效，并且在使用固定大小的堆时更为适宜。 pop/push 组合总是会从堆中返回一个元素并将其替换为 *item*。 

nlargest(*n*, *iterable*, *key=None*)和nsmallest`(*n*, *iterable*, *key=None*）：返回前n个最大元素或前n个最小元素组成的列表。

可以通过key元素来指定排序的依据：当存在key参数时，可以对更复杂的数据结构，返回根据某一个元素排序后的结果，例如下面这个例子，堆由一个字典组成的列表构造，可以根据字典中price的值来查找：

```python
import heapq

portfolio = [
   {'name': 'IBM', 'shares': 100, 'price': 91.1},
   {'name': 'AAPL', 'shares': 50, 'price': 543.22},
   {'name': 'FB', 'shares': 200, 'price': 21.09},
   {'name': 'HPQ', 'shares': 35, 'price': 31.75},
   {'name': 'YHOO', 'shares': 45, 'price': 16.35},
   {'name': 'ACME', 'shares': 75, 'price': 115.65}
]

cheap = heapq.nsmallest(3, portfolio, key=lambda s: s['price'])
expensive = heapq.nlargest(3, portfolio, key=lambda s: s['price'])

print(cheap)
print(expensive)
```

返回结果

```python
[{'name': 'YHOO', 'shares': 45, 'price': 16.35}, {'name': 'FB', 'shares': 200, 'price': 21.09}, {'name': 'HPQ', 'shares': 35, 'price': 31.75}]
[{'name': 'AAPL', 'shares': 50, 'price': 543.22}, {'name': 'ACME', 'shares': 75, 'price': 115.65}, {'name': 'IBM', 'shares': 100, 'price': 91.1}]
```

### 2、优先级队列（Priority Queue）

通过使用二叉堆heapq可以实现优先级队列，每次 pop操作都返回队列中优先级最高的元素。并且，优先级队列应当满足排序的稳定性，即两个优先级相同的任务，按照被加入时的顺序返回。一个简单的优先级队列的实现（来自[Python cookbook](https://python3-cookbook.readthedocs.io/zh_CN/latest/c01/p05_implement_a_priority_queue.html))

```python
class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]
```

heappush(heap,item) 方法接收的item可以是一个元组，这样当需要插入一个元素时，会依次比较元组中的每一个元素，如果相同或元素不可比较则比较下一个元素。由于这个原理，可以在队列中为每一个元素指定一个唯一的index值，这样对于值相同的元素，插入时不会出现 TypeError: unorderable types: Item() < Item() 错误，并且能够保证元素插入时的稳定性。

## 七、树（Tree）

### 1、树节点的数据结构

树节点的数据结构定义如下：

```python
class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
```

### 2、二叉树的创建

定义一个Tree结构和一个辅助队列，队列中存放当前节点中left或right至少有一个为None的节点。add()接口定义了如何插入一个元素：将新节点加入队列，队首节点无左子树，则元素插入到队首节点的左子树，否则插入队首节点的右子树，并从队列中弹出队首节点。

```python
class Tree:
    def __init__(self):
        self.root = None
        self.nodes = []

    def add(self, elem):
        node = Node(elem)
        self.nodes.append(node)
        if not self.root:
            self.root = node            
        else:
            if not self.nodes[0].left:
                self.nodes[0].left = node
            else:
                self.nodes[0].right = node
                self.nodes = self.nodes[1:]
```

创建树的函数可以如下定义：输入为一个可迭代的序列，输出为树的root节点，输出的数据类型为Node.

```python
def create_tree(data) -> Node:
    t = Tree()
    for v in data:
        t.add(v)
    return t.root
```

### 3、二叉树的遍历

二叉树的前、中、后序遍历，是指遍历结果中根节点的位置。

1、前序遍历

前序遍历顺序为根-左-右，通过递归实现前序遍历：

```python
def pre_order(root: Node, data: list):
    if not root:
        return
    data.append(root)
    pre_order(root.left, data)
    pre_order(root.right, data)
```

也可以通过栈来实现树节点的缓存，栈中元素的弹出顺序即为遍历结果，但在入栈时要先压入右子树，再压入左子树，这样在弹出时才能先弹出左子树的节点。

```python
def pre_order_stack(root: Node):
    stack = []
    stack.append(root)
    data = []
    while stack:
        cur = stack.pop()
        data.append(cur)
        if cur.right:
            stack.append(cur.right)
        if cur.left:
            stack.append(cur.left)
    return data
```

2、中序遍历

中序遍历的顺序为 左-根-右，递归的实现与前序遍历类似，将节点加入结果的操作放在左右子树的递归操作之间。中序遍历一个二叉查找树，返回的即为顺序排序后的序列。

```python
def in_order(root: Node, data: list):
    if not root:
        return
    in_order(root.left, data)
    data.append(root)
    in_order(root.right, data)
```

而用栈来实现中序遍历，用cur记录当前的节点，当前节点无左子树时，弹出该节点，cur指向栈顶元素的右子树，如果右子树也为空，则再弹出一个节点。

```python
def in_order_stack(root: Node):
    stack = []
    data = []
    cur = root
    while stack or cur:
        while cur:
            stack.append(cur)
            cur = cur.left
        top = stack.pop()
        data.append(top)
        cur = top.right
    return data
```

3、后序遍历

后序遍历结果为左-右-根，递归：

```python
def post_order(root: Node, data: list):
    if not root:
        return
    post_order(root.left, data)
    post_order(root.right, data)
    data.append(root)
```

使用栈进行后续遍历，与先序遍历类似，除了cur节点加入结果列表这一步，放在左右子树入栈之后。以及result列表需要逆序输出，因为根元素总是更先被加入结果列表。

```python
def post_order_stack(root: Node):
    stack = []
    data = []
    stack.append(root)
    while stack:
        cur = stack.pop()
        if cur.left:
            stack.append(cur.left)
        if cur.right:
            stack.append(cur.right)
        data.append(cur)
    return data[::-1]
```

4、层序遍历

层序遍历使用队列，依次将队首节点的左右子树加入队列，然后弹出队首节点。

与前序、中序、后续遍历不同，它们使用的是DFS（深度优先遍历），而层序遍历使用的是BFS（广度优先遍历）。

在python中可以借助collections.deque作为队列的数据结构，它在双端的插入和弹出操作性能优于list。插入：list.append() / deque.append() ，弹出： list.pop(0) / deque.popleft().

```python
def bfs(root: Node):
    if not root:
        return []
    queue = deque()
    queue.append(root)
    data = []
    while queue:
        cur = queue.popleft()
        data.append(cur)
        if cur.left:
            queue.append(cur.left)
        if cur.right:
            queue.append(cur.right)
    return data
```

### 4、二叉查找树（Binary Search Tree）

对有序结构（如数组）进行查找时，二分查找的复杂度是O(logn)，但要保证数组有序，排序操作的复杂度可能达到O(nlogn)，如果要在插入时保证数组有序，插入操作的复杂度为O(n).

如果需要支持高效的插入操作，需要引入一种链式数据结构（如：链表）。而链表无法通过索引直接获取到中间元素，只能沿链表遍历，因此查找的效率又会下降（只能使用顺序查找）。

二叉查找树能够同时获得二分查找的效率和链表插入的灵活性。二叉查找树的每个节点都大于其左子树的所有节点，并且小于其右子树的所有节点。

一个简单的二叉查找树的查找和排序操作如下，插入和查找操作通过递归来实现。

```python
class BST:
    def __init__(self):
        self.root = None

    def __len__(self):
        return len(self.root)

    def get(self, key):
        return self._get(self.root, key)

    def _get(self, root_node: Node, key):
        if not root_node:
            return None
        if key < root_node.val:
            return self._get(root_node.left, key)
        elif key > root_node.val:
            return self._get(root_node.right, key)
        return root_node.val

    def put(self, key, val):
        self.root = self._put(self.root, key, val)

    def _put(self, root_node: Node, key, val):
        if not root_node:
            return Node(key)
        if key < root_node.val:
            root_node.left = self._put(root_node.left, key, val)
        elif key > root_node.val:
            root_node.right = self._put(root_node.right, key, val)
        return root_node
```

这种方式在插入的数据是均匀的时候效率比较高，最好情况下树的高度为logN，而当插入顺序有序时达到最坏情况，树的高度与数据长度相同。



## 八、哈希表（Hash Table）

哈希表（也叫散列表）通过计算一个关于键值的函数，将数据映射到一个表，加快了查找速度。这个映射函数称作散列函数，存放记录的数组称作哈希表。

使用哈希表的查找算法分为两步：

（1）用散列函数将被查找的键转化为数组的一个索引

（2）处理碰撞冲突

python的set()和dict()都是通过hash来实现的，因此需要保证key是可hash的。

（可hash性： 如果一个对象在自己的生命周期中有一哈希值（hash value）是不可改变的，那么它就是*可哈希的*（hashable）的 。）

对于自定义的类，如果想要使用哈希表加快索引速度，可以通过重写hash()函数和eq()函数来实现。在将类的对象插入一个hash表（例如set或dict）时，会先根据hash()函数计算hash值，当hash值相同时再根据eq()函数比较对象是否相等，如果hash()和eq()的结果都相等，则认为是相同的对象。

例如，当不存在hash函数时，下面len(table)的结果会返回10，即set中插入了10个对象：

```python
class HashItem:
    def __init__(self, key, value):
        self.key = key
        self.value = value

if __name__ == '__main__':
    table = set()
    for i in range(10):
        item = HashItem(0, i)
        table.add(item)
    print(len(table))
```

而重写hash和eq函数后，len(table)的结果变为1，因为每次hash(key)的结果是同一个值，而eq函数比较的是key的值，所以key相同的元素其hash值和eq都相同，被视为同一个元素。

```python
class HashItem:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.key == other.key
        return False


if __name__ == '__main__':
    table = set()
    for i in range(10):
        item = HashItem(0, i)
        table.add(item)
    print(len(table))
```

而稍微修改一下eq函数，让其比较value的值模5的结果，len(table)的值变为5。

```python
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value % 5 == other.value % 5
        return False
```

注意，python3内部对于hash函数的处理，在单次运行时同一个键的hash结果是一致的，但是重新运行后值可能发生变化，例如在两个不同的解释器中执行hash('a')，结果如下：

```python
>>> hash('a')
1050036294

>>> hash('a')
-1314642242
```

因此，**不要尝试依赖系统固定的hash值**。

## 九、图

### 1、图的数据结构（邻接表）

采用set来表示邻接表

```python
"""
 无向图
"""
from collections import deque


class Graph:
    def __init__(self, V):
        self.V = V
        self.adjs = set()
        for i in range(self.V):
            self.adjs.append(set())
        self.E = 0

    def addEdge(self, v, w):
        self.valid_vertex(v)
        self.valid_vertex(w)
        self.adjs[v].add(w)
        self.adjs[w].add(v) # 有向图注释掉这行即可
        self.E += 1

    def adj(self, v):
        self.valid_vertex(v)
        return self.adjs[v]

    def valid_vertex(self, v):
        if v > self.V or v < 0:
            raise IndexError

    def __repr__(self):
        s = '{} verticles, {} edges\n'.format(self.V, self.E)
        for i in range(self.V):
            s += "{}: ".format(i)
            for w in self.adj(i):
                s += "{} ".format(w)
            s += "\n"
        return s

```

### 2、DFS（深度优先搜索）

采用递归实现DFS：

```python
class DepthFirstSearch:
    def __init__(self, graph: Graph, s: int):
        self.marked = [False] * graph.V
        self.count = 0
        graph.validate_vertex(s)
        self.dfs(graph, s)

    def dfs(self, graph: Graph, v: int):
        self.count += 1
        self.marked[v] = True
        [self.dfs(graph, w) for w in graph.adj(v) if not self.marked[w]]
```

也可以使用栈来实现DFS，每次弹出栈顶节点，然后将它的邻接点压入栈。

```python
    def dfs_with_stack(self, graph: Graph, v: int):
        visited, stack = set(), [v]
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                stack.extend(graph.adj(vertex) - visited)
        return visited
```

### 3、BFS（广度优先搜索）

使用队列来实现BFS，每次弹出队首节点，然后将它的邻接点加入队尾。

```python
class BreadFirstSearch:
    def __init__(self, graph: Graph, s: int):
        self.marked = [False] * graph.V
        self.edgeTo = [int] * graph.V
        self.distTo = [INFINITY] * graph.V
        graph.validate_vertex(s)
        self.bfs(graph, s)

    def bfs(self, graph: Graph, s: int):
        q = deque()
        self.marked[s] = True
        self.distTo[s] = 0
        q.append(s)
        while (q):
            v = q.pop()
            for w in graph.adj(v):
                if not self.marked[w]:
                    self.edgeTo[w] = v
                    self.distTo[w] = self.distTo[v] + 1
                    self.marked[w] = True
                    q.append(w)
```

### 4、拓扑排序

对有向无环图排序，可以使用DFS进行拓扑排序，有环图无法拓扑排序。 一幅有向图的拓扑顺序即为所有顶点的逆后序排列。 

拓扑排序可以用于解决调度问题。

使用深度优先算法获取所有顶点的后序排列，用栈存储后续排列结果，则栈的输出即为逆后序排列。

```python
class DepthFirstOrder:
    def __init__(self, graph: Graph):
        self.marked = [False] * graph.V
        self.reversePost = deque()
        for v in range(graph.V):
            if not self.marked[v]:
                self.dfs(graph, v)

    def dfs(self, graph: Graph, v: int):
        self.marked[v] = True
        for w in graph.adj(v):
            if not self.marked[w]:
                self.dfs(graph, w)
        self.reversePost.appendleft(v)
```

### 5、连通图

#### 无向图

增加一个id数组用来表示是图中的第几个连通图，size表示该点所在的连通图vertex的个数，count用来记录有几个连通图。初始化的时候使用DFS遍历整个图。

```python
class CC:
    def __init__(self, graph: Graph):
        self.marked = [False] * graph.V
        self.id = [0] * graph.V
        self.size = [0] * graph.V
        self.count = 0
        for v in range(graph.V):
            if not self.marked[v]:
                self.dfs(graph, v)
                self.count += 1

    def dfs(self, graph: Graph, v: int):
        graph.validate_vertex(v)
        self.marked[v] = True
        self.id[v] = self.count
        self.size[self.count] += 1
        for w in graph.adj(v):
            if not self.marked[w]:
                self.dfs(graph, w)

    def connected(self, v: int, w: int) -> bool:
        return self.id[v] == self.id[w]
```

#### 有向图

有向图的强连通分量（ strong component ）：v到w，w到v都有有向路径，则v和w是强连通的。

 Kosaraju-Sharir algorithm ：先获取当前G的反向图GR

Phase 1: run DFS on GR to compute reverse postorder.

对GR进行DFS，获取GR的拓扑排序。 

Phase 2: run DFS on G, considering vertices in order given by first DFS 

根据GR拓扑排序中节点的顺序，对G进行DFS，即可获得强连通分量的数量。

```python
class KosarajuSharirSCC:
    def __init__(self, graph: Graph):
        self.marked = [False] * graph.V
        self.id = [-1] * graph.V
        self.count = 0
        dfs = DepthFirstOrder(graph.__reversed__())
        for v in dfs.reversePost():
            if not self.marked[v]:
                dfs(graph, v)
                self.count += 1

    def dfs(self, g: Graph, v: int):
        self.marked[v] = True
        self.id[v] = self.count
        for w in g.adj(v):
            if not self.marked[w]:
                self.dfs(g, w)

    def strongly_connected(self, v: int, w: int):
        return self.id[v] == self.id[w]
```

原理：强连通性具有自反性、对称性和传递性，因此，一个有向图的强连通分量与其逆图的强连通分量相同。先对逆图求拓扑排序，再根据排序结果对原图进行DFS，可达的节点就在同一个全连通分量中。

