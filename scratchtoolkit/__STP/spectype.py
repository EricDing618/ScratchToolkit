from .config import Tuple,Union,init_path,safe_eval
init_path()
from scratchtoolkit.util import *

class BlockBuffer:
    def __init__(self):
        self.buffer={}
    def add(self,id:str,value:tuple):
        self.buffer[id]=value
    def get(self,id:str,default=[]):
        a=self.buffer.get(id,default)
        return a
    def update(self):
        for id,values in dict(self.buffer).items():
            self.bigupdate(id,values)

    def bigupdate(self,_id="",values=(),recursive=False):
        a=[]
        for i in range(len(values)):
            value=values[i]
            if isinstance(value,(int,float,list)):
                a.append(str(value))
            elif isinstance(value,str):
                a.append("\""+value+"\"")
            elif isinstance(value,Symbol):
                a.append(value.symbol)
            elif isinstance(value,SFunc):
                a.append(*value.get_tuple())
            elif isinstance(value,BlockID):
                a.extend(self.bigupdate(_id,(Symbol('('),*self.buffer[value._id],Symbol(')')),True))
            elif isinstance(value,(SArray,SVariable)):
                '''在InputParser/VarListParser中处理'''
        if recursive:
            return a
        else:
            self.buffer[_id]=a
        print('bigupdate-in-a',self.buffer,a,_id,values)

class InputParser:
    def __init__(self,blocks:dict,buffer:BlockBuffer):
        """
        解析含参型积木块，生成python代码。
        """
        self.blocks=blocks
        self.buffer=buffer
        self.code=[]
    def generate(self,block:list[str,dict],symbol=Symbol('=='),args=[],binput='',types=[int,int]):
        '''注意：symbol必须为js运算符/内置函数名/关键词'''
        self.id,self.idinfo=block
        self.args=[]
        for i,t in zip(args,types):
            self.args.append(t(i))
        if symbol.is_func(): #内置函数
            self.buffer.add(self.id,(SFunc(symbol[:-2],args)))
        else:
            match len(args):
                case 1:
                    self.buffer.add(self.id,(symbol,args[0],args[1]))
                case 2:
                    b=[]
                    for i in range(2):
                        a=self.idinfo['inputs'][f'{args[0]}{i+1}'][1]
                        if isinstance(a,str):
                            b.append(BlockID(a,self.blocks))
                        elif isinstance(a[1],str):
                            if a[1].isdigit():
                                b.append(int(a[1]))
                            else:
                                b.append(float(a[1]))
                    self.buffer.add(self.id,(b[0],Symbol(args[1]),b[1]))

class VarListParser:
    def __init__(self,blocks:dict):
        """
        解析变量及列表型积木块，生成python代码。
        """
        self.blocks=blocks

class FuncParser:
    def __init__(self,blocks:dict,baseblock:dict):
        """
        解析函数型积木块，生成python代码。
        """
        self.blocks=blocks
        self.base=baseblock
        self.funcmuta=self.blocks[self.base['inputs']['custom_block'][1]]['mutation']
        self.type={'%s':'int|float|str','%b':'bool'}
        self.name=[]
        self.argtypes=[]
        c=self.funcmuta['proccode'].split(' ')
        for i in range(len(c)):
            if self.isidentifier(c[i]):
                if i==0 or not self.isidentifier(c[i-1]):
                    self.name.append(c[i])
                else:
                    self.name[-1]+=c[i]
            else:
                self.argtypes.append(c[i])
        self.funcname='_'+'_'.join(self.name)
    def isidentifier(self,s:str):
        """
        判断参数字符串是否为合法的标识符。
        """
        r=True
        for i in '!@#$%^&*()/\\+-=[]{}|;:,.<>?':
            if i in s:
                r=False
                break
        return r
    
    def create(self,funccode:dict):
        self.funccode=funccode
        if self.funcname not in self.funccode: #创建函数
            self.funccode[self.funcname]=[{},{}]
        for argname,argdefault,argtype in zip(safe_eval(self.funcmuta['argumentnames']),safe_eval(self.funcmuta['argumentdefaults']),self.argtypes):
            self.funccode[self.funcname][0][argname.replace(' ','_')]=[argdefault,self.type.get(argtype,'Any')] #type: ignore 
    
    def addcode(self,free=False,args:Union[str,Tuple[str,...]]="",opcode:str="",depth:int=0):
        if not free:
            self.funccode[self.funcname][1]['self.'+opcode+'('+', '.join(args)+')']=depth
        else:
            self.funccode[self.funcname][1][args]=depth
        
    def update(self):
        return self.funccode