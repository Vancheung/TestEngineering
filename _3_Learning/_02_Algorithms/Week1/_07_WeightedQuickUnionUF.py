class WeightedQuickUnionUF():
    def __init__(self, n):
        self.count = n
        self.parent = []
        self.size = []
        for i in range(n):
            self.parent.append(i)
            self.size.append(1)

    def count(self):
        return self.count

    def find(self, p):
        self.validate(p)
        while (p != self.parent[p]):
            p = self.parent[p]
        return p

    def validate(self, p):
        if p < 0 or p >= len(self.parent):
            raise ValueError('index {} is not between 0 and {}'.format(p, len(
                self.parent) - 1))

    def connected(self, p, q):
        return self.find(p) == self.find(q)

    def union(self, p, q):
        rootP = self.find(p)
        rootQ = self.find(q)
        if rootP == rootQ:
            return
        if self.size[rootP] < self.size[rootQ]:
            self.parent[rootP] = rootQ
            self.size[rootQ] += self.size[rootP]
        else:
            self.parent[rootQ] = rootP
            self.size[rootP] += self.size[rootQ]
        self.count -= 1

def batchConnect(uf, pqs):
    for t in pqs:
        p = t[0]
        q = t[1]
        if not uf.connected(p, q):
            try:
                uf.union(p, q)
            except Exception:
                break # raise time
        print(uf.parent,uf.size)
    return uf


if __name__ == '__main__':
    uf = WeightedQuickUnionUF(10)
    pqs1 = [(4, 3), (3, 8), (6, 5), (9, 4), (2, 1), (5, 0), (7, 2), (6, 1)]
    batchConnect(uf, pqs1)
    pqs2 = [(5, 0), (7, 2), (6, 1), (7, 3)]
    batchConnect(uf, pqs2)
