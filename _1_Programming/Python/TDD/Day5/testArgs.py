import unittest
import Args

WRONG_FORMAT_ERROR = "Wrong format of argument!"

cmd = '-l -p 8080 -d /user/bin'


class testCases(unittest.TestCase):
    def testArgsInit(self):
        ar = Args.Args()
        self.assertIsNotNone(ar)
        self.assertEqual(ar.logging,False)

    def testSetLogging(self):
        log = True
        ar = Args.Args()
        ar.setLogging(log)
        self.assertEqual(ar.logging, True)
        assert(ar.setLogging('aa') == WRONG_FORMAT_ERROR)

    def testSetPort(self):
        port = 8080
        ar = Args.Args()
        ar.setPort(port)
        self.assertEqual(ar.port, 8080)
        ar.setPort('8081')
        self.assertEqual(ar.port, 8081)

        ar = Args.Args()
        assert (ar.setLogging('aa') == WRONG_FORMAT_ERROR)
        self.assertEqual(ar.port, None)

    def testSetDir(self):
        dir = '/user/bin'
        ar = Args.Args()
        ar.setDir(dir)
        self.assertEqual(ar.directory, '/user/bin')

    def testQuery(self):
        ar = Args.Args()
        log = True
        port = 8080
        dir = '/user/bin'
        ar.setLogging(log)
        ar.setPort(port)
        ar.setDir(dir)
        self.assertEqual(ar.Query('l'),True)
        self.assertEqual(ar.Query('p'),8080)
        self.assertEqual(ar.Query('d'),dir)
        self.assertEqual(ar.Query('m'), WRONG_FORMAT_ERROR)

    def testParse(self):
        ar = Args.Args()
        self.assertIsNotNone(ar.Parse(cmd))
        ar.genArgs()
        self.assertEqual(ar.Query('l'), True)
        self.assertEqual(ar.Query('p'), 8080)
        self.assertEqual(ar.Query('d'), dir)


if __name__ == '__main__':
    unittest.main()
