'''
version 2: modify data structure, use tree
id[i] is parent of i
root of i is id[id[id[...id[i]...]]]
'''


# UF (int N): initialize union-find data structure with N objects(0~N-1)
# void union(int p,int q): to merge components containing p and q, set the id of p's root to the id of q's root
# boolean connected(int p,int q): if the p and q have the same root

class QuickFindUF():
    def __init__(self, N):
        self.id = []
        for i in range(N):
            self.id.append(i)

    def connected(self, p, q):
        return self.root(p) == self.root(q)

    def union(self, p, q):
        i = self.root(p)
        j = self.root(q)
        self.id[i] = j

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
        print(uf.id)
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
