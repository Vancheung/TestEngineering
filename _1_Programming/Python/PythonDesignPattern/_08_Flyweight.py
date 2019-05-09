import random
from enum import Enum
import pygame
from pygame.locals import *

TreeType = Enum('TreeType','apple_tree cherry_tree peach_tree')

# 使用pygame 图像化
pygame.init()
screen = pygame.display.set_mode((800,800))

class Tree():
    pool = dict()
    # cls引用的是tree类
    def __new__(cls, tree_type):
        obj = cls.pool.get(tree_type,None)
        if not obj:  # 当客户端要创建一个tree实例时，检查是否创建过相同种类的对象
            obj = object.__new__(cls)
            cls.pool[tree_type] = obj
            obj.tree_type = tree_type
        return obj  # 创建过则直接返回之前创建的对象

    # 渲染同一个对象，age x y为非共享的变量（非固有属性），由客户端代码显式传递
    def render(self,age,x,y):
        print('render a tree of type {} and age {} at ({}, {})'.format(self.tree_type,age,x,y))
        
        surf = pygame.Surface((age,age))
        surf.fill((255,255,255))
        screen.blit(surf,(x,y))


def client():
    rnd = random.Random()
    age_min, age_max = 1,30
    min_point,max_point = 0,800
    tree_counter = 0

    for _ in range(10):
        t1 = Tree(TreeType.apple_tree)
        t1.render(rnd.randint(age_min,age_max),rnd.randint(min_point,max_point),rnd.randint(min_point,max_point))
        tree_counter += 1

    for _ in range(3):
        t2 = Tree(TreeType.cherry_tree)
        t2.render(rnd.randint(age_min, age_max), rnd.randint(min_point, max_point), rnd.randint(min_point, max_point))
        tree_counter += 1

    for _ in range(5):
        t3 = Tree(TreeType.peach_tree)
        t3.render(rnd.randint(age_min, age_max), rnd.randint(min_point, max_point), rnd.randint(min_point, max_point))
        tree_counter += 1

    print('trees rendered: {}'.format(tree_counter))
    print('trees actually created: {}'.format(len(Tree.pool)))

    t4 = Tree(TreeType.cherry_tree)
    t5 = Tree(TreeType.cherry_tree)
    t6 = Tree(TreeType.apple_tree)
    print('{} == {}? {}'.format(id(t4),id(t5),id(t4)==id(t5)))
    print('{} == {}? {}'.format(id(t5), id(t6), id(t5) == id(t6)))

    while True:
        pygame.display.flip()



if __name__ == '__main__':
    client()
