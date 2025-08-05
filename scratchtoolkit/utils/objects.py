class Sprite:
    def __init__(self, target: dict):
        self.target:dict = target

        self.isStage:bool = target['isStage']
        self.name:str = target['name']
        self.vars:dict[str, list] = target['variables']
        self.lists:dict[str, list] = target['lists']
        self.broadcasts:dict[str, str] = target['broadcasts']
        self.blocks:dict = target['blocks']
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
        