import pygame
from creature import Creature
from obstacle import Obstacle
import neat
import random
import os
import sys

WIDTH = 1280
HEIGHT = 720

CAPTION = "AI Obstacle Course"
gen = 0

pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 50)

ALLOWED_OBSTACLES = 20


def draw_hud(screen):
    # generations
    global STAT_FONT
    score_label = STAT_FONT.render("Generations: " + str(gen - 1), 1, (255, 255, 255))
    screen.blit(score_label, (10, 10))


def generate_obstacles():
    start_x = 250
    end_x = 800

    left_wall = Obstacle(start_x, 0, 50, HEIGHT)
    right_wall = Obstacle(end_x, 0, 50, HEIGHT)
    obs = [left_wall, right_wall,
           Obstacle(start_x + 200, 400, 150, 25),
           Obstacle(start_x + 200, 400, 25, 150),
           Obstacle(start_x + 200, 550, 150, 25),
           Obstacle(start_x + 350, 400, 25, 50),
           Obstacle(start_x + 350, 500, 25, 75)]

    #     width = random.randint(15, 25)
    #     height = 15
    # for i in range(40):
    #     ob = Obstacle(start_x + i*60, 400, 15, 25)
    #     obs.append(ob)
    # for i in range(ALLOWED_OBSTACLES):
    #     width = random.randint(15, 25)
    #     height = 15
    #     x = random.randint(start_x, end_x - 30)
    #     y = random.randint(0, HEIGHT - 300)
    #     ob = Obstacle(x, y, width, height)
    #     obs.append(ob)
    return obs


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
        creatures.append(Creature(genome_id, 500, 530, 15))
        ge.append(genome)

    obs = generate_obstacles()

    # obs.append(Obstacle)
    game_loop = True
    while game_loop and len(creatures) > 0:
        screen.blit(game_surf, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_loop = False
                sys.exit(0)

        for i, c in enumerate(creatures):
            output = nets[i].activate(c.get_data())
            choice = output.index(max(output))
            c.set_input_choice(choice)
            # print(output)
            # print(str(i) + ":" + str(choice))

        for ob in obs:
            ob.draw(screen)

        for c in creatures:
            c.draw(screen, obs)

        for i, c in enumerate(creatures):
            for ob in obs:
                if ob.check_hit([c.x, c.y], c.r):
                    c.collision = True

            if not c.verify_bounds(WIDTH, HEIGHT):
                c.collision = True

            if c.collision:
                ge[creatures.index(c)].fitness -= 20
                nets.pop(creatures.index(c))
                ge.pop(creatures.index(c))
                creatures.pop(creatures.index(c))
            else:
                genomes[i][1].fitness = max(0, ((c.start_y - c.y) / 10) * 2)

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
