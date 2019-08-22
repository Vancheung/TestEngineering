from random import randint
import sys
class RandomizedQueue():
    def __init__(self):
        self.items = [None] * 2
        self.n = 0

    def isEmpty(self):
        return self.n==0

    def size(self):
        return self.n

    def resize(self,capacity):
        if not isinstance(capacity,int):
            raise IllegalArgumentException
        copy = [None]*capacity
        for i in range(self.n):
            copy[i] = self.items[i]
        self.items = copy

    def enqueue(self,item):
        # double size when array is full
        if not item:
            raise IllegalArgumentException
        if self.n==len(self.items):
            self.resize(self.n*2)
        self.items[self.n] = item
        self.n+=1

    def dequeue(self):
        # halve size when array is 1/4 full
        if(self.isEmpty()):
            raise NoSuchElementException
        index = randint(0,self.n)
        item = self.items[index]
        if index!=self.n-1:
            self.items[index] = self.items[self.n-1]  # exchange items[index] and the last item
        self.items[self.n-1] = None
        self.n -= 1
        if self.n < (len(self.items)/4):
            self.resize(int(len(self.items)/2))
        return item

    def sample(self):
        if(self.isEmpty()):
            raise NoSuchElementException()
        return self.items[randint(0,self.n)]

    def iterator(self):
        return RandomizedQueueIterator(self)

class RandomizedQueueIterator():
    def __init__(self,rq):
        self.rdq = rq.items
        self.current = 0

    def hasNext(self):
        return self.current < len(self.rdq)

    def remove(self):
        raise UnsupportedOperationException

    def next(self):
        if not self.hasNext():
            raise NoSuchElementException
        item = self.rdq[self.current]
        self.current +=1
        return item

class IllegalArgumentException(Exception):
    pass
class NoSuchElementException(Exception):
    pass
class UnsupportedOperationException(Exception):
    pass

if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        data = f.readlines()
        rq = RandomizedQueue()
        for i in data:
            rq.enqueue(i)
        for j in range(int(sys.argv[2])):
            print(rq.dequeue())
