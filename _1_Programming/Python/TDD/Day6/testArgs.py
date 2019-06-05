import unittest
from Schema import Schema
# from defaultMap import defaultMap
from Args import Args

sch = 'l:bool p:int d:str'
cmd = '-l -p 8080 -d /usr/logs'

class testCases(unittest.TestCase):
    def testInitArgs(self):
        schema = Schema('%s' % sch)
        self.assertIsNotNone(schema)

    def testWrongSchema(self):
        try:
            schema = Schema('l:boo')
        except TypeError as e:
            print(e)

    def testIsBoolean(self):        
        schema = Schema('%s' % sch)    
        self.assertTrue(schema.isBoolean('l',True))
        self.assertTrue(schema.isBoolean('l',False))
        self.assertFalse(schema.isBoolean('l',1))

    def testIsInt(self):        
        schema = Schema('%s' % sch)
        self.assertTrue(schema.isInt('p', 8000))
        self.assertFalse(schema.isInt('p', True))
        self.assertFalse(schema.isInt('p', 'str'))

    def testIsString(self):
        schema = Schema('%s' % sch)
        self.assertFalse(schema.isString('d', 8000))
        self.assertFalse(schema.isString('d', True))
        self.assertTrue(schema.isString('d', 'str'))

    def testArgs(self):
        schema = Schema('%s' % sch)
        arg = Args(schema,cmd)
        self.assertTrue(arg.isMatch())

        argwrong = Args(schema,'-l -p abc -d /usr/logs')
        try:
            argwrong.isMatch()
        except TypeError as e:
            print(e)

    def testArgsSetProperty(self):
        schema = Schema(sch)
        arg = Args(schema,cmd)
        arg.cmdParse(cmd)
        self.assertEqual(arg.logging,False)
        self.assertEqual(arg.port,None)
        self.assertEqual(arg.directory,None)
        arg.setProperty()
        self.assertEqual(arg.logging, True)
        self.assertEqual(arg.port, 8080)
        self.assertEqual(arg.directory, '/usr/logs')



if __name__ == '__main__':
    unittest.main()
