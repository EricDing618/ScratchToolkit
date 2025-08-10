import os,sys,pathlib
from ast import literal_eval as safe_eval
import json
import time
from textwrap import dedent
from typing import Any,Optional,Union,Tuple
from string import digits

def repath(path:str):
    return str(pathlib.Path(path).resolve(strict=True))
def init_path():
    sys.path.append(repath("../.."))

from numpy import array,where    
from loguru import logger as log
from art import text2art
log.remove()

THISPATH=os.getcwd()
LOCALDATE=time.strftime('%Y-%m-%d_%H：%M',time.localtime(time.time()))
LOGFORMAT="<level>[{time:YYYY-MM-DD HH:mm:ss}] [{level}]: {message}</level>"
'''if os.path.basename(THISPATH) != "STP":
    os.chdir('./src/scratchtoolkit/__STP')'''

with open("./src/__STP/frame/spriteframe.py","r",encoding="utf-8") as f:
    SPRITE_INIT_CODE='\n'.join([i.rstrip() for i in f.readlines() if 'import' not in i])
with open("./src/__STP/frame/gameframe.py","r",encoding="utf-8") as f:
    GAME_INIT_CODE='\n'.join([i.rstrip() for i in f.readlines() if 'import' not in i])
with open("./src/__STP/settings.json",'r',encoding='utf-8') as f:
    USERSET:dict=json.load(f)

__L='\n'.join('# '+i for i in text2art("Scratch-To-Pygame").splitlines())
HEAD=f'''\
{__L}
# Scratch-To-Pygame({USERSET['info']['version']})
# Made by EricDing618.
'''
if os.path.basename(os.getcwd()) == "STP":
    os.chdir('..')
