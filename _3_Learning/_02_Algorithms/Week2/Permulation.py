import sys
from Week2.RandomizedQueue import RandomizedQueue
if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        data = f.readlines()
        rq = RandomizedQueue()
        for i in data:
            rq.enqueue(i)
        for j in range(sys.argv[2]):
            rq.dequeue()

