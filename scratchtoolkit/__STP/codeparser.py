from .config import USERSET,json,SPRITE_INIT_CODE,GAME_INIT_CODE,HEAD,Any,Union,Tuple,digits,repath,init_path
init_path()
from .mypath import log,UnPackingScratch3File,PathTool
from .spectype import FuncParser,BlockBuffer,InputParser,VarListParser
from scratchtoolkit.util import *

class CodeParser(Data):
    def __init__(self,last:UnPackingScratch3File):
        """
        转换核心，解析project.json并生成python代码。
        """
        self.buffer=BlockBuffer()
        self.cdir,self.outdir=last.cdir,last.outdir
        self.t=PathTool(self.cdir)
        with open(self.t.join((self.cdir,"project.json")),'r',encoding='utf-8') as f: #导入project.json
            self.pj=json.load(f)
        super().__init__()
        self.last=last

        self.depth=0 #默认深度
        self.code:list[str]=[] #存储代码（总）
        self.gamecode:list[str]=[] #存储游戏代码
        self.gamecode.extend(GAME_INIT_CODE.splitlines()) #游戏初始化代码
        self.sprcode:dict[str,dict]={} #所有角色代码汇总
        self.targets=self.pj["targets"] #所有角色信息
        self.fstr(f"pg.display.set_caption('{last.p.NAME}')",4)
        for t in self.targets:
            self.give(t)
            self.sprcode[self.classname]=self.funccode #保存角色代码
            self.funccode={"__init__":[{},{"super().__init__()":0}]} #恢复默认

    def give(self,tgs:dict): #给予信息,tgs为targets下每个信息
        #为方便后面操作
        self.isStage:bool=tgs['isStage'] #是否为舞台
        self.name:str=tgs['name'] #角色名
        self.vars:dict=tgs['variables'] #变量
        self.lists:dict=tgs['lists'] #列表
        self.broadcasts:dict=tgs['broadcasts'] #广播
        self.blocks:dict=tgs["blocks"] #积木块
        self.sounds:list=tgs["sounds"] #音频
        self.volume:int=tgs['volume'] #音量
        self.layerOrder:int=tgs["layerOrder"] #角色的图层顺序，值越大，角色越靠前
        
        if self.isStage: #舞台，有些全局设置
            self.tempo:int=tgs['tempo'] #正常速度为60
            self.comments:dict=tgs['comments'] #键是注释的ID，值是注释的内容
            self.currentCostume:int=tgs['currentCostume'] #角色的当前服装索引
            self.costumes:list[dict]=tgs['costumes'] #角色的服装
            self.videoTransparency:int=tgs['videoTransparency'] #角色的视频透明度，范围是0到100，0表示完全透明，100表示完全不透明
            self.videoState:str=tgs['videoState'] #角色的视频状态，可以是on（开启视频）或off（关闭视频）。
            self.textToSpeechLanguage:str=tgs['textToSpeechLanguage'] #角色的文本到语音语言
            self.classname='stage_'+self.name
        else:
            self.visible:bool=tgs.get("visible",True) #角色是否可见
            self.x:float=tgs['x'] #x坐标
            self.y:float=tgs['y'] #y坐标
            self.size:int=tgs['size'] #放大与缩小，100是原始尺寸
            self.direction:int=tgs['direction'] #朝向，0度表示朝右，90度表示朝上，180度表示朝左，270度表示朝下
            self.draggable:bool=tgs['draggable'] #角色的可拖动性
            self.rotation:str=tgs['rotationStyle'] #角色的旋转样式，可以是all around（围绕中心点旋转）、left-right（左右旋转）或don't rotate（不旋转）
            self.classname='spr_'+self.name
        self.funccode={"__init__":[{},{"super().__init__()":0}]} #代码（角色下函数）
        for block in self.blocks.items():
            self.sleep=False
            self.id,self.idinfo=block
            if isinstance(self.idinfo,dict): #一般积木块
                self.opcode=self.idinfo["opcode"]
                if not self.idinfo['shadow'] and self.opcode not in USERSET["blocks"]['ignore']: #不隐藏且不被忽略的积木块
                    self.depth,self.base=self.get_nested_depth(self.id,self.idinfo)
                    self.add()
                    self.depth=0 #恢复默认
            else: #自定义变量、列表类型
                self.myvarlist(self.idinfo)
    def myvarlist(self,kw): #自定义变量、列表管理
        ...
    def add(self): #积木管理
        type_=f"{self.classname} -> {self.id}"
        log.debug(f'Converting {type_} (name="{self.opcode}" ,depth={self.depth})...')
        if self.sleep:
            self.depth+=1

    def fstr(self,string:str|dict="",mode=0,args=()):
        '''
        mode=0: 调用积木方法，string不填，args为传参  
        mode=1: 创建一个函数，string为mutation，args不填   
        mode=2: 灵活性的，args不填，string是代码（如判断、循环等）  
        mode=3: 角色基础信息，string为代码，args不填  
        mode=4: 游戏基础信息，string为代码，args不填  
        mode=5: 列表、变量管理，string为代码，args不填   
        mode=6: 含参类，args为（inputs开头参数名，运算符）  
        '''
        args=list(str(i) for i in args)
        match mode:
            case 0:
                if self.base.get('opcode','')=='procedures_definition': #在某个函数下
                    func=FuncParser(self.blocks,self.base)
                    func.create(self.funccode)
                    func.addcode(False,args,self.opcode,self.depth)
                    self.funccode=func.update()
                else: #在角色下
                    self.funccode['__init__'][1]['self.'+self.opcode+'('+', '.join(args)+')']=self.depth
            case 1:
                if isinstance(string,dict):
                    func=FuncParser(self.blocks,self.base)
                    func.create(self.funccode)
                    self.funccode=func.update()
                else:
                    raise ValueError("Invalid mutation!")
            case 2:
                if self.base.get('opcode','')=='procedures_definition': #在某个函数下
                    funcmutation=self.blocks[self.base['inputs']['custom_block'][1]]['mutation']
                    if isinstance(string,str):
                        func=FuncParser(self.blocks,self.base)
                        func.create(self.funccode)
                        func.addcode(True,string,self.opcode,self.depth)
                        self.funccode=func.update()
                    else:
                        raise ValueError("Invalid code!")
                else: #在角色下
                    self.funccode['__init__'][1][string]=self.depth
            case 3:
                self.funccode['__init__'][1][string]=0 #角色基础信息，无需深度
            case 4:
                self.gamecode.append('        '+string)
            case 5:
                ...
            case 6:
                op=args[1] if args[1] else self.opcode+'()'
                ip=InputParser(self.blocks,self.buffer)
                ip.generate([self.id,self.idinfo],Symbol(op),)
            case _:
                raise ValueError("Invalid mode!")

    def get_nested_depth(self,id:str,block:dict,depth=0):
        """
        递归函数，用于计算积木块的嵌套深度。
        
        :param id: 当前积木块的ID
        :param block: 当前积木块
        :param depth: 当前深度
        :return: 积木块的嵌套深度
        """
        pid=block.get('parent','')
        if pid:
            parentdict=self.blocks.get(pid,{}) #父积木块
            if parentdict:
                inputs=parentdict.get('inputs',{}) #父积木块的输入
                substack=inputs.get("SUBSTACK",[]) #父积木块的子积木块
                if parentdict['opcode'] not in USERSET["blocks"]['ignore'] and not block.get('topLevel'): #父积木块不被忽略且不是顶层积木块
                    if not block["shadow"]: #不隐藏的纯积木块
                        if id in substack: #嵌套类型
                            return self.get_nested_depth(pid,parentdict, depth+1)
                        else:
                            return self.get_nested_depth(pid,parentdict, depth)
                    else:
                        return self.get_nested_depth(pid,parentdict, depth)
        return depth,block

    def write_result(self):
        self.buffer.update() #更新嵌套缓存区
        self.builtins=[] #存储导入的内置库
        self.requirements=[] #存储第三方库依赖
        self.code.append(HEAD) #加入头注释
        #生成导入库代码
        for type_,modinfo in self.mod.items():
            for name,args in modinfo.items():
                if '->' in name: #fix: 修复pygame与pygame-ce的名称冲突
                    name,real=name.split('->')
                    self.requirements.append(real)
                elif type_=='third-party':
                    self.requirements.append(name)
                else:
                    self.builtins.append(name)
                if not args[0] and not args[1]:
                    self.code.append(f"import {name}")
                elif args[0] and not args[1]:
                    self.code.append(f"import {name} as {args[0]}")
                elif not args[0] and args[1]:
                    self.code.append(f"from {name} import {', '.join(args[1])}")
                else:
                    c=[]
                    for i,j in zip(args[0],args[1]):
                        c.append(f"{j} as {i}")
                    self.code.append(f"from {name} import {', '.join(c)}")

        #生成角色初始化代码
        for i in SPRITE_INIT_CODE.splitlines():
            self.code.append(i)
        self.code.append("")

        # 生成角色转换代码
        for sprname,funccode in self.sprcode.items():
            self.code.append(f"class {sprname}(Sprite):")
            for funcname,funcinfo in funccode.items():
                if funcinfo[0]: #有参数
                    c=[]
                    for argname,arginfo in funcinfo[0].items():
                        argdefault=arginfo[0] if arginfo[0] else '""' if arginfo[0]=="" else 'None'
                        if arginfo[1] in ('Any','int|float|str'):
                            c.append(f"{argname}:{arginfo[1]}={argdefault}")
                        elif arginfo[1]=='bool':
                            c.append(f"{argname}:{arginfo[1]}={argdefault.capitalize()}")
                    self.code.append(f"    def {funcname}(self, {', '.join(c)}):")
                else: #无参数
                    self.code.append(f"    def {funcname}(self):")
                if funcinfo[1]: #有代码
                    for line,depth in funcinfo[1].items():
                        if line.startswith('id='): #输入类型占位标识
                            code=self.buffer.get(line[3:],"")
                            self.code.append('    '*(depth+2)+code)
                        self.code.append('    '*(depth+2)+line)
                    self.code.append("")
                else: #无代码
                    self.code.append("        ...")

            self.code.append("")

        # 生成游戏初始化代码
        for i in self.gamecode:
            self.code.append(i)

        # 生成运行入口
        self.code.extend([
            "",
            "if __name__=='__main__':",
            "   rungame=Game()"
        ])

        # 写入转换结果
        self.outpyfile=self.t.join((self.outdir,self.last.p.NAME+".py"))
        with open(self.outpyfile,'w',encoding='utf-8') as f:
            f.write('\n'.join(self.code))
        with open(self.t.join((self.outdir,"requirements.txt")),'w',encoding='utf-8') as f:
            f.write('\n'.join(self.requirements))

    def code_tree(self):
        return {
            "project_info": self.baseinfo,
            "import_modules": self.mod,
            "built-in_modules": self.builtins,
            "requirements": self.requirements,
            "variables": self.var,
            "lists": self.array,
            "block_buffer": self.buffer.buffer,
            "sprite_code": self.sprcode,
            "game_code": self.gamecode,
            "outpyfile": repath(self.outpyfile)
        }