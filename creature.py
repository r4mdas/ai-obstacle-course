import pygame
import math
from obstacle import Obstacle
from pygame import Surface


class Creature(pygame.sprite.Sprite):
    def __init__(self, x, y, r):
        super(Creature, self).__init__()

        self.x = x
        self.y = y
        self.r = r
        self.vel_x = 0
        self.vel_y = 0
        self.rect = pygame.Rect(self.x, self.y, 50, 50)
        self.center = [self.x, self.y]
        self.color = (0, 100, 255)

        self.left_key = False
        self.right_key = False
        self.down_key = False
        self.up_key = False

        self.collision = False
        self.speed = 3

        self.alive = True

        self.radars = []

    def draw_radar(self, screen):
        # print(self.radars)
        for radar in self.radars:
            position = radar[0]
            pygame.draw.line(screen, (0, 255, 0), self.center, position, 3)
            pygame.draw.circle(screen, (0, 255, 0), position, 5)

    def check_radar_collision(self, screen: Surface, obs, x, y):
        # print(self.center)
        if not screen.get_height() > y > 0:
            return True
        if not screen.get_width() > x > 0:
            return True

        ob: Obstacle

        for ob in obs:
            if ob.collide_line(x, y):
                return True

        return False

    def check_radar(self, degree, screen, obs):
        length = 0
        # print(screen)
        x = int(self.center[0] + math.cos(math.radians(360 - degree)) * length)
        y = int(self.center[1] + math.sin(math.radians(360 - degree)) * length)

        # Define a length for the radar
        while not self.check_radar_collision(screen, obs, x, y) and length < screen.get_width():
            length = length + 1
            x = int(self.center[0] + math.cos(math.radians(360 - degree)) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - degree)) * length)
        # Calculate Distance To Border And Append To Radars List
        dist = int(math.sqrt(math.pow(x - self.x, 2) + math.pow(y - self.y, 2)))
        self.radars.append([(x, y), dist])

    def update(self, screen, obs):
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
        self.radars.clear()
        for d in range(0, 360, 90):
            self.check_radar(d, screen, obs)

    def verify_bounds(self, screen_width, screen_height):
        if self.x <= 0 or self.x >= screen_width or self.y <= 0 or self.y >= screen_height:
            return False
        return True

    def draw(self, screen, obs):
        self.update(screen, obs)
        if self.alive:
            pygame.draw.circle(screen, self.color, (self.x, self.y), 15)
            self.draw_radar(screen)

    def is_alive(self):
        return self.alive

    def get_data(self):
        radars = self.radars
        return_values = [0, 0, 0, 0]
        for i, radar in enumerate(radars):
            return_values[i] = int(radar[1] / 30)

        return return_values

    def set_keys(self, left, right, up, down):
        self.left_key = left
        self.right_key = right
        self.up_key = up
        self.down_key = down
