import pygame
import math


class CreatureCollider(pygame.Surface):
    def __init__(self, x, y, w, h):
        super(self).__init__()

        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.center = (self.x, self.y)

    # def update(self):
    #     idx = 0
    #     # for d in range(0, 360, 45):
    #     #     x = int(self.center[0] + math.cos(math.radians(360 - d))
    #     #             * self.dtc)
    #     #     y = int(self.center[1] + math.sin(math.radians(360 - d))
    #     #             * self.dtc)
    #     # scale_x, scale_y = SCALE_ATTR
    #
    #     # x = int(x + math.cos(math.radians(360 - d)))
    #     # y = int(y + math.sin(math.radians(360 - self.angle)))
    #     # self.collision_pts[idx] = (x + int(scale_x / 2), y + int(scale_y / 2))
    #
    #     idx += 1

    def drawCollider(self, screen, x, y):
        # self.update()
        self.center = (x + int(self.w/2), y + int(self.h/2))
        pygame.draw.circle(screen, (255, 255, 0), self.center, 5)

