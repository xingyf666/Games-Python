import pygame
from pygame.locals import *    

class Set(pygame.sprite.Sprite):
    def __init__(self, map_size, image, hero_attribute):
        pygame.sprite.Sprite.__init__(self)

        self.map_size = map_size
        #设置边缘位置
        self.distance = self.map_size[0] // 2, 0
        self.move_speed = 32
        self.speed = [0, -1 * self.move_speed]
        self.image = image
        #选择图像中合适位置的英雄
        self.select = [0, 0]

        #检查移动的方向
        self.check = [0, 0, 0, 0]

        #英雄持有的道具池
        self.tools_set = set()

        #道具池锁定
        self.tools_list = None

        #道具书的获得
        self.book = None

        #属性：[life, attack, defense]
        self.attribute = hero_attribute

        #是否死亡
        self.dead = False

        #是否能移动
        self.move = True

        #建立框选矩形
        self.select_rect = pygame.Rect(0, 0, 0, 0)
        self.select_rect.width = 32
        self.select_rect.height = 32
        self.select_rect.top = self.select[1] * 32
        self.select_rect.left = self.select[0] * 32
        #复制所选图像
        self.capture = self.image.subsurface(self.select_rect).copy()

        #设置所选图像的位置
        self.rect = self.capture.get_rect()
        self.rect.left = self.distance[0] + 6 * 32
        self.rect.top = self.distance[1] + self.map_size[1] - 64
        
        #标记非透明部分
        self.mask = pygame.mask.from_surface(self.capture)

    def select(self):
        self.select_rect.top = self.select[1] * 32
        self.select_rect.left = self.select[0] * 32
        #复制所选图像
        self.capture = self.image.subsurface(self.select_rect).copy()
        
        #标记非透明部分
        self.mask = pygame.mask.from_surface(self.capture)

class Hero(Set):
    def __init__(self, map_size, image, hero_attribute):
        Set.__init__(self, map_size, image, hero_attribute)

    def moveup(self):
        if self.rect.top > self.distance[1] + 32:
            self.speed = [0, -1 * self.move_speed]
            self.rect.center = self.rect.center[0] + self.speed[0], \
                               self.rect.center[1] + self.speed[1]
        else:
            self.rect.top = self.distance[1] + 32

        Set.select(self)

    def moveleft(self):
        if self.rect.left > self.distance[0] + 32:
            self.speed = [-1 * self.move_speed, 0]
            self.rect.center = self.rect.center[0] + self.speed[0], \
                               self.rect.center[1] + self.speed[1]
        else:
            self.rect.left = self.distance[0] + 32

        Set.select(self)

    def moveright(self):
        if self.rect.right < self.distance[0] + self.map_size[0] - 32:
            self.speed = [1 * self.move_speed, 0]
            self.rect.center = self.rect.center[0] + self.speed[0], \
                               self.rect.center[1] + self.speed[1]
        else:
            self.rect.right = self.distance[0] + self.map_size[0] - 32

        Set.select(self)

    def movedown(self):
        if self.rect.bottom < self.distance[1] + self.map_size[1] - 32:
            self.speed = [0, 1 * self.move_speed]
            self.rect.center = self.rect.center[0] + self.speed[0], \
                               self.rect.center[1] + self.speed[1]
        else:
            self.rect.bottom = self.distance[1] + self.map_size[1] - 32

        Set.select(self)

    #停止时选择对应方向的停止图像
    def stop(self):
        Set.select(self)

    def fight(self, enemy_attack):
        if enemy_attack > self.attribute[2]:
            self.attribute[0] -= enemy_attack - self.attribute[2]
        if self.attribute[0] <= 0:
            self.dead = True

    def tool(self, num):
        #道具池锁定
        self.tools_list = list(self.tools_set)

        for each in self.tools_list:
            check = False
            
            if each == (1, 5):
                self.attribute[4] += 1 * num
                check = True
            elif each == (2, 5):
                self.attribute[5] += 1 * num
                check = True
            elif each == (3, 5):
                self.attribute[6] += 1 * num
                check = True
            elif each == (1, 1):
                self.attribute[1] += 2 * num
                check = True
            elif each == (2, 1):
                self.attribute[2] += 2 * num
                check = True
            elif each == (2, 2):
                self.attribute[0] += 200 * num
                check = True

            if check:
                self.tools_list.remove(each)

        self.tools_set = set(self.tools_list)
        
