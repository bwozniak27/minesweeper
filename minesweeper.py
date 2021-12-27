import selenium
from helper_functions import Minesweeper
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from dataclasses import dataclass


import time


def main():
    solver = Minesweeper()
    solver.run()

if __name__ == "__main__":
    main()