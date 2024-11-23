import pygame
import random
import time

pygame.init()

width, height = 600, 600
game_screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

x, y = 200, 200
delta_x, delta_y = 20, 0

food_x, food_y = random.randrange(0, width, 20), random.randrange(0, height, 20)
blue_food_x, blue_food_y = -20, -20

body_list = [(x, y)]

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)

game_over = False
inverted_controls = False
inverted_timer = 0
next_blue_apple_time = 0
score = 0

game_mode = None


def menu():
    global game_mode
    menu_font = pygame.font.SysFont(None, 50)
    title_font = pygame.font.SysFont(None, 60)
    
    while True:
        game_screen.fill((0, 0, 0))
        title_text = title_font.render("Snake Game", True, (255, 255, 255))
        classic_text = menu_font.render("Classic Mode", True, (255, 0, 0))
        frenzy_text = menu_font.render("Blue Frenzy", True, (0, 0, 255))
        
        game_screen.blit(title_text, (width // 3, height // 4))
        game_screen.blit(classic_text, (width // 3, height // 2))
        game_screen.blit(frenzy_text, (width // 3, height // 2 + 50))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if width // 3 <= mouse_x <= width // 3 + 200 and height // 2 <= mouse_y <= height // 2 + 40:
                    game_mode = 'classic'
                    return
                if width // 3 <= mouse_x <= width // 3 + 200 and height // 2 + 50 <= mouse_y <= height // 2 + 90:
                    game_mode = 'blue_frenzy'
                    return


def snake():
    global x, y, food_x, food_y, blue_food_x, blue_food_y, body_list, game_over, inverted_controls, inverted_timer, next_blue_apple_time, score
    x += delta_x
    y += delta_y

    if x < 0 or x >= width or y < 0 or y >= height:
        game_over = True

    if (x, y) in body_list:
        game_over = True

    body_list.append((x, y))

    if food_x == x and food_y == y:
        while (food_x, food_y) in body_list:
            food_x, food_y = random.randrange(0, width, 20), random.randrange(0, height, 20)
        score += 1
    elif blue_food_x == x and blue_food_y == y:
        while (blue_food_x, blue_food_y) in body_list:
            blue_food_x, blue_food_y = -20, -20
        inverted_controls = True
        inverted_timer = pygame.time.get_ticks()
        next_blue_apple_time = pygame.time.get_ticks() + 40000
        score += 3
    else:
        del body_list[0]

    game_screen.fill((0, 0, 0))
    score_text = font.render("Score: " + str(score), True, (255, 255, 0))
    game_screen.blit(score_text, [0, 0])
    pygame.draw.rect(game_screen, (255, 0, 0), (food_x, food_y, 20, 20))
    if game_mode == 'blue_frenzy':
        pygame.draw.rect(game_screen, (0, 0, 255), (blue_food_x, blue_food_y, 20, 20))
    for i, j in body_list:
        pygame.draw.rect(game_screen, (85, 107, 47), (i, j, 20, 20))
    pygame.display.update()

menu()

while True:
    if game_over:
        game_screen.fill((0, 0, 0))
        score_text = font.render("Score: " + str(score), True, (255, 255, 0))
        game_screen.blit(score_text, [0, 0])
        text = font.render("Game Over!", True, (255, 255, 255))
        game_screen.blit(text, (width // 3, height // 3))
        pygame.display.update()
        time.sleep(5)
        pygame.quit()
        quit()

    if inverted_controls and pygame.time.get_ticks() - inverted_timer > 20000:
        inverted_controls = False

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if inverted_controls:
                if event.key == pygame.K_LEFT and delta_x != -20:
                    delta_x = 20
                    delta_y = 0
                elif event.key == pygame.K_RIGHT and delta_x != 20:
                    delta_x = -20
                    delta_y = 0
                elif event.key == pygame.K_UP and delta_y != -20:
                    delta_x = 0
                    delta_y = 20
                elif event.key == pygame.K_DOWN and delta_y != 20:
                    delta_x = 0
                    delta_y = -20
            else:
                if event.key == pygame.K_LEFT and delta_x != 20:
                    delta_x = -20
                    delta_y = 0
                elif event.key == pygame.K_RIGHT and delta_x != -20:
                    delta_x = 20
                    delta_y = 0
                elif event.key == pygame.K_UP and delta_y != 20:
                    delta_x = 0
                    delta_y = -20
                elif event.key == pygame.K_DOWN and delta_y != -20:
                    delta_x = 0
                    delta_y = 20

    if game_mode == 'blue_frenzy' and blue_food_x == -20 and pygame.time.get_ticks() >= next_blue_apple_time:
        blue_food_x, blue_food_y = random.randrange(0, width, 20), random.randrange(0, height, 20)

    snake()
    clock.tick(10)

pygame.quit()
