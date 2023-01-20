import pygame


clock = pygame.time.Clock()


class Button:
    def __init__(self, x, y, image, pressed_image, scale=1):
        self.pressed = pressed_image
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            self.changeColor(surface)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

    def changeColor(self, surface):
        pos = pygame.mouse.get_pos()
        if pos[0] in range(self.rect.left + 5, self.rect.right + 5) and pos[1] in range(
                self.rect.top + 5,
                self.rect.bottom + 5):
            surface.blit(self.pressed, (self.rect.x, self.rect.y))
