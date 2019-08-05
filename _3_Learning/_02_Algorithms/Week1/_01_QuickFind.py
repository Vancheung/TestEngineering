'''
Find Query:
Union Command
'''


# UF (int N): initialize union-find data structure with N objects(0~N-1)
# void union(int p,int q): add connection between p and q
# boolean connected(int p,int q): are q and q in the same component?

class QuickFindUF():
    def __init__(self, N):
        self.id = []
        for i in range(N):
            self.id.append(i)

    def connected(self, p, q):
        return self.id[p] == self.id[q]

    def union(self, p, q):
        pid = self.id[p]
        qid = self.id[q]
        for i in range(len(self.id)):
            if self.id[i] == pid:
                self.id[i] = qid


if __name__ == '__main__':
    # N = int(input())
    uf = QuickFindUF(10)
    pqs = [(4,3),(3,8),(6,5),(9,4),(2,1),(5,0),(7,2),(6,1)]
    for t in pqs:
        p = t[0]
        q = t[1]
        if not uf.connected(p, q):
            uf.union(p, q)
    print(uf.connected(8,9))
    print(uf.connected(1,0))
    print(uf.connected(6,7))
    print(uf.id)
