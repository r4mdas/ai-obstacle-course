import pygame
import math
from pygame import Surface
import random
from creature_collider import CreatureCollider

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
        # self.images.append(pygame.image.load('art/square.png').convert())

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

        self.left_key = False
        self.right_key = False
        self.down_key = False
        self.up_key = False

        self.collision = False
        self.speed = 0.5

        self.alive = True

        self.radars = []

        self.angle = 0
        self.collision_pts = [(0, 0), (0, 0), (0, 0), (0, 0)
                              , (0, 0), (0, 0), (0, 0), (0, 0)]

    def rotate_center(self, image):
        rectangle = image.get_rect()
        rotated_image = pygame.transform.rotate(image, self.angle - 90)
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rectangle).copy()

        return rotated_image

    def draw_radar(self, screen):
        for radar in self.radars:
            position = radar[0]
            pygame.draw.line(screen, (0, 255, 0), (self.x + (SCALE_ATTR[0]/2), self.y + (SCALE_ATTR[1]/2)), position, 1)
            pygame.draw.circle(screen, (0, 255, 0), position, 5)

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

        center_x, center_y = (self.x + SCALE_ATTR[0]/2, self.y + SCALE_ATTR[1]/2)
        x = int(center_x + math.cos(math.radians(360 - degree)) * length)
        y = int(center_y + math.sin(math.radians(360 - degree)) * length)

        # Define a length for the radar
        while 0 < y < screen.get_height() and 0 < x < screen.get_width() \
                and game_map.get_at((x, y)) == BORDER_COLOR \
                and length < 300:
            length = length + 1
            x = int(center_x + math.cos(math.radians(360 - degree)) * length)
            y = int(center_y + math.sin(math.radians(360 - degree)) * length)

        # Calculate Distance To Border And Append To Radars List
        dist = int(math.sqrt(math.pow(x - self.x, 2) + math.pow(y - self.y, 2)))
        self.radars.append([(x, y), dist])

    def update(self, screen, game_map):

        self.x += math.cos(math.radians(360 - self.angle)) * self.speed
        self.y += math.sin(math.radians(360 - self.angle)) * self.speed

        self.center = [self.x, self.y]

        idx = 0
        dtc = (SCALE_ATTR[0] / 2)
        for d in range(0, 360, 45):
            x = int(self.center[0] + math.cos(math.radians(360 - d))
                    * dtc)
            y = int(self.center[1] + math.sin(math.radians(360 - d))
                    * dtc)
            scale_x, scale_y = SCALE_ATTR

            x = int(x + math.cos(math.radians(360 - d)))
            y = int(y + math.sin(math.radians(360 - self.angle)))
            self.collision_pts[idx] = (x + int(scale_x/2), y + int(scale_y/2))

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
            # self.img = pygame.transform.rotate(self.image, self.angle - 90)
            self.img = self.rotate_center(self.img)
            screen.blit(self.img, (self.x, self.y))

            self.draw_radar(screen)
            # for pt in self.collision_pts:
            #     pygame.draw.circle(screen, (255, 255, 0), pt, 5)

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
