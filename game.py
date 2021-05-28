import pygame
from creature import Creature
from obstacle import Obstacle
import neat

import os
import sys

WIDTH = 1280
HEIGHT = 720

CAPTION = "AI Obstacle Course"
gen = 0

pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 50)


def draw_hud(screen):
    # generations
    global STAT_FONT
    score_label = STAT_FONT.render("Generations: " + str(gen - 1), 1, (255, 255, 255))
    screen.blit(score_label, (10, 10))


def game_start(genomes, config):

    global gen

    gen += 1
    pygame.init()
    pygame.display.set_caption(CAPTION)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    game_surf = pygame.Surface((WIDTH, HEIGHT))
    game_surf.fill((200, 255, 0))

    nets = []
    creatures = []
    ge = []

    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        creatures.append(Creature(WIDTH / 2, 600, 15))
        ge.append(genome)

    # c1 = Creature(WIDTH / 2, 600, 15)

    obs = []
    obstacle_1 = Obstacle(0, 200, WIDTH - 400, 15)
    obs.append(obstacle_1)
    obstacle_2 = Obstacle(WIDTH - 600, 300, 600, 15)
    obs.append(obstacle_2)

    while True:
        screen.blit(game_surf, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_LEFT:
            #         creatures[0].left_key = True
            #     if event.key == pygame.K_RIGHT:
            #         creatures[0].right_key = True
            #     if event.key == pygame.K_UP:
            #         creatures[0].up_key = True
            #     if event.key == pygame.K_DOWN:
            #         creatures[0].down_key = True
            # if event.type == pygame.KEYUP:
            #     if event.key == pygame.K_LEFT:
            #         creatures[0].left_key = False
            #     if event.key == pygame.K_RIGHT:
            #         creatures[0].right_key = False
            #     if event.key == pygame.K_UP:
            #         creatures[0].up_key = False
            #     if event.key == pygame.K_DOWN:
            #         creatures[0].down_key = False

        for ob in obs:
            ob.draw(screen)

        for c in creatures:
            c.draw(screen, obs)

        for c in creatures:
            for ob in obs:
                if ob.check_hit([c.x, c.y], c.r):
                    c.collision = True

            if not c.verify_bounds(WIDTH, HEIGHT):
                c.collision = True

            if c.collision:
                ge[creatures.index(c)].fitness -= 1
                nets.pop(creatures.index(c))
                ge.pop(creatures.index(c))
                creatures.pop(creatures.index(c))

        draw_hud(screen)
        pygame.display.flip()
        clock.tick(60)


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for up to 50 generations.
    winner = p.run(game_start, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat-config.txt')
    run(config_path)
