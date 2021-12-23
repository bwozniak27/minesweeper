import selenium
import helper_functions as helper
from selenium import webdriver
from selenium.webdriver import ActionChains
from dataclasses import dataclass


import time
default = float('-inf')


def algorithm():
    # using chrome to access web
    driver = webdriver.Chrome()
    

    # open minesweeper.com
    driver.get('http://minesweeperonline.com/')
    
    # initial filling. negative inf for default
    # grid is rows of cols, at each space is (num of probabilies for avg, avg)
    #grid = [ [ [default, default], [default, default] ] ]
    grid = []
    temp_list = [default, default]
    for i in range(17):
        temp_row = []
        for j in range(31):
            temp_row.append(temp_list)
        grid.append(temp_row)


    # Select id of square (gonna have to change boxes to select)
    square = (9, 15)
    id_box = driver.find_element_by_id('{}_{}'.format(square[0], square[1]))

    # click square
    id_box.click()

    while True:
        grid = helper.calculate(driver, grid)
        if grid == True:
            while True:
                word = input('press k to kill, else to continue: ')
                if word == 'k':
                    return
        max = 0
        max_square = (1, 1)
        for row in range(1, 17):
            for col in range(1, 31):
                if grid[row][col][1] > max:
                    max = grid[row][col][1]
                    max_square = (row, col)
                
                if grid[row][col][1] == 0:
                    id_box = driver.find_element_by_id('{}_{}'.format(row, col))
                    id_box.click()

    

    



def main():
    algorithm()
    

if __name__ == "__main__":
    main()