import pygame
from pygame.locals import *

pygame.init()

class Check(pygame.sprite.Sprite):
    def __init__(self, bg_size, image):
        pygame.sprite.Sprite.__init__(self)

        self.check_line = pygame.image.load(image).convert_alpha()
        self.rect = self.check_line.get_rect()
        self.rect.top = bg_size[1]
        self.rect.left = 0
        #标记非透明部分
        self.mask = pygame.mask.from_surface(self.check_line)

#碰撞检测
class Collide(pygame.sprite.Sprite):
    def __init__(self, move_rect, rect_group):
        pygame.sprite.Sprite.__init__(self)

        #传入移动的对象和方块组
        self.move_rect = move_rect
        self.rect_group = rect_group
        #定义两个方块底部坐标，rect表示移动前的位置，bottom表示移动后的位置
        self.rect = self.move_rect.rect.bottom
        self.bottom = self.move_rect.rect.bottom
        self.rect_collide = pygame.sprite.spritecollide(self.move_rect, self.rect_group, \
                                                   False, pygame.sprite.collide_mask)
        #check检测是否碰撞
        self.check = False

    def check_collide(self):
        #循环跳出条件
        go_out = False
        #检测碰撞前将自身移除
        self.rect_group.remove(self.move_rect)
        self.rect_collide = pygame.sprite.spritecollide(self.move_rect, self.rect_group, \
                                                   False, pygame.sprite.collide_mask)
        while not go_out:
            #当碰撞时，检测为碰撞，同时将物块上移直到不碰撞
            while self.rect_collide:
                self.check = True
                self.move_rect.rect.bottom -= 30
                self.bottom = self.move_rect.rect.bottom
                self.rect_collide = pygame.sprite.spritecollide(self.move_rect, self.rect_group, \
                                                           False, pygame.sprite.collide_mask)

            #当未碰撞/碰撞后移动到未碰撞位置时，将物块上移，检测这个过程中是否碰撞，直到发生
            #碰撞或物块回到移动前位置(rect)为止
            while not self.rect_collide and self.move_rect.rect.bottom >= self.rect - 30:
                self.move_rect.rect.bottom -= 30
                self.rect_collide = pygame.sprite.spritecollide(self.move_rect, self.rect_group, \
                                                           False, pygame.sprite.collide_mask)

            #如果物块因为碰撞跳出上面的循环，则继续循环
            #否则将物块移回第一次检测后的bottom位置并跳出循环
            if self.rect_collide:
                go_out = False
            else:
                self.move_rect.rect.bottom = self.bottom
                go_out = True

        #检测完毕后放回
        self.rect_group.append(self.move_rect)

        #如果检测到碰撞，则物块停止活动
        if self.check:
            self.move_rect.active = False

#清理物块
class Clear(pygame.sprite.Sprite):
    def __init__(self, check_clear, rect_group):
        pygame.sprite.Sprite.__init__(self)

        self.num = 0
        self.group = []
        self.check_clear = check_clear
        self.rect_group = rect_group
        self.top = 23
        self.left = 0
        self.count = 0
        #clear_bottom收集清理的图像的最大位置
        self.clear_bottom = 720
        #check判断是否进行了清理
        self.check = False

    def clear(self):
        self.count = 0
        self.top = 23
        self.left = 0
        #从第23行开始
        for i in range(24):
            self.num = 0
            self.group = []
            self.left = 0

            #从第1列开始
            for j in range(24):
                self.check_clear.rect.top = self.top * 30
                self.check_clear.rect.left = self.left * 30
                self.rect_collide = pygame.sprite.spritecollide(self.check_clear, self.rect_group, \
                                                           False, pygame.sprite.collide_mask)

                #如果碰撞，将碰撞的物块加入group，碰撞次数num加1
                if self.rect_collide:
                    for each in self.rect_collide:
                        if each not in self.group:
                            self.group.append(each)              
                    self.num += 1

                #向右移动
                self.left += 1

            #通过集合去掉重复加入的物块
            self.group = set(self.group)
            self.group = list(self.group)

            #如果碰撞了23次，这说明这一行都有物块，将在这一行的所有物块都从rect_group中取出
            if self.num == 23:
                self.check = True
                self.count += 1
                if (self.top + 1) * 30 >= self.clear_bottom:
                    self.clear_bottom = (self.top + 1) * 30
                for each in self.group:
                    self.rect_group.remove(each)

            #向上移动
            self.top -= 1
