import unittest
import Args

cmd = '-l -p 8080 -d /user/bin'


class testCases(unittest.TestCase):
    def testParse(self):
        ar = Args.Args(cmd)
        self.assertIsNotNone(ar.Parse(), "Parse fail!")

    def testQuery(self):
        ar = Args.Args(cmd)
        # ar.Parse()
        self.assertEqual(ar.Query('m'), 'Arg name not found!')
        self.assertEqual(ar.Query('p'), 8080)
        self.assertEqual(ar.Query('d'), '/user/bin')

    def testDefault(self):
        ar = Args.Args(cmd)
        # ar.Parse()
        self.assertEqual(ar.Query('l'), True)


if __name__ == '__main__':
    unittest.main()
