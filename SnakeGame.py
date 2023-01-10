# write a simple snake game
# install pygame

import os
import pygame
import random
import time

# initialize pygame
pygame.init()

# define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# define game window
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game')

# define game clock
clock = pygame.time.Clock()

# define snake
snake_block = 10
snake_speed = 15

# define font
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# define functions
def Your_score(score):
    value = score_font.render("Score: " + str(score), True, blue)
    gameDisplay.blit(value, [5, 0])

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(gameDisplay, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    gameDisplay.blit(mesg, [display_width / 6, display_height / 3])

def write_score (score):
    # create the files scoreboard.txt in the same directory as the game
    try:
        score_file = open("/Users/noahelrimawi-fine/MyWorkspace/scoreboard.txt", "r")
        score_file.close()
    except:
        score_file = open("/Users/noahelrimawi-fine/MyWorkspace/scoreboard.txt", "w")
        score_file.close()
    # write the score to the file
    score_file = open("/Users/noahelrimawi-fine/MyWorkspace/scoreboard.txt", "a")
    score_file.write(str(score) + " ")
    score_file.close()

    # first check if the score is in the top 5
    score_list = scoreboard()
    if len(score_list) < 5:
        score_list.append(score)
    else:
        score_list[4] = score
    score_list.sort()
    score_list.reverse()
    score_list = score_list[:5]


# define scoreboard
def scoreboard ():
    # read the scores from the file
    score_file = open("/Users/noahelrimawi-fine/MyWorkspace/scoreboard.txt", "r")
    score_list = score_file.read()
    score_file.close()
    score_list = score_list.split()
    score_list = [int(i) for i in score_list]
    score_list.sort()
    score_list.reverse()
    score_list = score_list[:5]
    # print the scores
    gameDisplay.fill(white)
    message("Scoreboard", black)
    for i in range(len(score_list)):
        value = score_font.render(str(i + 1) + ". " + str(score_list[i]), True, blue)
        gameDisplay.blit(value, [display_width / 6, display_height / 3 + (i + 1) * 50])
    pygame.display.update()
    time.sleep(2)
    return score_list


def gameLoop(): 
    game_over = False
    game_close = False

    x1 = display_width / 2
    y1 = display_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    # define food
    foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            gameDisplay.fill(white)
            message("You Lost! Press Q-Quit or C-Play Again. Top Scores displayed on Quit", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        # display the scoreboard and write the score to the file
                        write_score(Length_of_snake - 1)
                        scoreboard()
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    x1_change = 0
                    y1_change = -snake_block
                elif event.key == pygame.K_DOWN:
                    x1_change = 0
                    y1_change = snake_block

        if x1 >= display_width - 10 or x1 < 0 or y1 >= display_height or y1 < 10:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        gameDisplay.fill(white)
        # add black boundaries to the game
        pygame.draw.rect(gameDisplay, black, [0, 0, display_width, 10])
        pygame.draw.rect(gameDisplay, black, [0, 0, 10, display_height])
        pygame.draw.rect(gameDisplay, black, [0, display_height - 10, display_width, 10])
        pygame.draw.rect(gameDisplay, black, [display_width - 10, 0, 10, display_height])
        

        pygame.draw.rect(gameDisplay, green, [foodx, foody, snake_block, snake_block]) # type: ignore        
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1 ]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()

