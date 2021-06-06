import pygame
import math
from obstacle import Obstacle
from pygame import Surface
from movequeue import Queue


class Creature(pygame.sprite.Sprite):
    def __init__(self, c_id, x, y, r):
        super(Creature, self).__init__()

        self.id = c_id
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
        self.speed = 1.8

        self.alive = True

        self.radars = []

        self.start_x = self.x
        self.start_y = self.y
        self.moves = Queue()
        self.avg_moves = Queue()

    def draw_radar(self, screen):
        # print(self.radars)
        for radar in self.radars:
            position = radar[0]
            pygame.draw.line(screen, (0, 255, 0), self.center, position, 1)
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
        while not self.check_radar_collision(screen, obs, x, y) and length < 300:
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

        self.center = [self.x, self.y]
        self.rect = pygame.Rect(int(self.x), int(self.y), 32, 32)
        self.radars.clear()

        # self.check_paralysis()
        for d in range(0, 360, 45):
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
        return_values = [0, 0, 0, 0, 0, 0, 0, 0]
        for i, radar in enumerate(radars):
            return_values[i] = int(radar[1] / 30)

        return return_values

    def set_input_choice(self, choice):
        self.moves.add((int(self.x), int(self.y)))
        if self.moves.len == 8:
            q_list = self.moves.get_as_list()
            sum_x = 0
            sum_y = 0

            for x, y in q_list:
                sum_x += x
                sum_y += y

            avg_x = sum_x / 8
            avg_y = sum_y / 8
            self.avg_moves.add((int(avg_x), int(avg_y)))
            self.moves.poll()
            # self.moves.print()

        if self.avg_moves.len >= 10:
            avg_list = self.avg_moves.get_as_list()

            max_diff_x = 0
            max_diff_y = 0

            for x, y in avg_list:
                for a, b in avg_list:
                    diff_x = abs(x - a)
                    diff_y = abs(y - b)
                    if diff_x > max_diff_x:
                        max_diff_x = diff_x
                    if diff_y > max_diff_y:
                        max_diff_y = diff_y
            # print((max_diff_x, max_diff_y))
            if max_diff_x <= 3 and max_diff_y <= 3:
                print("Creature " + str(self.id) + " killed by paralysis!")
                return False

            self.avg_moves.poll()

        if choice == 0:
            self.set_keys(True, False, True, False)
        elif choice == 1:
            self.set_keys(False, True, True, False)
        elif choice == 2:
            self.set_keys(False, False, True, False)
        elif choice == 3:
            self.set_keys(False, False, False, True)
        elif choice == 4:
            self.set_keys(False, True, True, False)
        elif choice == 5:
            self.set_keys(False, True, False, True)
        elif choice == 6:
            self.set_keys(True, False, True, False)
        elif choice == 7:
            self.set_keys(True, False, False, True)

        return True

    def set_keys(self, left, right, up, down):
        self.left_key = left
        self.right_key = right
        self.up_key = up
        self.down_key = down
