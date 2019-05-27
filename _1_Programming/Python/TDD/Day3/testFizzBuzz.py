import FizzBuzz as fz
import unittest

FIZZ = "Fizz"
BUZZ = "Buzz"
FIZZ_BUZZ = "FizzBuzz"



class testFizzBuzz(unittest.TestCase):
    def testFizzBuzz(self):
        d = {}
        d[1] = str(1)
        d[3] = FIZZ
        d[5] = BUZZ
        d[13] = FIZZ
        d[15] = FIZZ_BUZZ
        for i in (1, 3, 5, 15, 13):
            assert (d[i] == fz.FizzBuzz(i))


if __name__ == '__main__':
    unittest.main()
