import random
import time
import copy
import pygame
import sys
from math import floor

Cell_map = []
size = int(input("How many cells accross? "))
tick_speed_input = float(input("What tick speed? (0 for none) "))
 ##Make cells
for i in range (0,size):
    temp = []
    for x in range(0, size):
        temp.append(0)
    Cell_map.append(temp)


def Num_of_neigbours(y_axis, x_axis):
    # Define relative neighbor coordinates
    relative_coords = [
        (1, 1), (-1, 1), (1, -1), (-1, -1),
        (0, 1), (0, -1), (1, 0), (-1, 0)
    ]

    # Initialize neighbor count
    int_to_return = 0

    # Check each neighbor
    for dy, dx in relative_coords:
        ny, nx = y_axis + dy, x_axis + dx
        if 0 <= ny < size and 0 <= nx < size:
            if Cell_map[ny][nx] == 1:
                int_to_return += 1

    return int_to_return


def Create_new_map():
    ###make list of all map co ordinates
    co_ordinates = []
    for i in range(0, size):
        temp_co_ordinates = []
        for x in range(0, size):
            temp_co_ordinates.append([i,x])
        co_ordinates.append(temp_co_ordinates)


    ###create blank new map
    New_map = []
    for i in range(0, size):
        temp = []
        for x in range(0, size):
            temp.append(0)
        New_map.append(temp)

    ###fill in map
    i_count = 0
    for i in New_map:
        x_count = 0
        for x in i:
            if (Cell_map[i_count][x_count] == 0) and (Num_of_neigbours(i_count,x_count) == 3):
                New_map[i_count][x_count] = 1
            elif (Cell_map[i_count][x_count] == 1) and ((Num_of_neigbours(i_count,x_count) == 2) or (Num_of_neigbours(i_count,x_count) == 3)):
                New_map[i_count][x_count] = 1
            elif (Cell_map[i_count][x_count] == 1) and (Num_of_neigbours(i_count, x_count) < 3):
                New_map[i_count][x_count] = 0
            else:
                New_map[i_count][x_count] = 0
            x_count += 1
        i_count += 1
    return New_map


pygame.init()
desired_size = 1080
pixels_per_cell = round(desired_size/size)
screen = pygame.display.set_mode((size*pixels_per_cell, size*pixels_per_cell))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
clock = pygame.time.Clock()


### cell coordinate grid
coordinate_grid = []
for i in range (0,size):
    temp = []
    for x in range(0, size):
        temp_2 = [x*pixels_per_cell, i*pixels_per_cell]
        temp.append(temp_2)
    coordinate_grid.append(temp)

if tick_speed_input == 0:
    sleep_time = 0
else:
    sleep_time = 1/tick_speed_input


size_of_square = pixels_per_cell
time_check = time.time()


def draw_map():
    screen.fill(BLACK)
    for x in coordinate_grid:
        for y in x:
            if Cell_map[round(y[1] / pixels_per_cell)][round(y[0] / pixels_per_cell)] == 1:
                pygame.draw.rect(screen, WHITE, (y[1], y[0], size_of_square, size_of_square))
    pygame.display.flip()


enter_key_not_pressed = True
while enter_key_not_pressed:
    draw_map()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if event.type == pygame.MOUSEBUTTONDOWN:
        time_since_last_check = time.time() - time_check
        time_check = time.time()
        if time_since_last_check > 0.1:
            mouse_pos = pygame.mouse.get_pos()
            x_pos = int(floor(mouse_pos[0]/pixels_per_cell))
            y_pos = int(floor(mouse_pos[1]/pixels_per_cell))
            if Cell_map[x_pos][y_pos] == 0:
                Cell_map[x_pos][y_pos] = 1
            elif Cell_map[x_pos][y_pos] == 1:
                Cell_map[x_pos][y_pos] = 0
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            enter_key_not_pressed = False


size_of_square = pixels_per_cell
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    draw_map()
    Cell_map = copy.deepcopy(Create_new_map())
    time.sleep(sleep_time)
