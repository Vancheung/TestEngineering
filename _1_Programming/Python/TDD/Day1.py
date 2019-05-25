def FizzBuzz(n):
    result = ''
    if (n % 3 == 0) or ('3' in str(n)):
        result += 'Fizz'
    if (n % 5 == 0) or ('5' in str(n)):
        result += 'Buzz'

    if result == '':
        result += str(n)
    return result


def testFizzBuzz():
    d = {}
    # for i in range(100):
    #     d.setdefault(str(i),i)
    d['1'] = '1'
    d['3'] = 'Fizz'
    d['5'] = 'Buzz'
    d['15'] = 'FizzBuzz'
    d['13'] = 'Fizz'

    for i in (1, 3, 5, 13, 15):
        assert (FizzBuzz(i) == d[str(i)])


if __name__ == '__main__':
    testFizzBuzz()
