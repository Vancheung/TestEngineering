import unittest
import kata.textetst_fixture


class testCases(unittest.TestCase):

    def testbaseline(self):
        kata.textetst_fixture.main()
        with open('baseline.txt', 'r') as base, open('out.txt', 'r') as new:
            self.assertEqual(base.readlines(), new.readlines())


if __name__ == '__main__':
    unittest.main()
