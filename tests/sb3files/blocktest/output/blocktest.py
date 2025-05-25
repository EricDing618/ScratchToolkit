#  ____                      _          _             _____                ____                                        
# / ___|   ___  _ __   __ _ | |_   ___ | |__         |_   _|  ___         |  _ \  _   _   __ _   __ _  _ __ ___    ___ 
# \___ \  / __|| '__| / _` || __| / __|| '_ \  _____   | |   / _ \  _____ | |_) || | | | / _` | / _` || '_ ` _ \  / _ \
#  ___) || (__ | |   | (_| || |_ | (__ | | | ||_____|  | |  | (_) ||_____||  __/ | |_| || (_| || (_| || | | | | ||  __/
# |____/  \___||_|    \__,_| \__| \___||_| |_|         |_|   \___/        |_|     \__, | \__, | \__,_||_| |_| |_| \___|
#                                                                                 |___/  |___/                         
# Scratch-To-Pygame(Beta v0.0.1)
# Made by EricDing618.

from typing import Any
import math
import random
import sys
from threading import Thread, Timer
import pygame as pg
from js2py import eval_js
from numpy import array, where

class JSObject:
    def __init__(self,obj):
        self.obj=obj
    def __eq__(self,other):
        return str(self.obj)==str(other.obj)
    def __ne__(self,other):
        return str(self.obj)!=str(other.obj)
    def __add__(self,other):
        if isinstance(self.obj,str) or isinstance(other.obj,str):
            return str(self.obj)+str(other.obj)
        else:
            return float(self.obj)+(other.obj)
    def __str__(self):
        return str(self.obj)
    def __repr__(self):
        return str(self.obj)

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

    def get_mapping(self,key):
        # Key maps to convert the key option in blocks to pygame constants
        self.KEY=array(['up arrow', 'down arrow', 'left arrow', 'right arrow', 'space', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'enter', '<', '>', '+', '-', '=', '.', ',', '%', '$', '#', '@', '!', '^', '&', '*', '(', ')', '[', ']', '?', '\\', '/', "'", '"', '`', 'backspace', 'escape', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12'])
        self.BIND=array([pg.K_UP,pg.K_DOWN,pg.K_LEFT,pg.K_RIGHT,pg.K_SPACE,pg.K_a,pg.K_b,pg.K_c,pg.K_d,pg.K_e,pg.K_f,pg.K_g,pg.K_h,pg.K_i,pg.K_j,pg.K_k,pg.K_l,pg.K_m,pg.K_n,pg.K_o,pg.K_p,pg.K_q,pg.K_r,pg.K_s,pg.K_t,pg.K_u,pg.K_v,pg.K_w,pg.K_x,pg.K_y,pg.K_z,pg.K_0,pg.K_1,pg.K_2,pg.K_3,pg.K_4,pg.K_5,pg.K_6,pg.K_7,pg.K_8,pg.K_9,pg.K_RETURN, pg.K_LESS, pg.K_GREATER, pg.K_PLUS, pg.K_MINUS, pg.K_EQUALS, pg.K_PERIOD, pg.K_COMMA, pg.K_PERCENT, pg.K_DOLLAR, pg.K_HASH, pg.K_AT, pg.K_EXCLAIM, pg.K_CARET, pg.K_AMPERSAND, pg.K_ASTERISK, pg.K_LEFTPAREN, pg.K_RIGHTPAREN, pg.K_LEFTBRACKET, pg.K_RIGHTBRACKET, pg.K_QUESTION, pg.K_BACKSLASH, pg.K_SLASH, pg.K_QUOTE, pg.K_QUOTEDBL, pg.K_BACKQUOTE, pg.K_BACKSPACE, pg.K_ESCAPE, pg.K_F1, pg.K_F2, pg.K_F3, pg.K_F4, pg.K_F5, pg.K_F6, pg.K_F7, pg.K_F8, pg.K_F9, pg.K_F10, pg.K_F11, pg.K_F12])
        return self.BIND[where(self.KEY == key)[0][0]] if key in self.KEY else None

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



class Game:
    def __init__(self):
        pg.init() #初始化
        screen = pg.display.set_mode((800,600)) #舞台大小为800,600
        pg.display.set_caption('blocktest')

if __name__=='__main__':
   rungame=Game()