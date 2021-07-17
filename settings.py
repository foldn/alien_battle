import pygame
class Settings():
    """存储该游戏的所有设置的类"""
    def __init__(self):
        #初始化游戏的设置
        #屏幕设置

        self.bg_image = pygame.image.load('images/bg_image.png')
        self.start_image = pygame.image.load('images/start_image.png')
        self.screen_width = 1000
        self.screen_height = 600
        #飞船设置
        self.ship_limit = 3
        #子弹设置
        self.bullet_width = 3
        self.bullet_height = 20
        self.ship_bullet_color = 255, 255, 255
        self.alien_bullet_color = 255, 255, 255
        self.bullets_allowed = 30
        #外星人设置
        self.fleet_drop_speed = 0.1


        #以什么样的速度加快游戏节奏
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 6
        self.bullet_speed_factor = 12
        self.alien_bullet_speed_factor = 6
        self.alien_speed_factor = 10

        #fleet_direction 为1表示向右
        self.fleet_direction = 1

        #计分
        self.alien_points = 50

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

