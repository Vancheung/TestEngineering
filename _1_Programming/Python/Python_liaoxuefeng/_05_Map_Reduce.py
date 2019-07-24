# -*- coding: utf-8 -*-
from functools import reduce

def normalize(name):
    return name.title()

# 测试:
L1 = ['adam', 'LISA', 'barT']
L2 = list(map(normalize, L1))
print(L2)


def prod(L):
    return reduce(lambda a,b:a*b,L)

print('3 * 5 * 7 * 9 =', prod([3, 5, 7, 9]))
if prod([3, 5, 7, 9]) == 945:
    print('测试成功!')
else:
    print('测试失败!')


DIGITS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}

def char2num(s):
    return DIGITS[s]

def str2float(s):
    s = s.split('.')
    s0 =  reduce(lambda x, y: x * 10 + y, map(char2num, s[0]))
    n = len(s[1])
    s1 = reduce(lambda x, y: x*10 + y, map(char2num, s[1]))
    return s0+ s1/(10**n)




print('str2float(\'123.456\') =', str2float('123.456'))
if abs(str2float('123.456') - 123.456) < 0.00001:
    print('测试成功!')
else:
    print('测试失败!')
