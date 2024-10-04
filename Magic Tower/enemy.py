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

        #锁定一个最初的位置
        self.const_select = tuple(select)

        self.dead = False

        #怪物动作的图像坐标移动
        self.act_select = 1
        
        #怪物属性：[blood, attack, defense, money]
        self.attribute = list(e_attribute)
        
        #建立框选矩形
        self.select_rect = pygame.Rect(0, 0, 0, 0)
        self.select_rect.width = 32
        self.select_rect.height = 32
        self.select_rect.top = self.select[1] * 33 + 1 - 33
        self.select_rect.left = self.select[0] * 33 + 1 - 33
        #复制所选图像
        self.capture = self.image.subsurface(self.select_rect).copy()

        self.const_image = self.capture

        #设置所选图像的位置
        self.rect = self.capture.get_rect()
        self.rect.left = self.distance[0] + self.pos[0] * 32
        self.rect.top = self.distance[1] + self.pos[1] * 32
        
        #标记非透明部分
        self.mask = pygame.mask.from_surface(self.capture)

    def select(self):
        self.select_rect.top = self.select[1] * 33 + 1 - 33
        self.select_rect.left = self.select[0] * 33 + 1 - 33
        #复制所选图像
        self.capture = self.image.subsurface(self.select_rect).copy()

        #设置所选图像的位置
        self.rect = self.capture.get_rect()
        self.rect.left = self.distance[0] + self.pos[0] * 32
        self.rect.top = self.distance[1] + self.pos[1] * 32
        
        #标记非透明部分
        self.mask = pygame.mask.from_surface(self.capture)

    
class Enemy(Set):
    def __init__(self, map_size, image, floor, select, pos, e_attribute):
        Set.__init__(self, map_size, image, floor, select, pos, e_attribute)

    def act(self):
        self.select[1] += self.act_select
        self.act_select = -1 * self.act_select

        Set.select(self)
        
    def fight(self, hero_attack):
        if self.attribute:
            if hero_attack > self.attribute[2]:
                self.attribute[0] -= \
                                hero_attack - self.attribute[2]
            if self.attribute[0] <= 0:
                self.dead = True
        
