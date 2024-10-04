import pygame
from pygame.locals import *
import random
import sys
import hero
import tower_wall
import enemy
import floor_info
import time

pygame.init()
pygame.mixer.init()

bg_size = width, height = 624, 416
map_size = 416, 416
WHITE = 255, 255, 255
BLACK = 0, 0, 0
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255

screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption('魔塔')

pygame.mixer.music.load('music\\magic tower.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

fight_sound = pygame.mixer.Sound('music\\fight.wav')
fight_sound.set_volume(1)
defense_sound = pygame.mixer.Sound('music\\defense.wav')
defense_sound.set_volume(0.2)
open_sound = pygame.mixer.Sound('music\\open.wav')
open_sound.set_volume(0.4)
gain_sound = pygame.mixer.Sound('music\\gain.wav')
gain_sound.set_volume(0.4)

background = pygame.image.load('images\\background.png').convert_alpha()
map_wall = pygame.image.load('images\\map.png').convert_alpha()
hero_image = pygame.image.load('images\\hero.png').convert_alpha()
tools_image = pygame.image.load('images\\tools.png').convert_alpha()
doors_image = pygame.image.load('images\\doors.png').convert_alpha()
enemy_image = pygame.image.load('images\\enemy.png').convert_alpha()
stairs_image = pygame.image.load('images\\stairs.png').convert_alpha()
fight_image = pygame.image.load('images\\fight.png').convert_alpha()
dict_image = pygame.image.load('images\\dict.png').convert_alpha()
store_image = pygame.image.load('images\\store.png').convert_alpha()
store_talk = pygame.image.load('images\\store_talk.png').convert_alpha()
menu_image = pygame.image.load('images\\menu.png').convert_alpha()

def main():    
    #判断游戏是否运行
    running = True
    global restart
    restart = False

    #游戏名
    name_font = pygame.font.Font('font\\name_font.ttf', 40)
    name_text = name_font.render('魔塔', True, WHITE)

    #英雄属性
    life = 1000
    attack = 1000
    defense = 10
    money = 0
    yellow = 0
    blue = 0
    red = 0

    #初始化列表，用于构建英雄对象
    attribute_list = [life, attack, defense, money, yellow, blue, red ]
    
    #初始化面板属性
    hero_attribute = [ \
                      ['生命：' + str(life), (10, 50)], \
                      ['攻击：' + str(attack), (10, 80)], \
                      ['防御：' + str(defense), (10, 110)], \
                      ['金钱：' + str(money), (10, 140)], \
                      ['黄钥匙：' + str(yellow), (10, 280)], \
                      ['蓝钥匙：' + str(blue), (10, 310)], \
                      ['红钥匙：' + str(red), (10, 340)], \
                      ]
    attribute_text = []
    attribute_font = pygame.font.Font('font\\attribute_font.ttf', 25)
    #初始化面板文字对象
    for each in hero_attribute:
        attribute_text.append([attribute_font.render(each[0], True, WHITE), each[1]])

    #创建英雄对象
    hero_man = hero.Hero(map_size, hero_image, attribute_list)

    #数据初始化
    floor_info.set()

    #超级道具显示位置
    sup_tool_pos = [0, 0]
    
    #道具书的显示
    dict_open = False
    show = None
    show_font = pygame.font.Font('font\\show_font.ttf', 20)
    #basic基础坐标变量
    basic = 0
    #记录展示的怪物个数
    show_num = 0

    #跳楼器的作用
    jump_up =  False
    jump_down = True

    #楼层和已经到达的最高层
    floor = 1
    highest = floor

    #菜单显示
    show_menu = False

    #楼层显示
    floor_font = pygame.font.Font('font\\attribute_font.ttf', 30)
    
    #楼层地图
    Tower = []
    first_floor = 1
    #从第一层开始加入每层图像的对象
    for each in floor_info.tower_image:
        image = pygame.image.load(each).convert_alpha()
        Tower.append(tower_wall.Tower_wall(map_size, image, first_floor))
        first_floor += 1

    #载入对话图像
    for each in floor_info.NPC:
        #尝试获取楼层索引的图像，如果有，说明这个NPC是这一层的，载入相应的对话图像
        image_list = each.talk_dict.get(each.floor)
        if image_list:
            for image in image_list:
                each.talk_image_list.append(pygame.image.load(image).convert_alpha())

    #判断商店是否在对话，载入商店字体，记录购买次数
    store_trade = False
    store_font = pygame.font.Font('font\\talk_font.ttf', 16)
    buy_num = 1

    #英雄移动的方向及其对应的图像
    hero_up = 0
    hero_down = 0
    hero_left = 0
    hero_right = 0

    #判断是否对话
    listening = False
    #判断是否按键
    press = False

    #控制帧率的对象
    clock = pygame.time.Clock()

    #战斗间隔，战斗判断，锁定位置（记录战斗前的位置，用于返回），战斗锁（锁定const_pos）
    fighting_sep = 100
    fighting = False
    const_pos = None
    fighting_lock = False

    #每80毫秒触发英雄移动
    HEROMOVE = USEREVENT
    hero_sep = 120
    pygame.time.set_timer(HEROMOVE, hero_sep)

    #每200毫秒怪物动作
    ENEMYMOVE = USEREVENT + 1
    enemy_sep = 200
    pygame.time.set_timer(ENEMYMOVE, enemy_sep)

    #每80毫秒门打开
    DOOROPEN = USEREVENT + 2
    door_sep = 90
    pygame.time.set_timer(DOOROPEN, door_sep)
    
    #计时器的计时器，用来计时
    second = 0
    minute = 0
    hour = 0

    #计时器的数据
    time_font = pygame.font.Font('font\\attribute_font.ttf', 20)
    time_text = time_font.render('{:02.0f} : {:02.0f} : {:02.0f}'.format(hour, \
                                     minute, second), True, WHITE)
    
    TIMER = USEREVENT + 3
    timer = False
    time_sep = 1000
    pygame.time.set_timer(TIMER, time_sep)

    while running:                
        #记录英雄最初的位置
        hero_pos = hero_man.rect.center
        #更新战斗锁定位置
        if not fighting_lock:
            const_pos = hero_pos
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                #当滚轮上滑，道具书显示的基础坐标向上移动，但不能大于0
                if event.button == 4:
                    basic += 30
                    if basic > 0:
                        basic = 0
                #当滚轮下滑，道具书显示的基础坐标向下移动
                #但不能小于当最后一个怪物处于底层时的basic
                elif event.button == 5:
                    basic -= 30
                    if basic < show_num * (-90) + 416 and show_num * (-90) + 416 < 0:
                        basic = show_num * (-90) + 416
                    #当怪物数量较少，不能移动
                    elif show_num * (-90) + 416 >= 0:
                        basic = 0
            
            elif event.type == HEROMOVE:
                #获取键盘状态
                key_pressed = pygame.key.get_pressed()
                #移动时，每次检测都改变移动的图像
                #check记录移动的方向
                if key_pressed[K_w] and hero_man.move:
                    hero_up = (hero_up + 1) % 4
                    hero_man.select = [hero_up, 3]
                    hero_man.moveup()
                    hero_man.check = [1, 0, 0, 0]
                elif key_pressed[K_s] and hero_man.move:
                    hero_down = (hero_down + 1) % 4
                    hero_man.select = [hero_down, 0]
                    hero_man.movedown()
                    hero_man.check = [0, 1, 0, 0]
                elif key_pressed[K_a] and hero_man.move:
                    hero_left = (hero_left + 1) % 4
                    hero_man.select = [hero_left, 1]
                    hero_man.moveleft()
                    hero_man.check = [0, 0, 1, 0]
                elif key_pressed[K_d] and hero_man.move:
                    hero_right = (hero_right + 1) % 4
                    hero_man.select = [hero_right, 2]
                    hero_man.moveright()
                    hero_man.check = [0, 0, 0, 1]
                else:
                    #当不移动时，利用check选择对应方向的图像
                    if hero_man.check == [1, 0, 0, 0]:
                        hero_man.select = [0, 3]
                    elif hero_man.check == [0, 1, 0, 0]:
                        hero_man.select = [0, 0]
                    elif hero_man.check == [0, 0, 1, 0]:
                        hero_man.select = [0, 1]
                    elif hero_man.check == [0, 0, 0, 1]:
                        hero_man.select = [0, 2]
                    #刷新英雄图像
                    hero_man.stop()
                
            elif event.type == KEYDOWN:                        
                for each in floor_info.Super_Tools:
                    if each.get:
                        #道具书的使用，当按下K键，打开道具书，再次按下关闭
                        if each.const_select == (1, 8) and event.key == K_h:
                            basic = 0
                            dict_open = not dict_open
                        #跳楼器的使用
                        elif each.const_select == (4, 12):
                            distance = None
                            #默认移动距离/方向没有
                            #当按上箭头且楼层小于最高层时才能移动
                            if event.key == K_UP and floor < highest:
                                distance = 1
                            elif event.key == K_DOWN:
                                distance = -1

                            #如果触发了移动，调用相应的函数，刷新楼层和位置
                            if distance:
                                next_pos, floor = each.jump_tool(each, hero_man.rect, floor, distance)

                                if next_pos:
                                    #如果发现英雄不在范围内，不移动
                                    hero_man.rect.left = next_pos[0] * 32 + 208
                                    hero_man.rect.top = next_pos[1] * 32

            elif event.type == KEYUP:
                if event.key == K_m:
                    show_menu = True
                    
                elif show_menu:
                    if event.key == K_1:
                        show_menu = False

                #商店的检测
                for each in floor_info.Store:
                    if each.talk:
                        buy = False
                        
                        if event.key == K_4:
                            each.talk = False
                            hero_man.move = True
                            break
                        #num是由于商店不同级别导致的资源差异
                        elif event.key == K_1 and hero_man.attribute[3] >= each.attribute[0][0]:
                            hero_man.attribute[0] += each.attribute[1][0] * each.num
                            buy = True
                        elif event.key == K_2 and hero_man.attribute[3] >= each.attribute[0][0]:
                            hero_man.attribute[1] += each.attribute[2][0] * each.num
                            buy = True
                        elif event.key == K_3 and hero_man.attribute[3] >= each.attribute[0][0]:
                            hero_man.attribute[2] += each.attribute[3][0] * each.num
                            buy = True

                        if buy:
                            #每次购买后价格上涨
                            hero_man.attribute[3] -= each.attribute[0][0]
                            each.attribute[0][0] += buy_num * 20
                            buy_num += 1
                                  
                if fighting:
                    #战斗退出指令
                    if event.key == K_q:
                        #按下Q键退出战斗，英雄返回原地，可以移动
                        fighting = False
                        fighting_lock = False
                        hero_man.rect.center = const_pos
                        hero_man.move = True

                if listening:
                    #当与NPC碰撞时，通过任意键继续
                    for each in floor_info.NPC:
                        #当处于对话，如果是老人，则停止对话
                        if each.old and event.key != K_a and event.key != K_w \
                                     and event.key != K_d and event.key != K_s:
                            each.talk = False
                            hero_man.move = True
                        #如果是商人
                        elif each.trader:
                            if each.talk:
                                #如果是正在对话的商人就不能移动
                                hero_man.move = False
                            else:
                                hero_man.move = True
                                
                            if each.talk and event.key != K_a and event.key != K_w \
                                     and event.key != K_d and event.key != K_s:
                                #按下Y键购买，花费金币，可以移动
                                if event.key == K_y and not each.buy:
                                    each.buy = True
                                    hero_man.attribute[3] -= each.price
                                #按下N键并且还没有购买时退出，对话停止
                                elif event.key == K_n and not each.buy:
                                    hero_man.move = True
                                    each.talk = False
                                #如果已经购买
                                if each.buy:
                                    press = True
                                    if each.talk_index != -1:
                                    #将图像索引向下一个移动，英雄可以移动
                                        each.talk_index += 1
                                    hero_man.move = True
                                    each.talk = False
                                    #如果这时存在道具，添加道具并移除
                                    if each.tool:
                                        hero_man.tools_set.add(each.tool)
                                        each.tool = None
                                    #道具/购买效果
                                    hero_man.tool(each.num)

            elif event.type == ENEMYMOVE:
                #怪物有两个移动图像，上下切换
                for each in floor_info.Enemy:
                    each.act()
                #NPC有两个移动图像，上下切换
                for each in floor_info.NPC:
                    each.act()
                #商店有两个移动图像，上下切换
                for each in floor_info.Store:
                    each.act()

            #作为门打开图像的延时
            elif event.type == DOOROPEN:
                for each in floor_info.Doors:
                    each.act()

            #这是一个计时器
            elif event.type == TIMER:
                #如果没有计时，则开始计时
                if not timer:
                    time_start = time.time()
                    timer = not timer
                else:
                    #结束计时
                    time_end = time.time()
                    #计时结果取整
                    second = int('{:.0f}'.format((time_end - time_start)))
                    
                    second = second % 60
                    minute = minute % 60
                    
                    if second == 0:
                        minute += 1
                        if minute == 60:
                            hour += 1
                            
                    time_text = time_font.render('{:02.0f} : {:02.0f} : {:02.0f}'.format(hour, \
                                                minute, second), True, WHITE)
        
        #面板属性刷新
        hero_attribute = [['生命：' + str(hero_man.attribute[0]), (10, 50)], \
                          ['攻击：' + str(hero_man.attribute[1]), (10, 80)], \
                          ['防御：' + str(hero_man.attribute[2]), (10, 110)], \
                          ['金钱：' + str(hero_man.attribute[3]), (10, 140)], \
                          ['黄钥匙：' + str(hero_man.attribute[4]), (10, 280)], \
                          ['蓝钥匙：' + str(hero_man.attribute[5]), (10, 310)], \
                          ['红钥匙：' + str(hero_man.attribute[6]), (10, 340)], \
                          ]

       #每次循环刷新属性数据
        for i in range(7):
            attribute_text[i] = ([attribute_font.render(hero_attribute[i][0], True, WHITE), \
                                  hero_attribute[i][1]])

        #与所在楼层的墙壁进行碰撞检测，若碰撞使其回到初始位置
        for each in Tower:
            if each.floor == floor:
                check_collide = pygame.sprite.collide_mask(hero_man, each)
                if check_collide:
                    hero_man.rect.center  = hero_pos

        #与所在楼层的普通门的碰撞检测，碰撞后门打开
        for each in floor_info.Doors:
            if each.floor == floor:
                #func函数从字典中寻找门效果（消耗对应的钥匙）
                check_collide = pygame.sprite.collide_mask(hero_man, each)
                if check_collide:
                    hero_man.rect.center = hero_pos
                    #注意这里要判断add是否存在，因为门打开的坐标不在字典内
                    if each.add and hero_man.attribute[each.add[0]] > 0 and not each.play:
                        #播放开门音效
                        open_sound.play()
                        each.play = True
                        hero_man.attribute[each.add[0]] += each.add[1]
                        each.collide = True                 

        #与机关门的解锁
        for each in floor_info.Doors:
            if each.floor == floor:
                #机关门的问题
                if not each.add:
                    each.check(floor_info.Enemy)
                    if each.check_door:
                        if not each.play:
                            open_sound.play()
                            each.play = True
                            
                        each.collide = True 

        #与所在楼层的道具的碰撞检测，碰撞后触发道具效果，最后移除道具
        for each in floor_info.Tools:
            if each.floor == floor:
                check_collide = pygame.sprite.collide_mask(hero_man, each)
                if check_collide:
                    gain_sound.play()
                    #如果这个道具有效果则触发
                    if each.add:
                        hero_man.attribute[each.add[0]] += each.add[1]
                    #移除道具
                    floor_info.Tools.remove(each)

        #与所在楼层的超级道具的碰撞检测，碰撞后获取
        for each in floor_info.Super_Tools:
            if each.floor == floor:
                check_collide = pygame.sprite.collide_mask(hero_man, each)
                if check_collide:
                    gain_sound.play()
                    #获取后标记超级道具已得到，输入显示的位置
                    #道具栏显示的位置向右移动，当移动到第5个时移动到下一行
                    each.get = True
                    each.get_tool(sup_tool_pos)
                    sup_tool_pos[0] += 1
                    if sup_tool_pos[0] == 5:
                        sup_tool_pos[1] += 1
                        sup_tool_pos[0] = 0

        #与所在楼层的怪物的碰撞检测，碰撞后进行战斗（英雄先攻）
        for each in floor_info.Enemy:
            if each.floor == floor:
                check_collide = pygame.sprite.collide_mask(hero_man, each)
                if check_collide:
                    #进入战斗，记录战斗前的位置
                    fighting = True
                    fighting_lock = True
                    
                    #战斗时不能移动
                    hero_man.move = False
                    fighting_sep -= 1
                    #通过sep控制战斗间隔
                    if fighting_sep % 5 == 0:
                        fight_sound.play()
                        each.fight(hero_man.attribute[1])
                        if each.dead:
                            #怪物死了就不能再发起攻击，锁定解除，获得金币
                            hero_man.move = True
                            fighting_lock = False
                            fighting_sep = 1000
                            hero_man.attribute[3] += each.attribute[3]
                            floor_info.Enemy.remove(each)
                            fighting = False
                        else:
                            hero_man.fight(each.attribute[1])
                            defense_sound.play()

        #与所在楼层的NPC的碰撞检测，碰撞后进行对话
        for each in floor_info.NPC:
            if each.floor == floor:
                check_collide = pygame.sprite.collide_mask(hero_man, each)
                if check_collide:
                    press = False
                    hero_man.rect.center = hero_pos
                    hero_man.move = False
                    each.talk = True
                    listening = True
                    #如果这是一个老人，并且老人有道具则给英雄加道具
                    if each.tool and each.old:
                        #获得道具名
                        tool = each.tool
                        
                        #如果是整型，说明是给钱！！！
                        if type(tool) == int:
                            hero_man.attribute[3] += tool
                            each.tool = None
                            
                        for each_tool in floor_info.Super_Tools:
                            #找到对应的道具，如果这个道具没有被获得则获得
                            if each_tool.select == tool and not each_tool.get:
                                each_tool.get = True
                                #改变道具的显示位置
                                each_tool.get_tool(sup_tool_pos)
                                #移动下一个道具坐标
                                sup_tool_pos[0] += 1
                                if sup_tool_pos[0] == 5:
                                    sup_tool_pos[1] += 1
                                    sup_tool_pos[0] = 0

        #与商店进行碰撞检测
        for each in floor_info.Store:
            if each.floor == floor:
                check_collide = pygame.sprite.collide_mask(hero_man, each)
                if check_collide:
                    hero_man.rect.center = hero_pos
                    hero_man.move = False
                    each.talk = True
                    store_trade = True
        
        #与所在楼层的楼梯的碰撞检测
        for each in floor_info.Stairs:
            if each.floor == floor:
                check_collide = pygame.sprite.collide_mask(hero_man, each)

                #如果碰撞，英雄身体转正，记录英雄移动后的位置pos，延时200毫秒
                if check_collide:
                    hero_man.check = [0, 1, 0, 0]
                    pos = hero_man.rect.center
                    hero_man.rect.center = hero_pos

                    #判断是下楼还是上楼
                    if each.select[0] == 1:
                        floor -= 1
                    else:
                        floor += 1
                        highest += 1

                    #上下楼后与所在位置进行碰撞检测
                    for each in Tower:
                        if each.floor == floor:
                            check_collide = pygame.sprite.collide_mask(hero_man, each)
                            #当发生碰撞，将英雄移回pos（楼梯位置），随机上下左右移动
                            while check_collide:
                                hero_man.rect.center = pos
                                move = random.choice([1, 2, 3, 4])
                                #随机移动，判断是否越界，若越界则不移动
                                if move == 1 and hero_man.rect.top >= 64:
                                    hero_man.rect.top -= 32
                                elif move == 2 and hero_man.rect.bottom <= 416 - 64:
                                    hero_man.rect.bottom += 32
                                elif move == 3 and hero_man.rect.left >= 208 + 64:
                                    hero_man.rect.left -= 32
                                elif move == 4 and hero_man.rect.right <= 624 - 64:
                                    hero_man.rect.right += 32
                                #如果没有发生移动/移动后碰撞就继续循环，若移动后不碰撞就跳出循环
                                if hero_man.rect.center != pos:
                                    check_collide = pygame.sprite.collide_mask(hero_man, each)

        screen.blit(background, (0, 0))
        screen.blit(map_wall, (map_size[0] // 2, 0))

        #显示该层的数据
        for each in floor_info.Tools:
            if each.floor == floor:
                screen.blit(each.capture, each.rect)

        for each in floor_info.Enemy:
            if each.floor == floor:
                screen.blit(each.capture, each.rect)

        for each in floor_info.Doors:
            if each.floor == floor:
                screen.blit(each.capture, each.rect)

        for each in floor_info.Stairs:
            if each.floor == floor:
                screen.blit(each.capture, each.rect)

        for each in floor_info.NPC:
            if each.floor == floor:
                screen.blit(each.capture, each.rect)

        for each in floor_info.Store:
            if each.floor == floor:
                screen.blit(each.capture, each.rect)

        #显示超级道具
        for each in floor_info.Super_Tools:
            if each.get:
                #当超级道具被获得后，显示图像（道具栏中）
                screen.blit(each.capture, each.rect)
            #当这个道具没被获得，但是它在这层楼存在，显示图像（楼层中）
            elif each.pos and each.floor == floor:
                screen.blit(each.capture, each.rect)

        #当门打开的图像移动到第四位时将其移除（这里要和上面分开，防止移除时的影响）
        for each in floor_info.Doors:
            if each.select[1] == 4:
                floor_info.Doors.remove(each)

        #显示当前楼层的图像
        for each in Tower:
            if each.floor == floor:
                screen.blit(each.image, each.rect)

        #显示英雄（额外加一个判断是否在对话，再加一个判断是否在打架）
        if (hero_man.move or listening or press) and not fighting:
            screen.blit(hero_man.capture, hero_man.rect)
        elif fighting_sep % 5 == 0:
            screen.blit(hero_man.capture, hero_man.rect)
        else:
            screen.blit(fight_image, hero_man.rect)

        #显示游戏名
        screen.blit(name_text, (10, 10))

        #显示属性
        for each in attribute_text:
            screen.blit(each[0], each[1])

        #显示楼层
        floor_text = floor_font.render('第{:02.0f}层'.format(floor), True, WHITE)
        screen.blit(floor_text, (100, 10))

        #显示计时器
        screen.blit(time_text, (10, 380))

        #显示超级道具内容
        for each in floor_info.Super_Tools:
            #默认什么都没有
            show = None
            if each.get:
                #如果有被获得的超级道具
                if each.const_select == (1, 8) and dict_open:
                    #这是道具书且道具书打开时的操作
                    #展示的数目清零，制作需要展示的怪物集合，以及为防止重复展示的怪物名集合
                    show_num = 0
                    enemy_set = set()
                    name_set = set()
                    #显示字典的背景图像
                    screen.blit(dict_image, (map_size[0] // 2, 0))
                    for enemy in floor_info.Enemy:
                        if enemy.floor == floor:
                            #对处在这一层的怪物进行判定，如果它的名字出现过就不重复加入
                            if enemy.const_select not in name_set:
                                name_set.add(enemy.const_select)
                                enemy_set.add(enemy)

                    #初始化用于展示的属性列表
                    enemy_list = []
                    enemy_set = list(enemy_set)
                    for enemy in enemy_set:
                        #将要展示的怪物集合中的怪物的截取位置和相应图像传入，记录个数
                        show_num += 1
                        enemy_list.append((enemy.const_select, enemy.const_image))

                    #使用作用函数，它返回在道具书对象中存在的怪物字典中对应怪物的属性列表
                    show = each.dict_tool(enemy_list, hero_man.attribute[1], hero_man.attribute[2])
                    #初始化位置
                    pos = 0
                    
                    for enemy in show:
                        #取出属性列表中的内容
                        name = enemy[0][0]
                        blood = enemy[0][1]
                        attack = enemy[0][2]
                        defense = enemy[0][3]
                        money = enemy[0][4]
                        image = enemy[1]
                        #lost是如果战斗会发生的损失
                        lost = enemy[2]

                        #判断lost的类型，如果是整型，根据损失大小改变提示文字的颜色
                        if type(lost) == int and lost < hero_man.attribute[0] * 0.2:
                            lost_text = show_font.render('你将损失{}点生命'.format(lost), True, GREEN)
                        elif type(lost) == int and lost < hero_man.attribute[0] * 0.5:
                            lost_text = show_font.render('你将损失{}点生命'.format(lost), True, BLUE)
                        elif type(lost) == int:
                            lost_text = show_font.render('你将损失{}点生命'.format(lost), True, RED)
                        #当lost不是整型，这就是不可攻击的对象/无损失
                        elif lost == '无损失':
                            lost_text = show_font.render('{}'.format(lost), True, GREEN)
                        else:
                            lost_text = show_font.render('{}'.format(lost), True, RED)

                        #载入需要展示的内容
                        show_text_1 = show_font.render('{}'.format(name), True, WHITE)
                        show_text_2 = show_font.render('血量：{}  攻击：{}'.format( \
                                blood, attack), True, WHITE)
                        show_text_3 = show_font.render('防御：{}  金币：{}'.format( \
                                defense, money), True, WHITE)

                        #引入变量basic作为滑动的基础坐标（第一个怪物的顶层坐标）
                        #pos用于排列每次显示的怪物内容
                        #每个怪物介绍要占用90像素，pos每次加3
                        screen.blit(image, (map_size[0] // 2 + 5, basic + pos * 30 + 5))
                        screen.blit(show_text_1, (map_size[0] // 2 + 35 + 5, basic + pos * 30 + 5))
                        screen.blit(show_text_2, (map_size[0] // 2 + 130, basic + pos * 30 + 5))
                        screen.blit(show_text_3, (map_size[0] // 2 + 130, basic + (pos + 1) * 30 + 5))
                        screen.blit(lost_text, (map_size[0] // 2 + 35 + 5, basic + (pos + 2) * 30 + 5))
                        pos += 3

                    #显示右侧的滚动条
                    line_length = 2 * height - show_num * 90
                    pygame.draw.line(screen, GREEN, (width-10, -basic), \
                                     (width-10, -basic + line_length), 10)


        #NPC对话
        for each in floor_info.NPC:
            if each.talk and not press:
                listening = True
                #加一个防报错机制
                try:
                    #尝试显示一个索引的对话图，这时不能移动
                    screen.blit(each.talk_image_list[each.talk_index], (208, 0))
                    hero_man.move = False
                except:
                    #如果尝试失败，说明索引越界，图像索引移动到最后一个
                    each.talk_index = -1
                    #此时所有NPC标记为停止对话状态（血的教训！！！）
                    for each_npc in floor_info.NPC:
                        each_npc.talk = False

        #与商店进行对话的显示
        for each in floor_info.Store:
            if each.floor == floor and each.talk:
                screen.blit(each.store_talk, (map_size[0] // 2, 0))
                talk_text = store_font.render('{}'.format(each.attribute[0][0]), True, BLACK)
                talk_rect = talk_text.get_rect()
                talk_rect.center = each.attribute[0][1]
                screen.blit(talk_text, talk_rect)

                for i in range(3):
                    talk_text = store_font.render('{}'.format(each.attribute[i+1][0] * each.num), \
                                                  True, BLACK)
                    talk_rect = talk_text.get_rect()
                    talk_rect.left, talk_rect.top = each.attribute[i+1][1]
                    screen.blit(talk_text, talk_rect)

        #显示菜单
        if show_menu:
            screen.blit(menu_image, (208, 0))
        
        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    main()
