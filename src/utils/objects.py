class Project:
    def __init__(self, pj: dict):
        self.pj:dict = pj

        self.targets:list[dict] = [Sprite(target) for target in pj['targets']]
        self.monitors:list[dict] = pj['monitors']
        self.extensions:list[str] = pj['extensions']
        self.meta:dict = pj['meta']

        self.semver:str = self.meta['semver']
        self.vmver:str = self.meta['vm']
        self.agent:str = self.meta['agent']
        self.platform:str = self.meta['platform']
    
    def __repr__(self):
        class_name = self.__class__.__name__
        attrs = ', '.join(f'{k}={v!r}' for k, v in vars(self).items())
        return f'{class_name}({attrs})'

class Sprite:
    def __init__(self, target: dict):
        self.target:dict = target

        self.isStage:bool = target['isStage']
        self.name:str = target['name']
        self.vars:dict[str, list] = target['variables']
        self.lists:dict[str, list] = target['lists']
        self.broadcasts:dict[str, str] = target['broadcasts']
        self.blocks = {block_id: Block(block_id, **block) for block_id, block in target['blocks'].items()}
        self.comments = target['comments']
        self.currentCostumeIndex = target['currentCostume']
        self.costumes:list[dict] = target['costumes']
        self.sounds = target['sounds']
        self.volume = target['volume']
        self.layerOrder = target['layerOrder']
        self.tempo = target['tempo']
        self.videoTransparency = target['videoTransparency']
        self.videoState = target['videoState']
        self.textToSpeechLanguage = target['textToSpeechLanguage']
    
    def __repr__(self):
        class_name = self.__class__.__name__
        attrs = ', '.join(f'{k}={v!r}' for k, v in vars(self).items())
        return f'{class_name}({attrs})'

class Block:
    def __init__(self, id:str, **kwargs):
        self.id:str = id
        self.opcode:str = kwargs.get('opcode', '')
        self.next:str|None = kwargs.get('next', None)
        self.parent:str|None = kwargs.get('parent', None)
        self.inputs:dict = kwargs.get('inputs', {})
        self.fields:dict = kwargs.get('fields', {})
        self.shadow:bool = kwargs.get('shadow', False)
        self.topLevel:bool = kwargs.get('topLevel', False)
        self.x:int|None = kwargs.get('x', None)
        self.y:int|None = kwargs.get('y', None)
        self.isHead:bool = all([self.x, self.y])

    def __repr__(self):
        class_name = self.__class__.__name__
        attrs = ', '.join(f'{k}={v!r}' for k, v in vars(self).items())
        return f'{class_name}({attrs})'    
        