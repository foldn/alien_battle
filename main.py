import pygame
import game_functions as gf
from settings import Settings
from ship import Ship
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from invincible_food import Invincibility_Food


def run_game():
    #初始化pygame和mixter，后者用来播放音乐
    pygame.init()
    pygame.mixer.init()

    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("飞机大战")

    # 创建Play按钮
    play_button = Button( screen)

    # 创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)

    # 创建计分牌
    scoreboard = Scoreboard(ai_settings, screen, stats)

    # 创建一艘飞船，子弹编组，外星人编组
    ship = Ship(ai_settings, screen)
    bullets = Group()
    alien_bullets = Group()
    aliens = Group()
    # 创建一个定时器，以达到boss按时发射子弹的效果
    BOSS_FIRE = pygame.USEREVENT
    pygame.time.set_timer(BOSS_FIRE, 300)

    # 创建无敌补给
    invinvible_food = Invincibility_Food(screen, ai_settings)
    #定义无敌补给事件以及对应的定时器
    SUPPLY_TIME = pygame.USEREVENT+1
    pygame.time.set_timer(SUPPLY_TIME, 3 * 1000)
    #定义无敌事件
    INVINCIBLE_TIME = pygame.USEREVENT+2

    # 载入游戏音乐并设置音量
    pygame.mixer.music.load("sound/game_background_music.ogg")
    pygame.mixer.music.set_volume(0.2)

    # 开始游戏主循环
    while True:

        gf.check_events(ai_settings, screen, stats, scoreboard, play_button, ship, aliens,
                        bullets, alien_bullets, BOSS_FIRE, SUPPLY_TIME, invinvible_food, INVINCIBLE_TIME)

        if stats.game_active:

            ship.updata()
            gf.update_bullets(ai_settings, screen, stats, scoreboard, ship, aliens, bullets, alien_bullets)
            gf.update_aliens(ai_settings, stats, scoreboard,screen, ship, aliens, bullets, alien_bullets)
            gf.update_supply(invinvible_food, ship, INVINCIBLE_TIME)
            gf.check_ship_bullets(ai_settings, stats, scoreboard,screen, ship, aliens, bullets, alien_bullets)
            gf.check_alien_alien_collision(ai_settings, screen, stats, scoreboard, ship, aliens, bullets, alien_bullets)

        gf.update_screen(ai_settings, screen, stats, scoreboard, ship,aliens, bullets, play_button, alien_bullets, invinvible_food)


if __name__ == "__main__":
    run_game()
