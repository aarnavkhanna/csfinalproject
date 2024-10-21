import pygame
import random
import time

pygame.init()

width, height = 625, 625
game_window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fun Snake Game")

start_x, start_y = 312, 312
x_change, y_change = 10, 0
Rapple_x, Rapple_y = random.randrange(0, width, 20), random.randrange(0, height, 20)

snake_body = [(start_x, start_y)]

def snake_game():
    global start_x, start_y, x_change, y_change, Rapple_x, Rapple_y
    start_x = (start_x + x_change) % width
    start_y = (start_y + y_change) % height
    
    snake_body.append((start_x, start_y))
    
    if start_x == Rapple_x and start_y == Rapple_y:
        while (Rapple_x, Rapple_y) in snake_body:
            Rapple_x, Rapple_y = random.randrange(0, width, 20), random.randrange(0, height, 20)
    else:
        del snake_body[0]

    game_window.fill((0, 0, 0))
    pygame.draw.rect(game_window, (255, 0, 0), [Rapple_x, Rapple_y, 20, 20])
    for i, j in snake_body:
        pygame.draw.rect(game_window, (85, 107, 47), [i, j, 20, 20])
    pygame.display.update()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and x_change != 10:
                x_change = -10
                y_change = 0
            elif event.key == pygame.K_RIGHT and x_change != -10:
                x_change = +10
                y_change = 0
            elif event.key == pygame.K_UP and y_change != 10:
                x_change = 0
                y_change = -10
            elif event.key == pygame.K_DOWN and y_change != -10:
                x_change = 0
                y_change = +10

    snake_game()
    time.sleep(0.06)

pygame.quit()