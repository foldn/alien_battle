import pygame
from pygame.sprite import Sprite
from numpy import random
class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self, ai_settings, screen, isBoss = False):
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        #创建一个水平移动速度的影响因子，随机生成
        self.horizontal_speed = random.randint(1,4)
        self.vertical_speed = random.randint(1,3)
        #判断是不是boss
        self.isBoss = isBoss

        #如果是boss则使用boss图片反之，则使用普通图片
        if self.isBoss == False:

            #加载外星人图像，并设置其rect属性
            self.image = pygame.image.load('images/alien_plane.bmp')
            self.rect = self.image.get_rect()

            #设置血量
            self.energy = 1

            #每个外星人最初都是在屏幕左上角附近创建
            self.rect.x = self.rect.width
            self.rect.y = self.rect.height

            #存储外星人的准确位置
            self.position_x = float(self.rect.x)
            self.position_y = float(self.rect.y)
        else:
            # 加载外星人图像，并设置其rect属性
            self.image = pygame.image.load('images/alienBoss.png')
            self.rect = self.image.get_rect()

            # 设置血量
            self.energy = 5

            # 每个外星人最初都是在屏幕左上角附近创建
            self.rect.x = self.rect.width
            self.rect.y = self.rect.height

            # 存储外星人的准确位置
            self.position_x = float(self.rect.x)
            self.position_y = float(self.rect.y)

    def check_edges(self):
        #如果外星人位于屏幕边缘，就返回True
        screen_rect = self.screen.get_rect()
        if self.rect.left <= 0:
            return True
        elif self.rect.right >= screen_rect.right:
            return True

    def update(self):
        """向右或向左移动的外星人"""
        self.position_x += self.horizontal_speed * self.ai_settings.fleet_direction
        self.position_y += self.vertical_speed * self.ai_settings.fleet_drop_speed
        self.rect.x = self.position_x
        self.rect.y = self.position_y

    def change_direction(self):
        #改变方向
        self.ai_settings.fleet_direction *= -1

    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)