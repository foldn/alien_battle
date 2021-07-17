import pygame
from pygame.sprite import Sprite

class Bullet (Sprite):
    #一个对飞船发射的子弹进行管理的类
    def __init__(self, ai_settings, screen, ship):
        #在飞船的位置创建一个子弹对象
        super(Bullet, self).__init__()
        self.screen = screen

        #在(0,0)处创建一个表示子弹的矩形，在设置正确的位置
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        #存储用小数表示的子弹位置
        self.y = float(self.rect.y)

        #定义子弹颜色和速度
        self.bullet_color = ai_settings.ship_bullet_color
        self.bullet_speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        #向上移动子弹
        #更新表示自动那位置的小数值
        self.y -= self.bullet_speed_factor
        #更新表示子弹的rect的位置
        self.rect.y = self.y

    def draw_ship_bullet(self):
        #在屏幕上绘制子弹
        pygame.draw.rect(self.screen, self.bullet_color, self.rect)

class Alien_Bullet(Sprite):
    def __init__(self, ai_settings, screen, alien):
        # 在飞船的位置创建一个子弹对象
        super(Alien_Bullet , self).__init__()
        self.screen = screen

        # 在(0,0)处创建一个表示子弹的矩形，在设置正确的位置
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = alien.rect.centerx
        self.rect.bottom = alien.rect.bottom

        # 存储用小数表示的子弹位置
        self.y = float(self.rect.y)

        #定义子弹颜色和速度
        self.bullet_color = ai_settings.alien_bullet_color
        self.bullet_speed_factor = ai_settings.alien_bullet_speed_factor

    def update(self):
        # 向下移动子弹
        # 更新表示自动那位置的小数值
        self.y += self.bullet_speed_factor
        # 更新表示子弹的rect的位置
        self.rect.y = self.y

    def draw_alien_bullet(self):
        # 在屏幕上绘制子弹
        pygame.draw.rect(self.screen, self.bullet_color, self.rect)
