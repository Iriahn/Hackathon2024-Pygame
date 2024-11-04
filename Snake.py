#Imports
import pygame
import time
import random

from pygame.mixer import unpause
from enum import Enum

def main():
    #Speed and window size
    SNAKE_SPEED = 15
    WINDOW_X = 720
    WINDOW_Y = 480

    #Defining colors
    class Color(pygame.Color, Enum):
        BLACK = pygame.Color(0, 0, 0)
        WHITE = pygame.Color(51, 47, 44)
        RED = pygame.Color(139, 0, 0)
        GREEN = pygame.Color(151, 255, 111)
        BLUE = pygame.Color(0, 0, 128)

    #Starts game
    pygame.init()

    pygame.display.set_caption('Snake Game')
    game_window = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
    fps = pygame.time.Clock()

    snake_position = [100, 50]
    snake_body = [ [100, 50], [90, 50], [80, 50], [70, 50] ]

    fruit_position = [random.randrange(1, (WINDOW_X//10))*10, random.randrange(1, (WINDOW_Y//10))*10]
    fruit_spawn = True

    direction = 'RIGHT'
    change_to = direction

    score = 0

    def show_score(choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score: ' + str(score), True, color)
        score_rect = score_surface.get_rect()
        game_window.blit(score_surface, score_rect)

    def game_over():
        my_font = pygame.font.SysFont('futuristic', 50)
        game_over_surface = my_font.render('Your Score is: ' + str(score), True, Color.RED)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (WINDOW_X/2, WINDOW_Y/4)
        game_window.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        time.sleep(2)

        pygame.quit()
        quit()

    def pause():
        paused = True
        large_text = pygame.font.SysFont('futuristic', 50)
        paused_surface = large_text.render('Paused', True, Color.BLACK)
        paused_rect = paused_surface.get_rect()
        paused_rect.center = ((WINDOW_X/2), (WINDOW_Y/2))
        game_window.blit(paused_surface, paused_rect)
        pygame.display.flip()

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = False
                        unpause()
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()

    #Main function
    while True:
        for event in pygame.event.get():
            #When pressing the keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
                if event.key == pygame.K_SPACE:
                    paused = True
                    pause()

        #When pressing two keys simultaneously
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        #Snake movement
        #Get fruit, +10 in score
        if direction == 'UP':
            snake_position[1] -= 10
        if direction == 'DOWN':
            snake_position[1] += 10
        if direction == 'LEFT':
            snake_position[0] -= 10
        if direction == 'RIGHT':
            snake_position[0] += 10

        #Snake growth
        snake_body.insert(0, list(snake_position))
        if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
            score += 10
            fruit_spawn = False
        else:
            snake_body.pop()

        if not fruit_spawn:
            fruit_position = [random.randrange(1, (WINDOW_X // 10)) * 10, random.randrange(1, (WINDOW_Y // 10)) * 10]
        fruit_spawn = True
        game_window.fill(Color.GREEN)

        for pos in snake_body:
            pygame.draw.rect(game_window, Color.BLUE, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(game_window, Color.RED, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

        #Game Over
        if snake_position[0] < 0 or snake_position[0] > WINDOW_X-10:
            game_over()
        if snake_position[1] < 0 or snake_position[1] > WINDOW_Y-10:
            game_over()

        #Snake touches itself
        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                game_over()

        #Score display
        show_score(1, Color.WHITE, 'futuristic', 30)
        #Refresh screen
        pygame.display.update()
        #Refresh rate
        fps.tick(SNAKE_SPEED)
if __name__ == "__main__":
    main()
