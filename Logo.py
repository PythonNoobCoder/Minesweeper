import pygame


class LogoSprite:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y

    def draw(self, surface, count):
        if count % 2 != 0:
            self.y += 0.5
            self.x += 0.5
        else:
            self.y -= 0.5
            self.x -= 0.5
        surface.blit(self.image, [self.x, self.y])
