import pygame
from pygame.locals import *

class Set(pygame.sprite.Sprite):
    def __init__(self, map_size, image, floor, select, pos, e_attribute):
        pygame.sprite.Sprite.__init__(self)

        self.floor = floor
        self.pos = pos
        self.map_size = map_size
        #设置边缘位置
        self.distance = self.map_size[0] // 2, 0
        self.image = image

        self.select = select
        self.const_select = tuple(select)
        #怪物动作的图像坐标移动
        self.act_select = 1

        self.dead = False
      
        #怪物属性：[blood, attack, defense, money]
        self.attribute = e_attribute
        
        #建立框选矩形
        self.select_rect = pygame.Rect(0, 0, 0, 0)
        self.select_rect.width = 32
        self.select_rect.height = 32
        self.select_rect.top = self.select[1] * 32 - 32
        self.select_rect.left = self.select[0] * 32 - 32
        #复制所选图像
        self.capture = self.image.subsurface(self.select_rect).copy()

        #设置所选图像的位置
        self.rect = self.capture.get_rect()
        self.rect.left = self.distance[0] + self.pos[0] * 32
        self.rect.top = self.distance[1] + self.pos[1] * 32
        
        #标记非透明部分
        self.mask = pygame.mask.from_surface(self.capture)

    def select(self):
        self.select_rect.top = self.select[1] * 32 - 32
        self.select_rect.left = self.select[0] * 32 - 32
        #复制所选图像
        self.capture = self.image.subsurface(self.select_rect).copy()

        #设置所选图像的位置
        self.rect = self.capture.get_rect()
        self.rect.left = self.distance[0] + self.pos[0] * 32
        self.rect.top = self.distance[1] + self.pos[1] * 32
        
        #标记非透明部分
        self.mask = pygame.mask.from_surface(self.capture)
        
class Tower_wall(pygame.sprite.Sprite):
    def __init__(self, map_size, image, floor):
        pygame.sprite.Sprite.__init__(self)

        self.floor = floor
        self.map_size = map_size
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.top = 0
        self.rect.left = self.map_size[0] // 2

        #标记非透明部分
        self.mask = pygame.mask.from_surface(self.image)

class Tools(Set):
    def __init__(self, map_size, image, floor, select, pos, t_attribute):
        Set.__init__(self, map_size, image, floor, select, pos, t_attribute)

        #第一个表示索引，第二个表示增量
        self.add = self.attribute.get(tuple(self.select))
        
class Doors(Set):
    def __init__(self, map_size, image, floor, select, pos, d_attribute, magic_enemy):
        Set.__init__(self, map_size, image, floor, select, pos, d_attribute)

        self.collide = False
        self.add = self.attribute.get(self.const_select)

        #机关门检验
        self.magic_enemy = magic_enemy
        self.check_door = True
        self.play = False

    def act(self):
        if self.collide:
            self.select[1] = self.select[1] % 4 + 1
            Set.select(self)

    def check(self, enemy):
        #判断机关门是否打开
        self.check_door = True
        for each in enemy:
            #通过将enemy的选择位置作为索引来判断
            if each.floor == self.floor:
                if self.magic_enemy.get(each.const_select) == self.floor:
                    self.check_door = False

class Stairs(Set):
    def __init__(self, map_size, image, floor, select, pos):
        attribute = None
        Set.__init__(self, map_size, image, floor, select, pos, attribute)
        
