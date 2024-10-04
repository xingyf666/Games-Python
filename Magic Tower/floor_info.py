import pygame
from pygame.locals import *
import floor_data
import enemy
import tower_wall
import main
import function

#各种图像
map_size = main.map_size
tools_image = main.tools_image
doors_image = main.doors_image
enemy_image = main.enemy_image
stairs_image = main.stairs_image
store_image = main.store_image
store_talk = main.store_talk

#每层地图的名称
tower_image = [ \
    'images\\map\\1.png', \
    'images\\map\\2.png', \
    'images\\map\\3.png', \
    'images\\map\\4.png', \
    'images\\map\\5.png', \
    'images\\map\\6.png', \
    'images\\map\\7.png', \
    'images\\map\\8.png', \
    'images\\map\\9.png', \
    'images\\map\\10.png', \
    ]

#怪物及其属性
#绿史莱姆[4, 1] #红史莱姆[3, 1]
#骷髅[8, 3] #骷髅战士[2, 5]
#小蝙蝠[9, 1]
#初级法师[8, 7]
#初级守卫[8, 11] #中级守卫[6, 11]
Enemy = []
enemy_attributes = floor_data.enemy
#这里加入怪物属性的字典：{怪物坐标 : [blood, attack, defense, money]}
e_attribute = { \
    (4, 1) : (35, 18, 1, 1), \
    (3, 1) : (45, 20, 2, 2), \
    (9, 1) : (35, 38, 3, 3), \
    (8, 7) : (60, 32, 8, 5), \
    (8, 3) : (50, 42, 6, 6), \
    (2, 5) : (55, 52, 12, 8), \
    (6, 11) : (100, 180, 110, 50), \
    (8, 11) : (50, 48, 22, 12), \
    (9, 3) : (100, 65, 15, 30), \
    }

#楼梯
Stairs = []
stairs_attributes = floor_data.stairs

#门以及机关门（选择和楼层）
Doors = []
doors_attributes = floor_data.doors
d_attribute = { \
    (1, 1) : [4, -1], \
    (2, 1) : [5, -1], \
    (3, 1) : [6, -1], \
    (6, 1) : [0, 0], \
    }

#指定怪物 : 楼层
magic_enemy = { \
    (6, 11) : 2, (8, 11) : 8, \
    (8, 3) : 10, (2, 5) : 10, \
    }

#楼层道具及其属性
#属性：[floor, select, pos]
Tools = []
tools_attributes = floor_data.tools
#索引为从道具池中选择的坐标，值为属性索引和增量
#道具书[1, 8] #记事本[2, 8]
#红血瓶[1, 2] #蓝血瓶[2, 2]
#红宝石[1, 1] #蓝宝石[2, 1]
#黄钥匙[1, 5] #蓝钥匙[2, 5] #红钥匙[3, 5]
#跳楼器[4, 12]
#铁剑[1, 13] #铁盾[1, 15]
t_attribute = { \
    (1, 2) : [0, 50], (2, 2) : [0, 200],\
    (1, 1) : [1, 2], \
    (2, 1) : [2, 2], \
    (4, 8) : [3, 500], \
    (1, 5) : [4, 1], \
    (2, 5) : [5, 1], \
    (3, 5) : [6, 1], \
    \
    (1, 13) : [1, 10], (1, 15) : [2, 10], \
    }

#特殊道具
Super_Tools = []
s_pos = [0, 0]
#索引为从道具池中选择的坐标
#道具书[1, 8] #记事本[2, 8]
#跳楼器[4, 12]
enemy_dict = { \
    (4, 1) : ('绿史莱姆', 35, 18, 1, 1), \
    (3, 1) : ('红史莱姆', 45, 20, 2, 2), \
    (9, 1) : ('小蝙蝠', 35, 38, 3, 3), \
    (8, 7) : ('初级法师', 60, 32, 8, 5), \
    (8, 3) : ('骷髅', 50, 42, 6, 6), \
    (2, 5) : ('骷髅战士', 55, 52, 12, 8), \
    (6, 11) : ('中级守卫', 100, 180, 110, 50), \
    (8, 11) : ('初级守卫', 50, 48, 22, 12), \
    (9, 3) : ('骷髅队长', 100, 65, 15, 30), \
    }

stairs_dict = { \
    1 : {'up' : [(2, 1)], 'down' : None}, \
    2 : {'up' : [(1, 10)], 'down' : [(1, 2), (2, 1)]}, \
    3 : {'up' : [(11, 10), (10, 11)], 'down' : [(2, 11)]}, \
    4 : {'up' : [(1, 10)], 'down' : [(11, 10)]}, \
    5 : {'up' : [(1, 2)], 'down' : [(2, 11)]}, \
    6 : {'up' : [(11, 10)], 'down' : [(1, 2)]}, \
    7 : {'up' : [(1, 2)], 'down' : [(11, 10)]}, \
    8 : {'up' : [(6, 2), (5, 1), (7, 1)], 'down' : [(1, 2), (2, 1)]}, \
    9 : {'up' : [(1, 10), (2, 11)], 'down' : [(5, 1), (6, 2), (7, 1)]}, \
    10 : {'up' : None, 'down' : [(1, 10)]}, \
    }

sup_attribute = { \
    (1, 8) : [None, None, enemy_dict], \
    (2, 8) : [5, [4, 9], None], \
    (4, 12) : [1, [2, 11], stairs_dict], \
    }


#NPC
NPC = []
npc_attributes = floor_data.npc
#这里加入怪物属性的字典：{怪物坐标 : [blood, attack, defense, money]}
#老人[6, 21] #商人[8, 21]
#道具书[1, 8] #跳楼器[4, 12]
#黄钥匙[1, 5] #蓝钥匙[2, 5]
n_attribute = { \
    (8, 21) : [1, None, [50, [1, (2, 5)]], None, None, None, [50, [1, (2, 5)]], [50, [5, (1, 5)]], None, None, None], \
    (6, 21) : [2, None, 1000, (1, 8), None, None, None, None, None, None, None], \
    }

old_talk_dict = { \
    2 : ['images\\old_talk\\old_talk_2.png'], \
    3 : ['images\\old_talk\\old_talk_3.png'], \
    4 : ['images\\old_talk\\old_talk_4.png'], \
    6 : ['images\\old_talk\\old_talk_6.png'], \
    }

trader_talk_dict = { \
    6 : ['images\\trader_talk\\trader_talk_6_no.png', 'images\\trader_talk\\trader_talk_6_yes.png'], \
    7 : ['images\\trader_talk\\trader_talk_7_no.png', 'images\\trader_talk\\trader_talk_7_yes.png'], \
    }

#商店
Store = []
store_attributes = floor_data.store

s_attribute = { \
    0 : [20, (map_size[0] // 2 + 200, 140)], \
    1 : [100, (map_size[0] // 2 + 230, 200)], \
    2 : [2, (map_size[0] // 2 + 230, 238)], \
    3 : [4, (map_size[0] // 2 + 230, 276)], \
    }

def set():
    for each in enemy_attributes:
        enemy_floor = each[0]
        enemy_select = each[1]
        enemy_pos = each[2]
        enemy_attribute = e_attribute.get(tuple(enemy_select))
        Enemy.append(enemy.Enemy(map_size, enemy_image, \
                                enemy_floor, enemy_select, enemy_pos, enemy_attribute))

    for each in tools_attributes:
        tools_floor = each[0]
        tools_select = each[1]
        tools_pos = each[2]
        Tools.append(tower_wall.Tools(map_size, tools_image, \
                                tools_floor, tools_select, tools_pos, t_attribute))

    for each in doors_attributes:
        doors_floor = each[0]
        doors_select = each[1]
        doors_pos = each[2]
        Doors.append(tower_wall.Doors(map_size, doors_image, \
                                doors_floor, doors_select, doors_pos, d_attribute, magic_enemy))

    for each in stairs_attributes:
        stairs_floor = each[0]
        stairs_select = each[1]
        stairs_pos = each[2]
        Stairs.append(tower_wall.Stairs(map_size, stairs_image, \
                                stairs_floor, stairs_select, stairs_pos))

    for each in npc_attributes:
        npc_floor = each[0]
        npc_select = each[1]
        npc_pos = each[2]
        npc_attribute = n_attribute.get(tuple(npc_select))
        if npc_attribute[0] == 0:
            talk_dict = steal_talk_dict
        elif npc_attribute[0] == 1:
            talk_dict = trader_talk_dict
        elif npc_attribute[0] == 2:
            talk_dict = old_talk_dict
        NPC.append(function.NPC(map_size, enemy_image, \
                                npc_floor, npc_select, npc_pos, npc_attribute, talk_dict))

    #获取键，这就是选择的坐标
    for each in sup_attribute.keys():
        select = each
        pos = sup_attribute[each][1]
        floor = sup_attribute[each][0]
        Super_Tools.append(function.Super_Tools(map_size, tools_image, floor, \
                                                select, pos, sup_attribute))

    for each in store_attributes:
        store_floor = each[0]
        store_select = each[1]
        store_pos = each[2]
        store_attribute = s_attribute
        Store.append(function.Store(map_size, store_image, \
                                store_floor, store_select, store_pos, store_talk, store_attribute))
