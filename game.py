import pygame
from creature import Creature
from obstacle import Obstacle

import sys

WIDTH = 1280
HEIGHT = 720

CAPTION = "AI Obstacle Course"


def game_start():
    pygame.init()
    pygame.display.set_caption(CAPTION)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    game_surf = pygame.Surface((WIDTH, HEIGHT))
    game_surf.fill((200, 255, 0))

    c1 = Creature(WIDTH/2, 600, 15)

    obs = []
    obstacle_1 = Obstacle(0, 200, WIDTH-400, 15)
    obs.append(obstacle_1)
    obstacle_2 = Obstacle(WIDTH-600, 300, 600, 15)
    obs.append(obstacle_2)

    while True:
        screen.blit(game_surf, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    c1.left_key = True
                if event.key == pygame.K_RIGHT:
                    c1.right_key = True
                if event.key == pygame.K_UP:
                    c1.up_key = True
                if event.key == pygame.K_DOWN:
                    c1.down_key = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    c1.left_key = False
                if event.key == pygame.K_RIGHT:
                    c1.right_key = False
                if event.key == pygame.K_UP:
                    c1.up_key = False
                if event.key == pygame.K_DOWN:
                    c1.down_key = False

        c1.draw(screen)
        obstacle_1.draw(screen)
        obstacle_2.draw(screen)

        for ob in obs:
            if ob.check_hit([c1.x, c1.y], c1.r):
                c1.collision = True

        if not c1.verify_bounds(WIDTH, HEIGHT):
            c1.collision = True

        if c1.collision:
            c1 = Creature(WIDTH / 2, 600, 15)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    game_start()
