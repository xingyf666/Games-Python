import pygame
from pygame.locals import *
import sys
import rect
import check_def
import traceback

pygame.init()
pygame.mixer.init()

clear_sound = pygame.mixer.Sound('music\\clear.wav')
clear_sound.set_volume(0.2)
level_up_sound = pygame.mixer.Sound('music\\level.wav')
level_up_sound.set_volume(0.2)


def main():
    bg_size = width, height = 960, 720
    running = True
    GREEN = 0, 255, 0
    
    pygame.mixer.music.load('music\\不动要塞.mp3')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    screen = pygame.display.set_mode(bg_size)
    background = pygame.image.load('images\\background.png').convert_alpha()
    pygame.display.set_caption('俄罗斯方块')

    #指定重复事件的延迟
    delay = 100
    interval = 200
    pygame.key.set_repeat(delay, interval)

    #定义检测线对象，加入物块组
    check_line = check_def.Check(bg_size, 'images\\check_line.png')
    rect_group = [check_line]

    #定义第一个物块
    next_rect = rect.Rect(bg_size)

    #创建清理函数对象(一个方块(~_~))
    check_clear = check_def.Check(bg_size, 'images\\方块.png')

    clock = pygame.time.Clock()

    #计时器，每800毫秒触发一次
    MOVING = USEREVENT
    sep = 800
    pygame.time.set_timer(MOVING, sep)

    #计算得分及等级
    score = 0
    level = 1
    score_font = pygame.font.Font('font\\font.ttf', 30)
    level_font = pygame.font.Font('font\\font.ttf', 30)

    #判定是否产生下一个物块
    check = True
    
    while running:
        if check:
            #将下一个物块加入物块组
            rect_group.append(next_rect)
            #定义组中最后一个对象为可移动对象
            move_rect = rect_group[-1]
            #创建下一个物块
            next_rect = rect.Rect(bg_size)
            #定义碰撞检测对象
            check_collide = check_def.Collide(move_rect, rect_group)
            #创建物块后禁止创建
            check = False

        #进行判定之前的可移动物块的位置
        check_pos = move_rect.rect.center    
            
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_a:
                    move_rect.moveleft()

                if event.key == K_d:
                    move_rect.moveright()

                if event.key == K_w:
                    move_rect.rect_change()

                if event.key == K_s:
                    #定义碰撞前的物块位置
                    check_collide.rect = move_rect.rect.bottom
                    move_rect.movedown()
                    #定义碰撞后的物块位置
                    check_collide.bottom = move_rect.rect.bottom
                    #进行碰撞检测
                    check_collide.check_collide()

                if event.key == K_SPACE:
                    #定义碰撞前的物块位置
                    check_collide.rect = move_rect.rect.bottom
                    move_rect.to_bottom()
                    #定义碰撞后的物块位置
                    check_collide.bottom = move_rect.rect.bottom
                    #进行碰撞检测
                    check_collide.check_collide()

            #当计时器发动时会触发这一事件
            elif event.type == MOVING:
                move_rect.move()
                

        screen.blit(background, (0, 0))

        #碰撞检测前移除自身
        rect_group.remove(move_rect)

        #定义清除检测对象
        clear = check_def.Clear(check_clear, rect_group)
        #清除检测函数
        clear.clear()
        #重新定义清除后的物块组
        rect_group = clear.rect_group

        #当发生清理时，在清理位置以上的所有物块调用to_bottom函数移至最底端
        if clear.check:
            clear_sound.play()
            praise = 1
            for i in range(clear.count):
                score += praise * 200
                praise += 1

            #先把move_rect加回去
            rect_group.append(move_rect)
            
            for each in rect_group:
                while each.rect.bottom < clear.clear_bottom:
                    #定义检测对象check_collide_rect
                    check_collide_rect = check_def.Collide(each, rect_group)
                    #定义碰撞前的物块位置
                    check_collide_rect.rect = each.rect.bottom
                    each.to_bottom()
                    #定义碰撞后的物块位置
                    check_collide_rect.bottom = each.rect.bottom
                    #进行碰撞检测
                    check_collide_rect.check_collide()

            rect_group.remove(move_rect)

        #检测是否碰撞底板check_line
        rect_collide = pygame.sprite.spritecollide(move_rect, rect_group, False, pygame.sprite.collide_mask)
        if rect_collide:
            #当碰撞底板时返回到移动前的位置
            move_rect.rect.center = check_pos
            #调用一下移动函数
            move_rect.move()
            #再检测一次碰撞
            rect_collide = pygame.sprite.spritecollide(move_rect, rect_group, False, pygame.sprite.collide_mask)
            if rect_collide:
                score += 50
                #当碰撞时允许生成下一个物块
                check = True
            #当物块移回move之前的位置
            move_rect.rect.center = check_pos

        #全检测完就把自己加回去    
        rect_group.append(move_rect)

        #显示下一个物块
        screen.blit(next_rect.tip, next_rect.tip_rect)

        #打印组中的物块，打印前把check_line移除(因为没有add_rect参数)
        rect_group.remove(check_line)
        for each in rect_group:
            screen.blit(each.add_rect, each.rect)
        rect_group.insert(0, check_line)

        #绘制得分及等级
        score_text = score_font.render('Score : {}'.format(str(score)), True, GREEN)
        level_text = score_font.render('Level : {}'.format(str(level)), True, GREEN)
        screen.blit(score_text, (700, 600))
        screen.blit(level_text, (705, 660))
        
        #得分与等级
        if score >= 1000 and level == 1:
            level_up_sound.play()
            level = 2
            sep = 600
        elif score >= 2000 and level == 2:
            level_up_sound.play()
            level = 3
            sep = 450
        elif score >= 5000 and level == 3:
            level_up_sound.play()
            level = 4
            sep = 300
        elif score >= 10000 and level == 4:
            level_up_sound.play()
            level = 5
            sep = 200
        elif score >= 16000 and level == 5:
            level_up_sound.play()
            level = 6
            sep = 100
        
        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
