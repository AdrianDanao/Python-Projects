import time
import random
import pygame
from config import *
from score import load_top_scores, update_top_scores, display_top_scores

# Load scores
top_scores = load_top_scores()

def draw_grid():
    for x in range(0, width, cell_size):
        for y in range(0, height, cell_size):
            rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(screen, gray, rect, 1)

def your_score(score):
    value = score_font.render(f"Your Score: {score}", True, blue)
    screen.blit(value, [10, 10])

def our_snake(block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, white, [x[0], x[1], block_size, block_size])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [width / 6, height / 3])

def save_top_score(length_of_snake):
    global top_scores
    screen.fill(black)
    message("Enter your initials (3 letters):", red)
    pygame.display.update()
    initials = []
    while len(initials) < 3:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    initials.append(event.unicode.upper())
                elif event.key == pygame.K_BACKSPACE and initials:
                    initials.pop()
        screen.fill(black)
        message("Enter your initials (3 letters): " + ''.join(initials), red)
        pygame.display.update()
    name = ''.join(initials)
    update_top_scores(name, length_of_snake - 1, top_scores)

def gameLoop():
    time.sleep(1)
    game_over = False
    game_close = False

    x1, y1 = width / 2, height / 2
    x1_change, y1_change = 0, 0

    snake_list = []
    length_of_snake = 1

    foods = []
    for _ in range(num_foods):
        foodx = round(random.randrange(0, width - cell_size) / cell_size) * cell_size
        foody = round(random.randrange(0, height - cell_size) / cell_size) * cell_size
        foods.append((foodx, foody))

    direction = None

    while not game_over:
        while game_close:
            screen.fill(black)
            message("You lost! Press Q-Quit or C-Play Again", red)
            your_score(length_of_snake - 1)
            display_top_scores(top_scores)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        save_top_score(length_of_snake)
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        save_top_score(length_of_snake)
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_a] and direction != "RIGHT":
                    x1_change, y1_change = -cell_size, 0
                    direction = "LEFT"
                elif event.key in [pygame.K_RIGHT, pygame.K_d] and direction != "LEFT":
                    x1_change, y1_change = cell_size, 0
                    direction = "RIGHT"
                elif event.key in [pygame.K_UP, pygame.K_w] and direction != "DOWN":
                    x1_change, y1_change = 0, -cell_size
                    direction = "UP"
                elif event.key in [pygame.K_DOWN, pygame.K_s] and direction != "UP":
                    x1_change, y1_change = 0, cell_size
                    direction = "DOWN"

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(black)

        draw_grid()

        for foodx, foody in foods:
            pygame.draw.rect(screen, red, [foodx, foody, cell_size, cell_size])
        
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        our_snake(cell_size, snake_list)
        your_score(length_of_snake - 1)
        display_top_scores(top_scores)

        pygame.display.update()

        for i, (foodx, foody) in enumerate(foods):
            if x1 == foodx and y1 == foody:
                foods[i] = (round(random.randrange(0, width - cell_size) / cell_size) * cell_size, 
                            round(random.randrange(0, height - cell_size) / cell_size) * cell_size)
                length_of_snake += 1
                eat_sound.play()

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
