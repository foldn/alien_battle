import pygame.font

class Button():

    def __init__(self, screen):
        """初始化按钮属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        #加载图片
        self.button_image = pygame.image.load('images/start_button.png')
        #设置按钮的尺寸和其他属性
        self.button_width = 200
        self.button_height = 50

        #创建按钮的rect对象，并使其居中
        self.rect = self.button_image.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery+200

    def draw_button(self):
        #使用指定图片绘制按钮
        self.screen.blit(self.button_image, self.rect)
