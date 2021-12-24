import selenium
import helper_functions as helper
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from dataclasses import dataclass


import time


def algorithm():
    coords = []
    # using chrome to access web
    driver = webdriver.Chrome()
    

    # open minesweeper.com
    driver.get('http://minesweeperonline.com/')
    
    # initial filling. -1 for blank, -2 for bomb
    grid = []
    for i in range(16):
        temp_row = []
        for j in range(30):
            temp_row.append(-1)
        grid.append(temp_row)


    # Select id of square (gonna have to change boxes to select)
    square = (9, 15)
    id_box = driver.find_element(By.ID, f'{square[0]}_{square[1]}')

    # click square
    id_box.click()
    
    done = False
    while not done:
        # each square type
        coords = helper.get_squares(driver)
        for i in range(len(coords)):
            for square in coords[i]:
                grid[square[0]][square[1]] = i
        # flagged bombs
        coords = helper.get_flags(driver)
        for square in coords:
            grid[square[0]][square[1]] = -2
        # print(grid)
        to_click, to_flag = helper.gimmes(grid)
        if len(to_click) == 0 and len(to_flag) == 0:
            done = True
        for square in to_flag:
            id_box = driver.find_element(By.ID, f'{square[0]}_{square[1]}')
            action = ActionChains(driver)
            try:
                action.context_click(id_box).perform()
            except Exception as e:
                print(e)
                print(square)
        for square in to_click:
            id_box = driver.find_element(By.ID, f'{square[0]}_{square[1]}')

            # click square
            try:
                id_box.click()
            except Exception as e:
                print(e)
                print(square)
    x = input("done: ")
    

    

    



def main():
    algorithm()
    

if __name__ == "__main__":
    main()