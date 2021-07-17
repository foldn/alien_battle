import sys
import pygame
import numpy
from bullet import Bullet
from bullet import Alien_Bullet
from alien_plane import Alien
from time import sleep


def fire_bullet(ai_settings, screen, ship, bullets):
    # 如果还没有到达限制，就发射一颗子弹
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def fire_alien_bullet(ai_settings, screen, aliens, alien_bullets):
    # 为外星人boss发射子弹
    for alien in aliens:
        if alien.isBoss:
            new_bullet = Alien_Bullet(ai_settings, screen, alien)
            alien_bullets.add(new_bullet)


def check_keydown_events(event, ai_settings, screen, stats, ship, bullets, SUPPLY_TIME, INVINCIBLE_TIME):
    # 按下对应键的事件判断
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    # 空格键发射子弹、ESC退出的判断
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()
    #P键暂停事件判断，再按一次恢复游戏
    elif event.key == pygame.K_p:
        if stats.game_active:
            stats.game_active = False
            stats.isPause = True
            pygame.time.set_timer(SUPPLY_TIME, 0)
            pygame.time.set_timer(INVINCIBLE_TIME, 0)
        elif not stats.game_active:
            stats.game_active = True
            stats.isPause = False
            pygame.time.set_timer(SUPPLY_TIME, 3 * 1000)
            pygame.time.set_timer(INVINCIBLE_TIME, 5 * 1000)



def check_keyup_events(event, ship):
    #松开按键的事件
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False
    


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """在玩家单击Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏统计信息
        stats.game_active = True
        stats.reset_stats()

        # 重置计分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_round()
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #创建新的外星人舰队，设定玩家飞船的初始位置
        create_fleet(ai_settings, screen, ship, aliens, stats)
        ship.center_ship()

        #设置初始设定，播放背景音乐
        ai_settings.initialize_dynamic_settings()
        pygame.mixer.music.play(-1)

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, alien_bullets, FIRE, SUPPLY_TIME, i_supply, INVINCIBLE_TIME):
    # 响应按键和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, ship, bullets, SUPPLY_TIME, INVINCIBLE_TIME)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        #当事件为FIRE时，启动事件对应的定时器，到达时间后调用方法
        elif event.type == FIRE:
            fire_alien_bullet(ai_settings, screen, aliens, alien_bullets)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb,
                              play_button, ship, aliens, bullets, mouse_x, mouse_y)
        #当事件为无敌果实补给时，启动定时器，时间到达，掉落无敌果实
        elif event.type == SUPPLY_TIME:
            i_supply.food_init()
        #开启无敌时间，事件结束后，飞机恢复原装
        elif event.type == INVINCIBLE_TIME:
            ship.invincible = False
            ship.image = pygame.image.load("./images/ship.bmp")
        



def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, alien_bullets, i_supply):
    # 如果处于游戏状态使用游戏背景，反之使用开始页面
    # 每次循环时都重绘屏幕
    if stats.isPause:
        return

    if stats.game_active == False and stats.isPause == False:
        screen.blit(ai_settings.start_image, (0, 0))
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
        screen.blit(ai_settings.bg_image, (0, 0))
        # 在飞船和外星人后面重绘所有子弹
        for bullet in bullets.sprites():
            bullet.draw_ship_bullet()
        for bullet in alien_bullets.sprites():
            bullet.draw_alien_bullet()
        # 绘制飞船和外星人
        ship.blitme()
        aliens.draw(screen)
        #无敌果实绘制
        i_supply.blitme()
        # 显示得分
        sb.show_score()
    # 如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets):
    # 更新子弹的位置，并删除已经消失的子弹
    bullets.update()
    alien_bullets.update()
    # 删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # 删除已经消失的敌方子弹
    for bullet in alien_bullets.copy():
        if bullet.rect.top >= ai_settings.screen_height:
            alien_bullets.remove(bullet)
    check_bullet_alien_collision(
        ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # 检查是否有子弹击中外星人
    # 如果有元素碰撞发生，就删除相应的子弹和外星人

    collisions = pygame.sprite.groupcollide(bullets, aliens, True, False)
    if collisions:
        for aliens_value in collisions.values():
            aliens_value[0].energy -= 1
            if aliens_value[0].energy == 0:
                if aliens_value[0].isBoss:
                    stats.score += ai_settings.alien_points*stats.level
                else:
                    stats.score += ai_settings.alien_points
                aliens_value[0].kill()
                sb.prep_score()
            check_high_score(stats, sb)
    # 检测外星人是否消灭完
    if len(aliens) == 0:

        bullets.empty()
        ai_settings.increase_speed()

        # 提高等级
        stats.level += 1
        sb.prep_round()

        create_fleet(ai_settings, screen, ship, aliens, stats)

def check_alien_alien_collision(ai_settings,screen,stats,sb,ship,aliens,bullets,alien_bullets):
    '''判断外星人飞船之间是否碰撞'''
    for alien in aliens:
        new_aliens = aliens.copy()
        new_aliens.remove(alien)
        collision = pygame.sprite.spritecollide(alien,new_aliens,False)
        if collision:
            #如果碰撞，更改外星人方向
            alien.change_direction()
            update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets,alien_bullets)

def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可以容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height -
                         ship_height - (3 * alien_height))
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可以容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.position_x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.position_x
    alien.rect.y = alien.rect.height
    aliens.add(alien)


def create_alienBoss(ai_settings, screen, aliens, alien_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings, screen, True)
    alien_width = alien.rect.width
    alien.position_x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.position_x
    alien.rect.y = alien.rect.height
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens, stats):
    """创建外星人群"""
    # 创建一个外星人，并计算一行可以容纳多少个外星人
    alien = Alien(ai_settings, screen)
    number_alien_x = get_number_aliens_x(ai_settings, alien.rect.width)


    state = stats
    if state.level % 3 != 0:

        # 创建外星人群:
        lis = set(numpy.random.randint(1, number_alien_x, 10))
        for alien_number in lis:
            create_alien(ai_settings, screen, aliens, alien_number)
    else:
        #创建外形BOSS群
        lis = set(numpy.random.randint(1, number_alien_x-5, state.level//3))
        for alien_number in lis:
            create_alienBoss(ai_settings, screen, aliens, alien_number)


def change_fleet_direction(ai_settings, aliens):
    """有外星人到达边缘时更改外星人方向"""
    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets, alien_bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:

        # 将ships_left减1
        stats.ships_left -= 1
        # 更新计分牌
        sb.prep_ships()
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        alien_bullets.empty()
        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens, stats)
        ship.center_ship()
        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats,screen, ship, aliens):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.top >= screen_rect.bottom:
            aliens.empty()
            create_fleet(ai_settings,screen,ship,aliens,stats)
            break



def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets,alien_bullets):
    """更新外星人中所有外星人的位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # 检测外星人和飞船的碰撞

    if (not ship.invincible) and pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets,alien_bullets)
    # 检查是否有外星人到达屏幕底端
    if not ship.invincible:
        check_aliens_bottom(ai_settings, stats,
                            screen, ship, aliens)




def check_high_score(stats, sb):
    """检查是否诞生了新的最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_supply(i_supply, ship, INVINCIBLE_TIME):
    if pygame.sprite.collide_mask(ship, i_supply):
        #设置飞船的无敌状态，更改飞船的样式，设置定时器
        ship.invincible = True
        ship.image = pygame.image.load("./images/ship_invincible.png")
        pygame.time.set_timer(INVINCIBLE_TIME, 5 * 1000)
        i_supply.active = False


def check_ship_bullets(ai_settings, stats, sb, screen, ship, aliens, bullets, alien_bullets):
    if (not ship.invincible) and pygame.sprite.spritecollideany(ship, alien_bullets):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets,alien_bullets)

