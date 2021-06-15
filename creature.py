import pygame
import math
from pygame import Surface
from movequeue import Queue
import random

BORDER_COLOR = (0, 220, 50, 255)

SCALE_ATTR = (48, 48)


class Creature(pygame.sprite.Sprite):
    def __init__(self, c_id, x, y, r):
        super(Creature, self).__init__()

        self.frames = 0
        self.images = []
        self.images.append(pygame.image.load('art/creature/creature-anim-1.png').convert_alpha())
        self.images.append(pygame.image.load('art/creature/creature-anim-2.png').convert_alpha())
        self.images.append(pygame.image.load('art/creature/creature-anim-3.png').convert_alpha())
        self.images.append(pygame.image.load('art/creature/creature-anim-4.png').convert_alpha())

        for i, img in enumerate(self.images):
            self.images[i] = pygame.transform.scale(img, SCALE_ATTR)

        self.index = 0
        self.image = self.images[self.index]

        self.id = c_id
        self.x = x
        self.y = y
        self.r = r
        self.vel_x = 0
        self.vel_y = 0
        self.img = None
        self.rect = pygame.Rect(self.x, self.y, 50, 50)
        self.center = [self.x, self.y]
        self.color = (0, 100, 255)
        self.arrow_color = (100, 200, 25)

        self.left_key = False
        self.right_key = False
        self.down_key = False
        self.up_key = False

        self.collision = False
        self.speed = 0.5

        self.alive = True

        self.radars = []

        self.start_x = self.x
        self.start_y = self.y
        self.moves = Queue()
        self.avg_moves = Queue()

        self.dtc = int(r)   # distance to center
        self.collision_pts = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
                              (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]

        self.angle = 0

    def draw_radar(self, screen):
        for radar in self.radars:
            position = radar[0]
            pygame.draw.line(screen, (0, 255, 0), self.center, position, 1)
            pygame.draw.circle(screen, (0, 255, 0), position, 5)

        # for pt in self.collision_pts:
        #    pygame.draw.circle(screen, (255, 255, 0), pt, 5)

    def check_radar_collision(self, screen: Surface, game_map: Surface):

        if not screen.get_height() > self.y > 0:
            return True
        if not screen.get_width() > self.x > 0:
            return True

        for collision_point in self.collision_pts:
            x, y = collision_point
            pt = (int(x), int(y))

            if 0 < pt[0] < screen.get_width() and \
                    0 < pt[1] < screen.get_height() and \
                    game_map.get_at(pt) != BORDER_COLOR:
                return True

        return False

    def check_radar(self, degree, screen, game_map: pygame.Surface):
        length = 0
        x = int(self.center[0] + math.cos(math.radians(360 - degree)) * length)
        y = int(self.center[1] + math.sin(math.radians(360 - degree)) * length)

        # Define a length for the radar
        while 0 < y < screen.get_height() and 0 < x < screen.get_width() \
                and game_map.get_at((x, y)) == BORDER_COLOR \
                and length < 300:
            length = length + 1
            x = int(self.center[0] + math.cos(math.radians(360 - degree)) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - degree)) * length)

        # Calculate Distance To Border And Append To Radars List
        dist = int(math.sqrt(math.pow(x - self.x, 2) + math.pow(y - self.y, 2)))
        self.radars.append([(x, y), dist])

    def update(self, screen, game_map):
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

        # self.x += self.vel_x
        # self.y += self.vel_y

        self.x = self.x + math.cos(math.radians(360 - self.angle)) * self.speed
        self.y = self.y + math.sin(math.radians(360 - self.angle)) * self.speed
        # print(self.angle)
        self.center = [self.x, self.y]

        idx = 0
        for d in range(0, 360, 45):
            x = int(self.center[0] + math.cos(math.radians(360 - d)) * self.dtc)
            y = int(self.center[1] + math.sin(math.radians(360 - d)) * self.dtc)
            self.collision_pts[idx] = (x, y)
            idx += 1

        self.rect = pygame.Rect(int(self.x), int(self.y), 32, 32)
        self.radars.clear()

        for d in range(0, 360, 45):
            self.check_radar(d, screen, game_map)

    def verify_bounds(self, screen_width, screen_height):
        if self.x <= 0 or self.x >= screen_width or self.y <= 0 or self.y >= screen_height:
            return False
        return True

    def draw(self, screen, game_map):
        self.update(screen, game_map)
        if self.alive:
            self.frames += 1

            if self.frames >= 3:
                self.frames = 0
                self.index += 1

                if self.index >= len(self.images):
                    self.index = 0

                self.image = self.images[self.index]
            self.img = self.image
            self.img = pygame.transform.rotate(self.image, self.angle - 90)
            screen.blit(self.img, (self.x, self.y))

    def is_alive(self):
        return self.alive

    def get_data(self):
        radars = self.radars
        return_values = [0, 0, 0, 0, 0, 0, 0, 0]
        for i, radar in enumerate(radars):
            return_values[i] = int(radar[1] / 30)

        return return_values

    def action_on_input(self, choice):
        if choice == 0:
            self.angle += 2
        elif choice == 1:
            self.angle -= 2
        elif choice >= 2:
            speed_choices = [0.6, 0.7, 0.75, 0.8, 0.9, 0.95, 1, 1.05, 1.1, 1.2, 1.5]
            chosen_speed = random.choice(speed_choices)
            self.speed = 2 * chosen_speed

        if self.angle != 0:
            self.angle = self.angle % 360

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
                # print("Creature " + str(self.id) + " died by paralysis!")
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
            self.set_keys(False, True, False, True)
        elif choice == 5:
            self.set_keys(True, False, False, True)

        return True

    def set_keys(self, left, right, up, down):
        self.left_key = left
        self.right_key = right
        self.up_key = up
        self.down_key = down
