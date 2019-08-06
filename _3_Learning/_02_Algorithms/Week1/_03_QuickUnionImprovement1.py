'''
version 3: weighted quick-union, always make the smaller tree below
O(union): depth of tree = lg(N)
O(connected): lg(N)
'''


# UF (int N): initialize union-find data structure with N objects(0~N-1)
# void union(int p,int q): link root of smaller tree to root of larger tree, update the sz[] array
# boolean connected(int p,int q): if the p and q have the same root

class QuickFindUF():
    def __init__(self, N):
        self.id = []
        self.sz = [] # tree size: the number of the elements in this root
        for i in range(N):
            self.id.append(i)
            self.sz.append(1)

    def connected(self, p, q):
        return self.root(p) == self.root(q)

    def union(self, p, q):
        i = self.root(p)
        j = self.root(q)
        if i==j:
            return
        if self.sz[i] < self.sz[j]:
            self.id[i] = j
            self.sz[j] += self.sz[i]
        else:
            self.id[j] = i
            self.sz[i] += self.sz[j]

    def root(self, i):
        while i != self.id[i]:
            i = self.id[i]
        return i


def batchConnect(uf, pqs):
    for t in pqs:
        p = t[0]
        q = t[1]
        if not uf.connected(p, q):
            uf.union(p, q)
        print(uf.id,uf.sz)
    return uf


if __name__ == '__main__':
    uf = QuickFindUF(10)
    pqs1 = [(4, 3), (3, 8), (6, 5), (9, 4), (2, 1), (5, 0), (7, 2), (6, 1)]
    batchConnect(uf, pqs1)
    assert uf.connected(8, 9) == True
    assert uf.connected(5, 4) == False
    pqs2 = [(5, 0), (7, 2), (6, 1), (7, 3)]
    batchConnect(uf, pqs2)
    assert uf.connected(5, 4) == True
