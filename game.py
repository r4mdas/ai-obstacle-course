import pygame
from creature import Creature
import neat
import os
import sys
import math

WIDTH = 1280
HEIGHT = 720

CAPTION = "AI Obstacle Course"
gen = 0

pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 50)

ALLOWED_OBSTACLES = 20
SECONDS_TO_LIVE = 10000
pre = 0
cur_time = 0


def draw_hud(screen, creatures, elapsed_time):
    # generations
    global STAT_FONT, pre, cur_time
    score_label = STAT_FONT.render("Generations: " + str(gen - 1), 1, (255, 255, 255))
    screen.blit(score_label, (10, 10))

    alive_label = STAT_FONT.render("Alive: " + str(len(creatures)), 1, (255, 255, 255))
    screen.blit(alive_label, (10, 50))

    cur_second = int(elapsed_time / 1000)

    if cur_second is not pre:
        cur_time = cur_second
    pre = cur_second

    time_label = STAT_FONT.render("Elapsed time: " + str(cur_time), False, (255, 255, 255))
    screen.blit(time_label, (10, 90))


def game_start(genomes, config):
    global gen

    elapsed_time = 0
    target_x, target_y = (WIDTH/2, 75)
    gen += 1
    pygame.init()
    pygame.display.set_caption(CAPTION)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    game_map = pygame.image.load('art/Maze.png').convert()

    game_surf = pygame.Surface((WIDTH, HEIGHT))
    game_surf.fill((200, 255, 0))

    nets = []
    creatures = []
    ge = []

    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        # print(genome_id)
        creatures.append(Creature(genome_id, 500, 530, 15))
        ge.append(genome)

    # obs = generate_obstacles()

    # obs.append(Obstacle)
    game_loop = True

    # pre = 0
    while game_loop and len(creatures) > 0:
        # screen.blit(game_surf, (0, 0))
        screen.blit(game_map, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_loop = False
                sys.exit(0)

        for i, c in enumerate(creatures):
            output = nets[i].activate(c.get_data())
            choice = output.index(max(output))
            if not c.set_input_choice(choice):
                print("Popped by paralysis")
                ge[creatures.index(c)].fitness -= 30
                nets.pop(creatures.index(c))
                ge.pop(creatures.index(c))
                creatures.pop(creatures.index(c))

        pygame.draw.circle(screen, (0, 255, 0), (target_x, target_y), 15)

        # for ob in obs:
        #     ob.draw(screen)

        for c in creatures:
            c.draw(screen, game_map)

        for i, c in enumerate(creatures):
            # for ob in obs:
            #     if ob.check_hit([c.x, c.y], c.r):
            #         c.collision = True

            c.collision = c.check_radar_collision(screen, game_map)

            if c.collision:  # or elapsed_time > SECONDS_TO_LIVE:
                print("Popped by bounds collision")
                ge[creatures.index(c)].fitness -= 20
                # if elapsed_time > SECONDS_TO_LIVE:
                #    ge[creatures.index(c)].fitness -= 30
                nets.pop(creatures.index(c))
                ge.pop(creatures.index(c))
                creatures.pop(creatures.index(c))
            else:
                init_distance = int(math.sqrt((float(c.x) - target_x) ** 2 + (c.y - target_y) ** 2))
                cur_distance = int(math.sqrt((float(c.start_x) - target_x) ** 2 + (c.start_y - target_y) ** 2))
                # if cur_distance > init_distance:
                #     genomes[i][1].fitness -= 20
                # else:
                genomes[i][1].fitness = ((init_distance - cur_distance) * 100) / init_distance

        draw_hud(screen, creatures, elapsed_time)
        pygame.display.flip()
        dt = clock.tick(60)
        elapsed_time += dt


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
