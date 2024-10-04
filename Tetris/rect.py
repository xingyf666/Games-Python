import pygame
from pygame.locals import *
from random import *

heng_4 = pygame.image.load('images\\横4.png')
jiao_4 = pygame.image.load('images\\拐4.png')
jiaodui_4 = pygame.image.load('images\\拐对4.png')
jiao_2 = pygame.image.load('images\\拐2.png')
jiaodui_2 = pygame.image.load('images\\拐对2.png')
tian_4 = pygame.image.load('images\\田4.png')
tu_4 = pygame.image.load('images\\凸4.png')


class Rect(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        
        self.bg_size = bg_size
        self.speed = 30
        self.num = 0
        self.tip_pos = 810, 135

        choice_rect = choice([1, 2, 3, 4, 5, 6, 7])
        if choice_rect == 1:
            self.add_rect = heng_4
        elif choice_rect == 2:
            self.add_rect = jiao_4
        elif choice_rect == 3:
            self.add_rect = jiao_2
        elif choice_rect == 4:
            self.add_rect = tian_4
        elif choice_rect == 5:
            self.add_rect = tu_4
        elif choice_rect == 6:
            self.add_rect = jiaodui_2
        elif choice_rect == 7:
            self.add_rect = jiaodui_4

        choice_flip = choice([0, 90, 180, 270])
        self.add_rect = pygame.transform.rotate(self.add_rect, choice_flip)
        self.rect = self.add_rect.get_rect()
        self.tip = self.add_rect
        self.num = randint(0, (690 - self.rect.width) // 30)
        self.rect.left = self.num * 30
        self.rect.top = -90
        self.tip_rect = self.tip_pos[0] - self.rect.width // 2, \
                         self.tip_pos[1] - self.rect.height // 2
        #标记非透明部分
        self.mask = pygame.mask.from_surface(self.add_rect)


    def move(self):
        self.rect.top += self.speed

    def moveleft(self):
        if self.rect.left >= 30:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def moveright(self):
        if self.rect.right <= 660:
            self.rect.right += self.speed
        else:
            self.rect.right = 690

    def movedown(self):
        if self.rect.bottom + 90 <= self.bg_size[1]:
            self.rect.bottom += 90
        elif self.rect.bottom + 60 <= self.bg_size[1]:
            self.rect.bottom += 60
        elif self.rect.bottom + 30 <= self.bg_size[1]:
            self.rect.bottom += 30

    def to_bottom(self):
        if self.rect.bottom != self.bg_size[1]:
            self.rect.bottom = self.bg_size[1]

    def rect_change(self):
        top = self.rect.top
        left = self.rect.left
        self.add_rect = pygame.transform.rotate(self.add_rect, 90)
        self.rect = self.add_rect.get_rect()
        self.rect.top = top
        self.rect.left = left
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 690:
            self.rect.right = 690
        self.mask = pygame.mask.from_surface(self.add_rect)         
