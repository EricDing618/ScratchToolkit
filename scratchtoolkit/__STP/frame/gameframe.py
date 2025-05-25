import pygame as pg

class Game:
    def __init__(self):
        pg.init() #初始化
        screen = pg.display.set_mode((800,600)) #舞台大小为800,600