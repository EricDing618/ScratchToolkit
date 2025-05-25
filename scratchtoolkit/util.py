from js2py import eval_js
from pkg_resources import get_distribution,DistributionNotFound

OperatorSymbols=("+","-","*","/","%","==","!=","<",">","<=",">=")

def installed(name:str):
    try:
        get_distribution(name)
        return True
    except DistributionNotFound:
        return False
    
class Data:
    def __init__(self):
        self.pj:dict
        self.baseinfo={
            "semver":self.pj['meta']['semver'],
            "vm":self.pj['meta']['vm'],
            "agent":self.pj['meta']['agent'],
            "platform_name":self.pj['meta']['platform']['name'],
            "platform_url":self.pj['meta']['platform']['url']
            }
        self.mod={ #根据情况导入所需要的库
            "internal":{
                "typing":["",["Any"]],
                "math":["",[]],
                "random":["",[]],
                "sys":["",[]],
                "threading":["",["Thread","Timer"]]
                },
            "third-party":{
                "pygame->pygame-ce":["pg",[]],
                "js2py":["",["eval_js"]],
                "numpy":["",["array","where"]]
                }
            }
        self.var={ #存储变量
            "public":{},
            "private":{}
            }
        self.array={ #存储列表
            "public":{},
            "private":{}
            }

class BlockID:
    def __init__(self,_id:str,blocks:dict):
        self._id=_id
        self.blocks=blocks
    
    def __repr__(self) -> str:
        return f'BlockID("{self._id}")'

class SVariable:
    def __init__(self,name:str,value:str):
        self.name='self.var_'+name
        self.value=value

class SArray:
    def __init__(self,name:str,value:list):
        self.name='self.arr_'+name
        self.value=value


class SFunc:
    def __init__(self,name:str,args=()):
        self.name=name
        self.args=args
    def __repr__(self):
        return f'SFunc({self.name}({", ".join(self.args)}))'
    def get_tuple(self):
        result_list = []
        length = len(self.args) 
        for i in range(length):
            result_list.append(self.args[i])
            if i < length - 1:
                result_list.append(Symbol(','))
        return (self.name,Symbol('('),*result_list,Symbol(')'))

class Symbol:
    def __init__(self,symbol:str|SFunc):
        self.symbol=symbol
    def is_func(self):
        return isinstance(self.symbol,SFunc)
    def __repr__(self) -> str:
        return f'Symbol("{self.symbol}")'

class SNumber:
    def __init__(self,num:int|float):
        self.num=num
    def __repr__(self) -> str:
        return f'SNumber({self.num})'
    
class ReduceJSCode:
    def __init__(self,code:list):
        self.code=code
        self.result=[]
        for i,j in enumerate(self.code):
            next_=self.code[i+1]
            if j in OperatorSymbols and isinstance(next_,str):
                self.result.append(j+next_)
            elif isinstance(next_,(SArray,SVariable)):
                self.result.append(j+next_.name)
    def reduce(self):
        return self.result