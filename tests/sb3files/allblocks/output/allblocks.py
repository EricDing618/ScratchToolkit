#  ____                          _            _               _____                   ____                                             
# / ___|    ___   _ __    __ _  | |_    ___  | |__           |_   _|   ___           |  _ \   _   _    __ _    __ _   _ __ ___     ___ 
# \___ \   / __| | '__|  / _` | | __|  / __| | '_ \   _____    | |    / _ \   _____  | |_) | | | | |  / _` |  / _` | | '_ ` _ \   / _ \\
#  ___) | | (__  | |    | (_| | | |_  | (__  | | | | |_____|   | |   | (_) | |_____| |  __/  | |_| | | (_| | | (_| | | | | | | | |  __/
# |____/   \___| |_|     \__,_|  \__|  \___| |_| |_|           |_|    \___/          |_|      \__, |  \__, |  \__,_| |_| |_| |_|  \___|
#                                                                                             |___/   |___/                            
# Scratch-To-Pygame(Beta v0.0.1)
# Made by EricDing618.

from typing import Any
import math
import random
import sys
from threading import Thread, Timer
import pygame as pg

class Sprite(pg.sprite.Sprite,Thread): #角色框架
    def __init__(self, image_file:tuple[str], initxy:tuple[int,int], direction:int):
        super().__init__()
        self.image:pg.Surface
        self.images={}
        for i in image_file:
            self.images[i]=pg.image.load(i)
        self.rect = self.image.get_rect() if self.image else pg.Rect(0,0,0,0)
        self.direction=direction
        self.rect.x,self.rect.y=initxy
        self.start()



    def motion_gotoxy(self,dx:float,dy:float):
        self.rect.move_ip(dx,dy)
    def motion_glidesecstoxy(self,dx:float,dy:float,duration:int|float):
        distance=duration * 10
        if self.rect:
            if dx != self.rect.x:
                dx=distance*math.cos(math.radians(self.direction))
            if dy != self.rect.y:
                dy=distance*math.sin(math.radians(self.direction))

    def motion_turnright(self, degrees):
        self.image = pg.transform.rotate(self.image, degrees)
    def control_wait(self,s:float):
        Timer(s,lambda:0).start()

class stage_Stage(Sprite):
    def __init__(self):
        super().__init__()


class spr_角色1(Sprite):
    def __init__(self):
        super().__init__()
                self.control_wait(1)
        while True:
        else:

    def _def_labeltext(self, number_or_text:int|float|str="", boolean:bool=False):
        self.control_wait(1)

    def _积木名称_labeltext(self, number_or_text:int|float|str="", boolean:bool=False):
        ...
    def _self(self):
        ...


class Game:
    def __init__(self):
        pg.init() #初始化
        screen = pg.display.set_mode((800,600)) #舞台大小为800,600
        pg.display.set_caption('allblocks')

if __name__=='__main__':
   rungame=Game()