class Item():
    def __init__(self, item):
        self.item = item
        self.prev = None
        self.next = None


class ListIterator():
    def __init__(self, first):
        self.current = first

    def hasNext(self):
        return self.current != None

    def remove(self):
        raise UnsupportedOperationException

    def next(self):
        if not self.hasNext():
            raise NoSuchElementException
        item = self.current.item
        self.current = self.current.next
        return item


class Deque:
    def __init__(self):
        self.first = None
        self.last = None
        self.n = 0

    def isEmpty(self):
        return self.n == 0

    def size(self):
        return self.n

    def addFirst(self, item):
        # Add to Front
        if None == item:
            raise IllegalArgumentException
        oldfirst = self.first
        self.first = Item(item)
        self.first.next = oldfirst
        if self.isEmpty():
            self.last = self.first
        else:
            oldfirst.prev = self.first
        self.n += 1

    def addLast(self, item):
        # Add to Back
        if None == item:
            raise IllegalArgumentException
        oldlast = self.last
        self.last = Item(item)
        self.last.prev = oldlast
        if self.isEmpty():
            self.first = self.last
        else:
            oldlast.next = self.last
        self.n+=1

    def removeFirst(self):
        # pop front
        if self.isEmpty():
            raise NoSuchElementException
        item = self.first.item
        newfirst = self.first.next
        if newfirst:
            newfirst.prev = None
        else:
            self.last = None
        self.first = newfirst
        self.n -= 1
        return item

    def removeLast(self):
        if self.isEmpty():
            raise NoSuchElementException
        item = self.last.item
        newlast = self.last.prev
        if newlast:
            newlast.next = None
        else:
            self.first=None
        self.last = newlast
        self.n -= 1
        return item

    def iterator(self):
        # return a iter
        return ListIterator(self.first)


class IllegalArgumentException(Exception):
    pass


class NoSuchElementException(Exception):
    pass


class UnsupportedOperationException(Exception):
    pass


if __name__ == '__main__':
    deque = Deque()
    print(deque.size())
    deque.addFirst('item1')
    print(deque.removeLast())
    print(deque.size())
    deque.addFirst('item2')
    deque.addFirst('item3')
    it = deque.iterator()
    while it.hasNext():
        print(it.next())
    print(deque.size())
    print(deque.removeLast())
    print(deque.size())
    deque.addLast('item4')
    print(deque.size())
    print(deque.removeFirst())
    print(deque.removeFirst())
