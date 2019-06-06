import unittest
from Schema import Schema
from Args import *

sch = 'l:bool,p:int,d:str'
cmd = '-l -p 8080 -d /user/bin'


class testCases(unittest.TestCase):
    def testSchema(self):
        s = Schema(sch)
        self.assertEqual(type(s.schema), dict)
        self.assertEqual(s.getSchema('l'), bool)
        self.assertEqual(s.getSchema('p'), int)
        self.assertEqual(s.getSchema('d'), str)

    def testWrongSchemaParse(self):
        wrongsch = 'l:boo,p:int,d:str'
        try:
            Schema(wrongsch)
        except TypeError as e:
            print(e)

    def testOtherSchemaParse(self):
        othersch = 'l:boolean,p:INT,d:string'
        try:
            s = Schema(othersch)
            self.assertEqual(s.getSchema('l'), bool)
            self.assertEqual(s.getSchema('p'), int)
            self.assertEqual(s.getSchema('d'), str)
        except TypeError as e:
            print(e)

    def testArgs(self):
        arg = Args(cmd)
        self.assertIsNotNone(arg)
        # print(arg.cmdParse(cmd))
        self.assertEqual(type(arg.cmd), dict)

    def testIsMatch(self):
        arg = Args(cmd)
        schema = Schema(sch)
        self.assertTrue(arg.isMatch(schema))
        wrongarg = Args('-l -p aaa -d /user')
        try:
            wrongarg.isMatch(schema)
        except TypeError as e:
            print(e)

    def testSetProperty(self):
        arg = Args(cmd)
        schema = Schema(sch)
        self.assertEqual(arg.__getattribute__('logging'), False)
        self.assertEqual(arg.__getattribute__('port'), None)
        self.assertEqual(arg.__getattribute__('directory'), None)
        try:
            arg.setProperty(schema)
            self.assertEqual(arg.__getattribute__('logging'), True)
            self.assertEqual(arg.__getattribute__('port'), 8080)
            self.assertEqual(arg.__getattribute__('directory'), '/user/bin')
        except TypeError as e:
            print(e)

        other = Args('-p 8000 -d /user')
        other.setProperty(schema)
        self.assertEqual(other.__getattribute__('logging'), False)
        self.assertEqual(other.__getattribute__('port'), 8000)
        self.assertEqual(other.__getattribute__('directory'), '/user')


if __name__ == '__main__':
    unittest.main()
