import pygame
import sys
import random
from pygame.math import Vector2

pygame.init()

# colors
BLACK = (30, 30, 30)
WHITE = (255, 255, 255)
PURPLE = (102, 0, 204)
RED = (255, 0, 0)

# size
cell_size = 40
cell_number = 20

Widht = cell_size * cell_number
Height = cell_size * cell_number

# screen
screen = pygame.display.set_mode((Widht, Height))
icon = pygame.image.load('snake/snake.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('snake')

# create the snake
head = Vector2(5, 10)
body = [Vector2(5, 10), Vector2(6, 10)]
direction = Vector2(0, 0)


status = 'no'
dead = False  # status = make the snake bigger
run = True


def draw_snake():
    global head

    for block in body:
        x_pos = int(block.x) * cell_size
        y_pos = int(block.y) * cell_size
        head = Vector2(body[0] * 40, body[1] * 40)
        pygame.draw.rect(screen, WHITE, pygame.Rect(
            x_pos, y_pos, cell_size, cell_size))

# move the snake


def change_snake():
    global body, status

    if direction[0] or direction[1] != 0:
        body_copy = body[:-1]
        body_copy.insert(0, body_copy[0] + direction)
        if status == 'yes':
            body_copy.insert(0, body_copy[0] + Vector2(0, 0))
            status = 'no'
        body = body_copy[:]


def move_snake():
    global direction

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            if direction.y != 1:
                direction = Vector2(0, -1)
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            if direction.y != -1:
                direction = Vector2(0, 1)
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            if direction.x != -1:
                direction = Vector2(1, 0)
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            if direction.x != 1:
                direction = Vector2(-1, 0)

    # create the fruit
position = Vector2(random.randrange(1, cell_number - 1) *
                   cell_size, random.randrange(1, cell_number - 1) * cell_size)

fruit_rect = pygame.Rect(position.x, position.y, cell_size, cell_size)


def draw_fruit():
    pygame.draw.rect(screen, PURPLE, fruit_rect)

# change the fruit position


def change_rect():
    global fruit_rect
    fruit_rect = pygame.Rect(random.randrange(1, cell_number) * cell_size,
                             random.randrange(1, cell_number) * cell_size, cell_size, cell_size)


# score
score = 0
score_font = pygame.font.SysFont('consolas', 15)


def check_colision():
    global score, body_score, status
    if fruit_rect.x == head.x and fruit_rect.y == head.y:
        score += 1
        status = 'yes'
        change_rect()

    elif head.x > Widht - cell_size or head.x < 0:
        end_game()

    elif head.y > Height - cell_size or head.y < 0:
        end_game()

    for block in body[+2:]:
        block1 = block * 40
        if block1 == head:
            end_game()


def show_score():

    string = 'Score: ' + str(score)
    text = score_font.render(string, True, WHITE)
    screen.blit(text, (25, 15))

# text


def show_end_text():

    end_text = 'U lost!'
    end_text2 = 'Press "q" to leave'
    end_text_font = pygame.font.SysFont('consolas', 210)
    end_text_font2 = pygame.font.SysFont('consolas', 30)
    text = end_text_font.render(end_text, True, RED)
    text2 = end_text_font2.render(end_text2, True, WHITE)

    screen.blit(text, (10, 300))
    screen.blit(text2, (250, 500))


# dificulty
dificulty = 150  # 300 super ez
# 150 = normal
# 100 = hard
# 50 = super hard
# userevent
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, dificulty)

# fps controller
fps = 60
clock = pygame.time.Clock()

# end game


def end_game():
    global dead, run
    run = False
    dead = True

    while dead:
        clock.tick(fps)
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dead = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    dead = False

        show_end_text()
        pygame.display.update()


while run:
    clock.tick(fps)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.USEREVENT:
            change_snake()
        move_snake()

    show_score()
    draw_fruit()
    draw_snake()
    check_colision()
    pygame.display.update()

sys.exit()
