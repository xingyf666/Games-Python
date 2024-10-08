#main.py

import pygame
import sys
import traceback
import myplane
import bullet
import enemy
import supply
from pygame.locals import *
from random import *

pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption('飞机大战')

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

background = pygame.image.load('images\\background.png').convert_alpha()

#载入游戏音乐
pygame.mixer.music.load('music\\KOTOKO.mp3')
pygame.mixer.music.set_volume(0.2)
bomb_sound = pygame.mixer.Sound('music\\bomb.wav')
bomb_sound.set_volume(0.2)
bigenemy_fly_sound = pygame.mixer.Sound('music\\震撼出场.wav')
bigenemy_fly_sound.set_volume(0.8)
smallenemy_down_sound = pygame.mixer.Sound('music\\smallenemy_down.wav')
smallenemy_down_sound.set_volume(0.2)
midenemy_down_sound = pygame.mixer.Sound('music\\midenemy_down.wav')
midenemy_down_sound.set_volume(0.3)
bigenemy_down_sound = pygame.mixer.Sound('music\\bigenemy_down.wav')
bigenemy_down_sound.set_volume(0.8)
me_down_sound = pygame.mixer.Sound('music\\me_down.wav')
me_down_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound('music\\转场.wav')
upgrade_sound.set_volume(0.8)
supply_sound = pygame.mixer.Sound('music\\supply.wav')
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound('music\\get_bomb.wav')
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound('music\\get_bullet.wav')
get_bullet_sound.set_volume(0.2)
bullet_sound = pygame.mixer.Sound('music\\bullet.wav')
bullet_sound.set_volume(0.05)
get_life_sound = pygame.mixer.Sound('music\\life.wav')
get_life_sound.set_volume(0.2)
button_sound = pygame.mixer.Sound('music\\按键.wav')
button_sound.set_volume(0.2)

class Again:
    restart = True

again = Again()

def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)

def add_big_enemies(group1, group2, num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)

def inc_speed(target, inc):
    for each in target:
        each.speed += inc
    

def main():
    pygame.mixer.music.play(-1)

    #生成我方飞机
    me = myplane.MyPlane(bg_size)

    #生成敌方飞机
    enemies = pygame.sprite.Group()

    #生成敌方小型飞机
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)

    #生成敌方中型飞机
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 4)

    #生成敌方大型飞机
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 2)

    #生成普通子弹
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 5
    for i in range(BULLET1_NUM):
        #子弹在飞机中央生成
        bullet1.append(bullet.Bullet1(me.rect.midtop))

    #生成超级子弹
    bullet2 = []
    bullet2_index = 0
    BULLET2_NUM = 10
    for i in range(BULLET2_NUM//2):
        #子弹在飞机两侧生成
        bullet2.append(bullet.Bullet2((me.rect.left + 8, me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.right - 8, me.rect.centery)))

    #中弹图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    #统计得分
    score = 0
    score_font = pygame.font.Font('font\\font.ttf', 30)

    #标志是否暂停游戏
    paused = False
    pause_nor_image = pygame.image.load('images\\pause_nor.png').convert_alpha()
    pause_pressed_image = pygame.image.load('images\\pause_pressed.png').convert_alpha()
    resume_nor_image = pygame.image.load('images\\resume_nor.png').convert_alpha()
    resume_pressed_image = pygame.image.load('images\\resume_pressed.png').convert_alpha()
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
    paused_image = pause_nor_image

    #设置难度级别
    level = 1

    #判断是否重启游戏
    start = True

    #用于切换图片
    switch_image = True

    #生命数量
    life_image = pygame.image.load('images\\life.png').convert_alpha()
    life_rect = life_image.get_rect()
    life_num = 3

    #加载结束界面
    again_nor_image = pygame.image.load('images\\again_nor.png').convert_alpha()
    again_press_image = pygame.image.load('images\\again_press.png').convert_alpha()
    again_rect = again_nor_image.get_rect()
    gameover_nor_image = pygame.image.load('images\\gameover_nor.png').convert_alpha()
    gameover_press_image = pygame.image.load('images\\gameover_press.png').convert_alpha()
    gameover_rect = gameover_nor_image.get_rect()
    end_score_font = pygame.font.Font('font\\font.ttf', 40)
    best_font = pygame.font.Font('font\\font.ttf', 50)

    again_image = again_nor_image
    gameover_image =  gameover_nor_image

    #用于阻止重复打开记录文件
    recorded = False

    #全屏炸弹
    bomb_image = pygame.image.load('images\\bomb.png').convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font('font\\font.ttf', 48)
    bomb_num = 3

    #每sep秒发放一个补给包
    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Bomb_Supply(bg_size)
    life_supply = supply.Life_Supply(bg_size)
    SUPPLY_TIME = USEREVENT
    sep = 30
    pygame.time.set_timer(SUPPLY_TIME, sep * 1000)
    remain_time = 1

    #超级子弹定时器
    DOUBLE_BULLET_TIME = USEREVENT + 1

    #标志是否使用超级子弹
    is_double_bullet = False

    #解除我方无敌状态定时器
    INVINCIBLE_TIME = USEREVENT + 2

    #判断是否播放按键音乐
    times = 1
    button_re = 0

    #用于延迟
    delay = 100

    running = True

    clock = pygame.time.Clock()

    while running:
        #计算补给剩余时间
        remain_time = (remain_time - 1 ) % sep
        
        #绘制背景
        screen.blit(background, (0, 0))
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            #当按下鼠标左键暂停
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        pygame.time.set_timer(SUPPLY_TIME, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        #计算补给剩余时间
                        remain_time = (remain_time - 1 ) % sep
                        pygame.time.set_timer(SUPPLY_TIME, remain_time * 1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
                        
                elif life_num == 0:
                    #获取鼠标位置，当鼠标在选框内时可以选择
                    mouse_pos = pygame.mouse.get_pos()
                    if event.button == 1 and width//2 - 95 < mouse_pos[0] < width//2 + 95 \
                                and height//2 - 72 < mouse_pos[1] < height//2 - 28:
                        start = False
                    elif event.button == 1 and width//2 - 95 < mouse_pos[0] < width//2 + 95 \
                                and height//2 + 28 < mouse_pos[1] < height//2 + 72:
                        again.restart = False
                    

            elif event.type == MOUSEMOTION:
                #当鼠标移动到暂停/开始按键上，按键加深
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image
                        
                #当鼠标移动到重新开始/结束游戏按键上，按键加深
                mouse_pos = pygame.mouse.get_pos()
                if width//2 - 95 < mouse_pos[0] < width//2 + 95 and \
                   height//2 - 72 < mouse_pos[1] < height//2 - 28:
                    again_image = again_press_image
                    button_re = 1 
                    
                elif width//2 - 95 < mouse_pos[0] < width//2 + 95 and  \
                   height//2 + 28 < mouse_pos[1] < height//2 + 72:
                    gameover_image =  gameover_press_image
                    button_re = 1 
                    
                else:
                    again_image = again_nor_image
                    gameover_image =  gameover_nor_image
                    times = 0
                    

            #按下空格键使用炸弹
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False

            #播放补给音效
            elif event.type == SUPPLY_TIME:
                supply_sound.play()
                choose = choice([1, 2, 3])
                if choose == 1:
                    bomb_supply.reset()
                elif choose == 2:
                    bullet_supply.reset()
                elif choose == 3:
                    life_supply.reset()

            #超级子弹计时
            elif event.type == DOUBLE_BULLET_TIME:
                is_double_bullet = False
                pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)

            #无敌计时器
            elif event.type == INVINCIBLE_TIME:
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME, 0)

                

        #根据用户得分增加难度
        if level == 1 and score > 50000:
            level = 2
            sep -= 5
            upgrade_sound.play()
            #增加3架小型敌机、2架中型敌机、1架大型敌机
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)
            #提升小型敌机的速度
            inc_speed(small_enemies, 1)
        elif level == 2 and score > 100000:
            level = 3
            sep -= 5
            upgrade_sound.play()
            #增加5架小型敌机、3架中型敌机、2架大型敌机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            #提升小、中型敌机的速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
        elif level == 3 and score > 300000:
            level = 4
            sep -= 5
            upgrade_sound.play()
            #增加8架小型敌机、5架中型敌机、3架大型敌机
            add_small_enemies(small_enemies, enemies, 8)
            add_mid_enemies(mid_enemies, enemies, 5)
            add_big_enemies(big_enemies, enemies, 3)
            #提升小、中型敌机的速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
            inc_speed(big_enemies, 1)
        elif level == 4 and score > 800000:
            level = 5
            sep -= 5
            upgrade_sound.play()
            #增加10架小型敌机、8架中型敌机、5架大型敌机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            #提升小、中、大型敌机的速度
            inc_speed(small_enemies, 2)
            inc_speed(mid_enemies, 1)
            inc_speed(big_enemies, 1)
                        

        if life_num and not paused:
            #检测用户的键盘操作
            key_pressed = pygame.key.get_pressed()

            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()

            #绘制全屏炸弹补给并检测是否获得
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                #只用检测两个物体，直接用collide_mask方法
                if pygame.sprite.collide_mask(bomb_supply, me):
                    get_bomb_sound.play()
                    bomb_num += 1
                    bomb_supply.active = False

            #绘制超级子弹补给并检测是否获得
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                #只用检测两个物体，直接用collide_mask方法
                if pygame.sprite.collide_mask(bullet_supply, me):
                    get_bullet_sound.play()
                    is_double_bullet = True
                    pygame.time.set_timer(DOUBLE_BULLET_TIME, 18 * 1000)
                    bullet_supply.active = False

            #绘制血量补给并检测是否获得
            if life_supply.active:
                life_supply.move()
                screen.blit(life_supply.image, life_supply.rect)
                #只用检测两个物体，直接用collide_mask方法
                if pygame.sprite.collide_mask(life_supply, me):
                    get_life_sound.play()
                    life_num += 1
                    life_supply.active = False
                    

            #发射子弹
            if not (delay % 10):
                bullet_sound.play()
                if is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.left + 8, me.rect.centery))
                    bullets[bullet2_index + 1].reset((me.rect.right - 8, me.rect.centery))
                    bullet2_index = (bullet2_index +2) % BULLET2_NUM
                else:
                    bullets = bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index +1) % BULLET1_NUM

                    

            #检测子弹是否击中敌机
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in big_enemies:
                                e.energy -= 1
                                e.hit = True
                                if e.energy == 0:
                                    e.active = False
                            else:
                                e.active = False


            #绘制大型敌机
            for each in big_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        #绘制被打到的特效
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)

                    #绘制血槽
                    pygame.draw.line(screen, BLACK, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.right, each.rect.top - 5), \
                                     2)

                    #当生命大于20%显示绿色，否则选择红色
                    enemy_remain = each.energy / enemy.BigEnemy.energy
                    if enemy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.left + each.rect.width * enemy_remain, each.rect.top - 5), \
                                     2)          
                    
                    #即将出现在画面中，播放音效
                    if each.rect.bottom == -50:
                        bigenemy_fly_sound.play(-1)
                else:
                    #毁灭
                    if not (delay % 3):
                        if e3_destroy_index == 0:
                            bigenemy_down_sound.play()
                        screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        #使得索引始终在0到6之间
                        e3_destroy_index  = (e3_destroy_index + 1) % 7
                        if e3_destroy_index == 0:
                            bigenemy_fly_sound.stop()
                            score += 10000
                            each.reset()
                        
            #检测我方飞机是否被撞
            enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
                me.active = False
                for e in enemies_down:
                    e.active = False

            #绘制中型敌机
            for each in mid_enemies:
                if each.active:
                    each.move()

                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image, each.rect)

                    #绘制血槽
                    pygame.draw.line(screen, BLACK, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.right, each.rect.top - 5), \
                                     2)

                    #当生命大于20%显示绿色，否则选择红色
                    enemy_remain = each.energy / enemy.MidEnemy.energy
                    if enemy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.left + each.rect.width * enemy_remain, each.rect.top - 5), \
                                     2)          
                else:
                    #毁灭
                    if not (delay % 3):
                        if e2_destroy_index == 0:
                            midenemy_down_sound.play()
                        screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                        #使得索引始终在0到3之间
                        e2_destroy_index  = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            score += 6000
                            each.reset()
                        

            #绘制小型敌机
            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    #毁灭
                    if not (delay % 3):
                        if e1_destroy_index == 0:
                            smallenemy_down_sound.play()
                        screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                        #使得索引始终在0到2之间
                        e1_destroy_index  = (e1_destroy_index + 1) % 3
                        if e1_destroy_index == 0:
                            score += 1000
                            each.reset()
            
            #绘制我方飞机
            if me.active:
                if switch_image:
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:
                #毁灭
                if not (delay % 3):
                    if me_destroy_index == 0:
                        me_down_sound.play()
                    screen.blit(me.destroy_images[me_destroy_index], each.rect)
                    #使得索引始终在0到3之间
                    me_destroy_index  = (me_destroy_index + 1) % 4
                    if me_destroy_index == 0:
                        life_num -= 1
                        me.reset()
                        pygame.time.set_timer(INVINCIBLE_TIME, 3 * 1000)


        #绘制游戏结束画面
        elif life_num == 0:
            #背景音乐停止
            pygame.mixer.music.stop()

            #停止全部音效
            pygame.mixer.stop()

            #停止发放补给
            pygame.time.set_timer(SUPPLY_TIME, 0)


        #绘制结束界面
        if life_num == 0:
            if not recorded:
                recorded = True
                #读取历史最高分
                with open('record.txt', 'r') as f:
                    record_score = int(f.read())

                #如果玩家得分高于历史最高分，则存档
                if score > record_score:
                    with open('record.txt', 'w') as f:
                        f.write(str(score))

            if times == 0 and button_re:
                button_sound.play()
                times = 1
                button_re = 0

            again_rect.center = width//2, height//2-50
            screen.blit(again_image, again_rect)
            gameover_rect.center = width//2, height//2+50
            screen.blit(gameover_image, gameover_rect)
            best_text = best_font.render('Best : {}'.format(str(record_score)), True, WHITE)
            screen.blit(best_text, (10, 5))
            end_score_text = end_score_font.render('Score : {}'.format(str(score)), True, WHITE)
            end_score_rect = end_score_text.get_rect()
            end_score_rect.center = width//2, height//2 - 150
            screen.blit(end_score_text, end_score_rect)
                    

        if life_num:
            #绘制全屏炸弹数量
            bomb_text = bomb_font.render(' X {}'.format(str(bomb_num)), True, WHITE)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height -10 - bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - text_rect.height))
            
            #绘制分数
            score_text = score_font.render('Score : {}'.format(str(score)), True, WHITE)
            screen.blit(score_text, (10, 5))

            #绘制剩余生命数量
            for i in range(life_num):
                screen.blit(life_image, \
                            (width - 10 - (i +1) * life_rect.width * 1.2, \
                            height - 10 - life_rect.height))


            #绘制暂停按钮
            screen.blit(paused_image, paused_rect)


        #用于切换图片
        if not (delay % 5):
            switch_image = not switch_image

        delay -= 1
        if not delay:
            delay = 100

        pygame.display.flip()
        clock.tick(60)

        if not start:
            break
        if not again.restart:
            pygame.quit()
            sys.exit()


if __name__ == '__main__':
    try:
        while again.restart:
            main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
