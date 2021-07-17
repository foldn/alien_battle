import pygame
from pygame.sprite import Sprite
from random import *


class Invincibility_Food(Sprite):
    def __init__(self, screen, ai_settings):
        super().__init__()

        self.screen = screen

        #获得无敌补给的图片以及rect
        self.image = pygame.image.load("images/invincible_food.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.start_width, self.start_height = ai_settings.screen_width, ai_settings.screen_height
        self.rect.left, self.rect.bottom = randint(0, self.start_width - self.rect.width), -100
        self.drop_speed = 3
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def drop(self):
        #无敌果实移动方法
        if self.rect.top < self.start_height:
            self.rect.top += self.drop_speed
        else:
            self.active = False

    def food_init(self):
        #移动果实初始化
        self.active = True
        self.rect.left, self.rect.bottom = randint(0, self.start_width - self.rect.width), -100


    def blitme(self):
        # 绘制无敌补给并检测是否获得
        if self.active:
            self.drop()
            self.screen.blit(self.image, self.rect)
