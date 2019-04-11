# -*- coding: utf-8 -*-
class Screen(object):
    @property
    def width(self):
        return self._width
    @width.setter
    def width(self,value):
        self._width = value

    @property
    def height(self):
        return self._height
    @height.setter
    def height(self,value):
        self._height = value

    @property
    def resolution(self):
        self._resolution = 786432
        return self._resolution


# 测试:
s = Screen()
s.width = 1024
s.height = 768
print(s.width,s.height)
print('resolution =', s.resolution)
if s.resolution == 786432:
    print('测试通过!')
else:
    print('测试失败!')
#s.resolution = 1
