import pygame

class DamageNumber(pygame.sprite.Sprite):

    def __init__(self, amount, pos, font=None, color=(255, 0, 0)):

        super().__init__()

        self.font = font or pygame.font.Font(None, 30)
        self.amount = amount

        self.image = self.font.render(str(amount), True, color)
        self.rect = self.image.get_rect(center=pos)
        self.timer = 0.0
        self.lifetime = 0.8
        self.speed_y = -30

        self.isDamageNumber = True

    def update(self, delta_time):

        self.timer += delta_time

        # Upward movement
        self.rect.y += int(self.speed_y * delta_time)

        # Transparency effect
        alpha = max(0, 255 - int((self.timer / self.lifetime) * 255))
        self.image.set_alpha(alpha)

        if self.timer >= self.lifetime:

            self.kill()
