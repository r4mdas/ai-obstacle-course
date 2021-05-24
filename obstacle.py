import pygame


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super(Obstacle, self).__init__()

        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.vel_x = 0
        self.vel_y = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = (255, 100, 0)

        self.left_key = False
        self.right_key = False
        self.down_key = False
        self.up_key = False

        self.speed = 5

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def check_hit(self, center, radius):
        return self.collide(center, radius) if self.rect else False

    def collide(self, center, r):
        rect = self.rect
        circle_distance_x = abs(center[0] - rect.centerx)
        circle_distance_y = abs(center[1] - rect.centery)
        if circle_distance_x > rect.w / 2.0 + r or circle_distance_y > rect.h / 2.0 + r:
            return False
        if circle_distance_x <= rect.w / 2.0 or circle_distance_y <= rect.h / 2.0:
            return True
        corner_x = circle_distance_x - rect.w / 2.0
        corner_y = circle_distance_y - rect.h / 2.0
        corner_distance_sq = corner_x ** 2.0 + corner_y ** 2.0
        return corner_distance_sq <= r ** 2.0
