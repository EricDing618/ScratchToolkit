'''
class Function():
    def __init__(self):
        self.func:dict[Sprite,dict[str,]]={}
        self.args:dict[Sprite,dict[str,tuple]]={}
    def add(self,sp:Sprite,func:str,exec,args=()):
        if self.func.get(sp,{}).get(func):
            self.func[sp][func]+=exec
            self.args[sp][func]+=args
        else:
            self.func[sp]={func:exec}
            self.args[sp]={func:args}
    def run(self,sp:Sprite,func:str):
        exec=self.func[sp][func]
        args=self.args[sp][func]
        for e,a in zip(exec,args):
            e(*a)

class CodeParser():
    def __functool(self,mutation:dict,args:Union[str,Tuple[str,...]]="",func=False,free=False):
        type={'%s':'int|float|str','%b':'bool'}
        name=[]
        argtypes=[]
        c=mutation['proccode'].split(' ')
        for i in range(len(c)):
            if c[i].isidentifier():
                if i==0 or not c[i-1].isidentifier():
                    name.append(c[i])
                else:
                    name[-1]+=c[i]
            else:
                argtypes.append(c[i])

        funcname='_'+'_'.join(name)
        if funcname not in self.funccode: #创建函数
            self.funccode[funcname]=[{},{}]
        for argname,argdefault,argtype in zip(eval(mutation['argumentnames']),eval(mutation['argumentdefaults']),argtypes):
            self.funccode[funcname][0][argname.replace(' ','_')]=[argdefault,type.get(argtype,'Any')] #type: ignore 
        if not func:
            if not free:
                self.funccode[funcname][1]['self.'+self.opcode+'('+', '.join(args)+')']=self.depth
            else:
                self.funccode[funcname][1][args]=self.depth
'''