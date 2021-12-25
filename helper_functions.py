import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from dataclasses import dataclass
import unittest



# get surrounding tiles
def get_surrounding_tiles(grid, row, col):
    # check for edges
    # print(f'square: {row}_{col}')
    unopened = []
    bombs = []

    # top left
    if row - 1 >= 0 and col - 1 >= 0:
        if grid[row - 1][col - 1] == -1:
            unopened.append((row - 1, col - 1))
        elif grid[row - 1][col - 1] == -2:
            bombs.append((row - 1, col - 1))

    # top middle
    if row - 1 >= 0:
        if grid[row - 1][col] == -1:
            unopened.append((row - 1, col))
        elif grid[row - 1][col] == -2:
            bombs.append((row - 1, col))

    # top right
    if row - 1 >= 0 and col + 1 < len(grid[0]):
        if grid[row - 1][col + 1] == -1:
            unopened.append((row - 1, col + 1))
        elif grid[row - 1][col + 1] == -2:
            bombs.append((row - 1, col + 1))

    # middle left
    if col - 1 >= 0:
        if grid[row][col - 1] == -1:
            unopened.append((row, col - 1))
        elif grid[row][col - 1] == -2:
            bombs.append((row, col - 1))

    # middle right
    if col + 1 < len(grid[0]):
        if grid[row][col + 1] == -1:
            unopened.append((row, col + 1))
        elif grid[row][col + 1] == -2:
            bombs.append((row, col + 1))

    # lower left
    if row + 1 < len(grid) and col - 1 >= 0:
        if grid[row + 1][col - 1] == -1:
            unopened.append((row + 1, col - 1))
        elif grid[row + 1][col - 1] == -2:
            bombs.append((row + 1, col - 1))

    # lower middle
    if row + 1 < len(grid):
        if grid[row + 1][col] == -1:
            unopened.append((row + 1, col))
        elif grid[row + 1][col] == -2:
            bombs.append((row + 1, col))
    
    # lower right
    if row + 1 < len(grid) and col + 1 < len(grid[0]):
        if grid[row + 1][col + 1] == -1:
            unopened.append((row + 1, col + 1))
        elif grid[row + 1][col + 1] == -2:
            bombs.append((row + 1, col + 1))

    return unopened, bombs


# calculate chance of bomb for each square, higher number, higher chance of bomb
# TODO: find way to only check squares with unopened squares around it
def calculate(board):
    probabilities = []
    for row in range(len(board)):
        temp =[]
        for col in range(len(board[row])):
            temp.append([])
        probabilities.append(temp)
    # print("probabilities: ", probabilities)
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == -1 or board[row][col] == -2 or board[row][col] == 0:
                continue
            unopened, bombs = get_surrounding_tiles(board, row, col)
            if len(unopened) > 6:
                continue
            num_bombs = board[row][col] - len(bombs)
            # print("unopened: ", unopened)
            for box in unopened:
                # print(f'appending {box}')
                probabilities[box[0]][box[1]].append(round(float(num_bombs) / len(unopened), 2))
    
    # print("probabilities: ", probabilities)
    for row in range(len(probabilities)):
        # print("row: ", probabilities[row])
        for col in range(len(probabilities[row])):
            if len(probabilities[row][col]) != 0:
                average = sum(probabilities[row][col]) / len(probabilities[row][col])
                probabilities[row][col] = round(average, 2)
            else:
                probabilities[row][col] = 2
    # print(probabilities)
    min_val = min(min(row) for row in probabilities)
    # square = [(i, probabilities.index(min_val)) for i, square in enumerate(probabilities) if min_val in square]
    square = []
    for i, row in enumerate(probabilities):
        if min_val in row:
            square = (i, row.index(min_val))
            break
    return (square[0] + 1, square[1] + 1)

def get_squares(driver):
    coords = []
    for i in range(9):
        boxes = driver.find_elements(By.CLASS_NAME, f'square.open{i}')
        temp = []
        for box in boxes:
            Id = box.get_attribute('id')
            Id = Id.split('_')
            square = (int(Id[0]) - 1, int(Id[1]) - 1)
            temp.append(square)
        coords.append(temp)
        
    return coords

def gimmes(board):
    to_flag = []
    to_click = []
    done = False
    while not done:
        restart = False
        for row in range(len(board)):
            if restart == True:
                break
            for col in range(len(board[row])):
                # still will call issue for edge squares
                if board[row][col] == -1 or board[row][col] == -2 or board[row][col] == 0:
                    continue
                unopened, bombs = get_surrounding_tiles(board, row, col)
                num = board[row][col] - len(bombs)
                
                # if all surrounding squares are bombs
                if num > 0 and num == len(unopened): 
                    for box in unopened:
                        board[box[0]][box[1]] = -2
                        to_flag.append((box[0] + 1, box[1] + 1))
                    restart = True
                    break
                if len(unopened) > 0 and num == 0:
                    for box in unopened:
                        board[box[0]][box[1]] = 0
                        to_click.append((box[0] + 1, box[1] + 1))
                    restart = True
                    break
        if restart == False:
            done = True
    # print(board)
    return to_click, to_flag

def get_flags(driver):
    coords = []
    boxes = driver.find_elements(By.CLASS_NAME, 'square.bombflagged')
    for box in boxes:
        Id = box.get_attribute('id')
        Id = Id.split('_')
        square = (int(Id[0]) - 1, int(Id[1]) - 1)
        coords.append(square)
        
    return coords



