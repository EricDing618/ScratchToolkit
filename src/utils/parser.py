from box import Box
import json, zipfile, pathlib
from typing import Literal

class SB3parser:
    def __init__(self, sb3file:str):
        self.sb3file = sb3file
    def read(self, type_:Literal['core','image','music']='core'):
        self.files = {}
        match type_:
            case 'image':
                suffix = ('.svg','.png','.jpg')
            case 'music':
                suffix = ('.wav','.mp3')
            case _:
                suffix = ('.json',)
        with zipfile.ZipFile(self.sb3file, 'r') as zf:
            for fn in zf.namelist():
                if pathlib.Path(fn).suffix in suffix:
                    with zf.open(fn) as f:
                        if '.json' in suffix:
                            self.files[fn] = json.loads(f.read())
                        else:
                            self.files[fn] = f.read()
        self.files = Box(self.files)
        return self.files
class ProjectParser:
    def __init__(self, pj:dict):
        self.pj = Box(pj)
        self.blocks :dict = self.pj.targets.blocks
        self.groups :dict[str,list] = {}
    def get_groups(self):
        for id, block in self.blocks.items():
            if not block.parent:
                self.groups[id] = [block,]
                next_=block.next
                while next_:
                    _block = self.blocks[next_]
                    self.groups[id].append(_block)
                    next_ = _block.next
        return self.groups

if __name__=='__main__':
    sb3=SB3parser(r"D:\gitclone\ScratchToolkit\tests\sb3files\blocktest.sb3")
    pp=ProjectParser(sb3.read()['project.json'])
    print(pp.get_groups())