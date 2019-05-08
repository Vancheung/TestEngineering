import functools

# 使用memorize 作为装饰器
# 先把100->1存入一个字典
# 到n=(0,1) 再返回
# 实现横切关注点
def memorize(fn):
    known = dict() # dict作为缓存

    @functools.wraps(fn)
    def memorizer(*args):  # 参数列表（被修饰函数可能有参数）
        if args not in known:   # 100 -> 1
            known[args] = fn(*args)
        return known[args]

    return memorizer

@memorize
def nsum(n):
    '''返回前n个数字之和'''
    assert(n>=0),'n must be >=0'
    return 0 if n==0 else n+nsum(n-1)

@memorize
def fibonacci(n):
    '''返回斐波那契数列的第n个数'''
    assert (n>=0),'n must be >=0'
    return n if n in (0,1) else fibonacci(n-1)+fibonacci(n-2)

def client():
    from timeit import Timer
    measure = [{'exec':'fibonacci(100)','import':'fibonacci','func':fibonacci},{'exec':'nsum(200)','import':'nsum','func':nsum}]

    for m in measure:
        t = Timer('{}'.format(m['exec']),'from __main__ import {}'.format(m['import']))
        print('name {}, doc: {}, executing: {}, time:{}'.format(m['func'].__name__,m['func'].__doc__,m['exec'],t.timeit()))

if __name__ == '__main__':
    client()
