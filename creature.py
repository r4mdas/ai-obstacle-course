import pygame


class Creature(pygame.sprite.Sprite):
    def __init__(self, x, y, r):
        super(Creature, self).__init__()

        self.x = x
        self.y = y
        self.r = r
        self.vel_x = 0
        self.vel_y = 0
        self.rect = pygame.Rect(self.x, self.y, 50, 50)
        self.color = (0, 100, 255)

        self.left_key = False
        self.right_key = False
        self.down_key = False
        self.up_key = False

        self.collision = False
        self.speed = 5

        self.alive = True

        self.radars = []

    def update(self):
        self.vel_x = 0
        self.vel_y = 0
        if self.left_key and not self.right_key:
            self.vel_x = -self.speed
        if self.right_key and not self.left_key:
            self.vel_x = self.speed
        if self.up_key and not self.down_key:
            self.vel_y = -self.speed
        if self.down_key and not self.up_key:
            self.vel_y = self.speed

        self.x += self.vel_x
        self.y += self.vel_y

        self.rect = pygame.Rect(int(self.x), int(self.y), 32, 32)

    def verify_bounds(self, screen_width, screen_height):
        if self.x <= 0 or self.x >= screen_width or self.y <= 0 or self.y >= screen_height:
            return False
        return True

    def draw(self, screen):
        self.update()
        if not self.collision:
            pygame.draw.circle(screen, self.color, (self.x, self.y), 15)

    def is_alive(self):
        return self.alive

    def get_data(self):
        pass
