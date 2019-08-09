from WeightedQuickUnionUF import WeightedQuickUnionUF


class Percolation():
    def __init__(self, n):
        self.N = n
        self.TOP = 0
        # nodes: 1~n*n
        self.BOTTOM = n * n + 1
        self.uf_top_bottom = WeightedQuickUnionUF(n * n + 2)
        self.nodes_open = [None]+[False] * n * n

    def open(self, row, col):
        if not self.validate(row) or not self.validate(col):
            raise ValueError(
                'index is not between {} and {}'.format(1,self.N))
        index = self.transindex(row, col)
        self.nodes_open[index] = True
        if row == 1:
            self.uf_top_bottom.union(self.TOP, index)
        if row == self.N:
            self.uf_top_bottom.union(self.BOTTOM, index)

        around = []
        # calculate up,down,left,right, if in map: add to around list
        if self.validate(row - 1) and self.nodes_open[self.transindex(row-1,col)]:  # Up
            around.append(self.transindex(row - 1, col))
        if self.validate(row + 1) and self.nodes_open[self.transindex(row + 1, col)]:  # Down
            around.append(self.transindex(row + 1, col))
        if self.validate(col - 1) and self.nodes_open[self.transindex(row, col - 1)]:  # Left
            around.append(self.transindex(row, col - 1))
        if self.validate(col + 1) and self.nodes_open[self.transindex(row, col + 1)]:  # Right
            around.append(self.transindex(row, col + 1))

        for i in around:
            self.uf_top_bottom.union(i, index)

    def isOpen(self, row, col):
        if not self.validate(row) or not self.validate(col):
            raise ValueError(
                'index is not between {} and {}'.format(1,self.N))
        return self.nodes_open[self.transindex(row, col)]

    def isFull(self, row, col):
        if not self.validate(row) or not self.validate(col):
            raise ValueError(
                'index is not between {} and {}'.format(1,self.N))
        return self.uf_top_bottom.connected(self.TOP, self.transindex(row, col))

    def numberOfOpenSites(self):
        count = 0
        for i in self.nodes_open:
            if i:
                count += 1
        return count

    def percolates(self):
        return self.uf_top_bottom.connected(self.TOP, self.BOTTOM)

    def validate(self, p):
        minn = 1
        maxx = self.N
        if p < minn or p > maxx:
            return False
        return True

    def transindex(self, row, col):
        # self.validate(row)
        # self.validate(col)
        return (row - 1) * self.N + col


if __name__ == '__main__':
    pass
