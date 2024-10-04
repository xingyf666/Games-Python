import pygame
from pygame.locals import *
import enemy
import tower_wall
import random
import math

class NPC(enemy.Set):
    def __init__(self, map_size, image, floor, select, \
                 pos, n_attribute, talk_dict):
        enemy.Set.__init__(self, map_size, image, floor, select, pos, n_attribute)

        #判断是否在对话，对话列表，没有道具
        self.talk = False
        self.talk_dict = talk_dict
        self.tool = None

        self.old = False
        self.trader = False

        self.price = 0
        self.num = 0

        if self.attribute[0] == 1:
            #这是商人，载入价格，数量，道具
            self.trader = True
            self.price = self.attribute[self.floor][0]
            self.num = self.attribute[self.floor][1][0]
            self.tool = self.attribute[self.floor][1][1]
        elif self.attribute[0] == 2:
            #这是老人，载入道具
            self.old = True
            self.tool = self.attribute[self.floor]

        #储存对话的图像，初始化索引，没有购买
        self.talk_image_list = []
        self.talk_index = 0
        self.buy = False
    
    def act(self):
        self.select[1] += self.act_select
        self.act_select = -1 * self.act_select

        enemy.Set.select(self)


class Store(pygame.sprite.Sprite):
    def __init__(self, map_size, image, floor, select, pos, store_talk, e_attribute):
        pygame.sprite.Sprite.__init__(self)

        self.floor = floor
        self.pos = pos
        self.map_size = map_size
        #设置边缘位置
        self.distance = self.map_size[0] // 2, 0
        self.image = image

        self.select = select
        self.const_select = tuple(select)

        self.act_select = 1

        self.num = pow(2, self.floor // 10)

        self.attribute = e_attribute

        self.talk = False
        self.store_talk = store_talk
        
        #建立框选矩形
        self.select_rect = pygame.Rect(0, 0, 0, 0)
        self.select_rect.width = 96
        self.select_rect.height = 32
        self.select_rect.top = self.select[1] * 32 - 32
        self.select_rect.left = self.select[0] * 96 - 96
        #复制所选图像
        self.capture = self.image.subsurface(self.select_rect).copy()

        #设置所选图像的位置
        self.rect = self.capture.get_rect()
        self.rect.left = self.distance[0] + self.pos[0] * 32
        self.rect.top = self.distance[1] + self.pos[1] * 32
        
        #标记非透明部分
        self.mask = pygame.mask.from_surface(self.capture)

    def act(self):
        self.select[1] += self.act_select
        self.act_select = -1 * self.act_select
        
        self.select_rect.top = self.select[1] * 32 - 32
        self.select_rect.left = self.select[0] * 96 - 96
        #复制所选图像
        self.capture = self.image.subsurface(self.select_rect).copy()

        #设置所选图像的位置
        self.rect = self.capture.get_rect()
        self.rect.left = self.distance[0] + self.pos[0] * 32
        self.rect.top = self.distance[1] + self.pos[1] * 32
        
        #标记非透明部分
        self.mask = pygame.mask.from_surface(self.capture)


class Super_Tools(tower_wall.Set):
    def __init__(self, map_size, image, floor, select, pos, s_attribute):
        #传入的pos不一定存在，如果是老人给的道具就没有pos
        if pos:
            tower_wall.Set.__init__(self, map_size, image, floor, select, pos, s_attribute)
        else:
            #没有pos就随便给一个
            pos = [0, 0]
            tower_wall.Set.__init__(self, map_size, image, floor, select, pos, s_attribute)

        #刷新pos为原先传入的内容，默认没有得到    
        self.pos = pos
        self.get = False
        #如果这是道具书，那么attribute就是怪物字典
        #如果是跳楼器，这就是一个楼层字典
        self.attribute = self.attribute[self.const_select][2]

    #当得到这个道具时调用，将道具位置移动到道具栏中
    def get_tool(self, pos):
        self.rect.left =  10 + pos[0] *32
        self.rect.top =  172 + pos[1] *32

    #道具发挥作用的函数
    def dict_tool(self, enemy, hero_attack, hero_defense):
        information = []
        #lost为损失
        lost = 0
        #each有两个元素，怪物属性和图像
        for each in enemy:
            #这里是从字典中调出对应位置的怪物属性
            enemy_attribute = self.attribute[each[0]]
            
            enemy_blood = enemy_attribute[1]
            enemy_attack = enemy_attribute[2]
            enemy_defense = enemy_attribute[3]

            if enemy_defense >= hero_attack:
                lost = '无法攻击！'
            else:
                #由于存在能否整除的问题，怪物的攻击次数会不同，这里进行调整
                remain = enemy_blood % (hero_attack - enemy_defense)
                if remain:
                    lost = enemy_blood // (hero_attack - enemy_defense) \
                           * (enemy_attack - hero_defense)
                else:
                    lost = (enemy_blood // (hero_attack - enemy_defense) - 1) \
                           * (enemy_attack - hero_defense)

                if lost <= 0:
                    lost = '无损失'

            #将怪物属性，怪物图像，损失作为元组传入
            information.append((enemy_attribute, each[1], lost))
                            
        return information

    def jump_tool(self, tool, hero_rect, floor, d):
        next_pos = None
        jump_list = None
        
        if d == 1:
            jump = 'down'
        else:
            jump = 'up'
            
        up_list = tool.attribute[floor]['up']
        down_list = tool.attribute[floor]['down']
        #分别判断英雄是否在上楼梯和下楼梯的位置，如果在，就获取上/下一层的楼梯字典
        if up_list:
            for pos in up_list:
                if pos[0] * 32 == hero_rect.left - 208 \
                    and pos[1] * 32 == hero_rect.top:
                    jump_list = tool.attribute.get(floor + d)
                            
        if down_list: 
            for pos in down_list:
                if pos[0] * 32 == hero_rect.left - 208 \
                    and pos[1] * 32 == hero_rect.top:
                    jump_list = tool.attribute.get(floor + d)

        #如果获取了楼层字典，楼层刷新，随机从中选择一个位置显示
        if jump_list:
            floor += d
            jump_list = tool.attribute[floor][jump]
                                                
            next_pos = list(random.choice(jump_list))

        return next_pos, floor

        
