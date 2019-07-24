class Chain(object):

    def __init__(self, path='POST '):
        self._path = path

    def __getattr__(self, path):
        if path == 'users':
            return Chain('%s' % self._path).__getattr__ #直接使用users的值
        return Chain('%s/%s' % (self._path, path))

    def __str__(self):
        return self._path

    __repr__ = __str__

print(Chain().status.user.timeline.list)
print(Chain().status.users('Van').timeline.list)
