from Percolation import *
import unittest


class testCases(unittest.TestCase):
    def testValidate(self):
        pc = Percolation(4)
        self.assertFalse(pc.validate(0))
        # self.assertRaises(ValueError, pc.validate, 0)
        self.assertTrue(pc.validate(1))

    def testPercolates(self):
        pc = Percolation(4)
        self.assertFalse(pc.percolates())
        pc.uf_top_bottom.union(pc.TOP, pc.BOTTOM)
        self.assertTrue(pc.percolates())

    def testTransIndex(self):
        pc = Percolation(4)
        self.assertEqual(pc.transindex(1, 1), 1)
        self.assertEqual(pc.transindex(4, 4), 16)
        # self.assertRaises(ValueError, pc.transindex, 1, 0)
        # self.assertRaises(ValueError, pc.transindex, 4, 5)

    def testIsOpen(self):
        pc = Percolation(4)
        self.assertFalse(pc.nodes_open[2])
        pc.nodes_open[2] = True
        self.assertTrue(pc.nodes_open[2])

    def testNumberOfOpenSites(self):
        pc = Percolation(4)
        pc.nodes_open[3] = True
        self.assertEqual(pc.numberOfOpenSites(), 1)
        pc.nodes_open[15] = True
        self.assertEqual(pc.numberOfOpenSites(), 2)

    def testIsFull(self):
        pc = Percolation(4)
        p1 = pc.transindex(2, 1)
        p2 = pc.transindex(2, 2)
        p3 = pc.transindex(1, 2)
        pc.uf_top_bottom.union(p1, p2)
        self.assertFalse(pc.isFull(2, 1))
        self.assertFalse(pc.isFull(2, 2))
        pc.uf_top_bottom.union(p3, p2)
        self.assertFalse(pc.isFull(1, 2))
        pc.uf_top_bottom.union(p3, 0)
        self.assertTrue(pc.isFull(2, 1))
        self.assertTrue(pc.isFull(2, 2))
        self.assertTrue(pc.isFull(1, 2))

    def testOpen(self):
        pc = Percolation(4)
        opens = [(2,2),(2,3),(1,2),(3,4),(4,3),(3,3)]
        self.assertFalse(pc.percolates())
        for i in opens:
            pc.open(i[0],i[1])
            # print(pc.nodes_open)
            # print('IS PERCOLATE? {}'.format(pc.percolates()))
        self.assertTrue(pc.percolates())


if __name__ == '__main__':
    unittest.main()
