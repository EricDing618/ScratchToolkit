from .config import os,json,USERSET,LOCALDATE,THISPATH,log,Optional,Union,Tuple,repath,init_path
init_path()

import zipfile
import xml.etree.ElementTree as ET
import shutil

from cairosvg import svg2png
from PIL import Image

class PathTool:
    def __init__(self,fp:Optional[str|tuple[str, str]]=None,mode='p'):
        '''mode = 'p': fp是一个文件路径;    
           mode = 'n': fp是一个文件名; 
           mode = 'd': fp是一个目录路径;  
           mode = 'j': 只合并路径，fp的类型为tuple[str,str]。'''
        if fp:
            if isinstance(fp,str): 
                fp=os.path.normpath(fp)
                self.NAME:str
                match mode:
                    case 'p':
                        self.DIR=os.path.dirname(fp)
                        self.FILE=os.path.basename(fp)
                        self.NAME,self.SUFFIX=os.path.splitext(self.FILE)
                    case 'n':
                        self.FILE=fp
                        self.NAME,self.SUFFIX=os.path.splitext(fp)
                    case 'd':
                        self.DIR=fp
                        self.NAME=os.path.basename(fp)
            elif mode=='j':
                self.j=os.path.join(*(os.path.normpath(p) for p in fp))
    def rmlog(self,dirpath:str,count:int=0):
        # 获取目录中的所有文件
        files = os.listdir(dirpath)
        if len(files) >= count:
            # 过滤出文件，而不是目录
            files = [f for f in files if os.path.isfile(os.path.join(dirpath, f))]
            if count:
                # 获取每个文件的修改时间，并按照修改时间排序
                files.sort(key=lambda f: os.path.getmtime(os.path.join(dirpath, f)))
                for i in range(count):
                    os.remove(os.path.join(dirpath,files[i]))
            else:
                for f in files:
                    os.remove(os.path.join(dirpath,f))
    def join(self,args:Union[str,Tuple[str,...]]=("",)):
        if hasattr(PathTool,'j'):
            return self.j
        elif args and len(args)!= 0:
            return os.path.join(*(os.path.normpath(p) for p in args))
        
LOGPATH=PathTool().join((USERSET['log']['outdir'] if USERSET['log']['outdir'] != "default" else "./../../log",LOCALDATE+".log")) #type: ignore
LOGDIR=os.path.dirname(LOGPATH)

class UnPackingScratch3File:
    def __init__(self,fp:str):
        """
        解包.sb3文件。
        
        :param fp: .sb3文件位置
        """
        log.debug(f"Unpacking {repath(fp)}...")
        with zipfile.ZipFile(fp,'r') as self.f: #解压.sb3文件
            if os.path.basename(fp)!=fp: #如果是一段路径
                self.p=PathTool(fp)
                self.cdir=self.p.join((self.p.DIR,self.p.NAME))
            else: #如果是一段文件名
                self.p=PathTool(fp,mode='n')
                self.cdir=self.p.join((THISPATH,self.p.NAME))
            self.f.extractall(self.cdir)

            #格式化.json文档
            self.prj_path=self.p.join((self.cdir,'project.json'))
            with open(self.prj_path,'r',encoding='utf-8') as f:
               c=json.load(f)
            with open(self.prj_path,'w',encoding='utf-8') as f:
                json.dump(c,f,ensure_ascii=False,indent=4)
        log.success(f"Completed unpacking {repath(fp)} -> {repath(self.cdir)}.")

    def convert(self):
        self.outdir=self.p.join((self.cdir,'output'))
        os.makedirs(self.outdir,exist_ok=True)
        for fn in os.listdir(self.cdir): #批量转换
            p=PathTool(fn,'n')
            if p.SUFFIX=='.svg':
                fp=p.join((self.cdir,p.FILE))
                #with open(p.join((self.cdir,p.FILE)), 'r',encoding='utf-8') as f:
                #    svg_size = surface.SVGSurface(f.read(),).width, surface.SVGSurface(p.join((self.cdir,p.FILE))).height
                tree = ET.parse(fp)
                root = tree.getroot()
                svg_size = float(root.attrib['width']), float(root.attrib['height'])
                png_path = p.join((self.cdir,"output",p.NAME+".png"))
                if svg_size != (0,0):
                    log.debug(f"The size of {repath(fp)} is {svg_size}.")
                    svg2png(url=fp,
                            write_to=png_path,
                            unsafe=True,
                            parent_width=svg_size[0],
                            parent_height=svg_size[1])
                else:
                    log.warning(f"{fn} has no size!")
                    image = Image.new("RGB",(1, 1),(0,0,0))
                    image.save(png_path)
                #os.remove(p.join((self.cdir,p.FILE)))
                #log.success(f"Removed {p.join((self.cdir,p.FILE))}.")
                log.success(f"Converted {repath(fp)} -> {repath(png_path)}.")


class PackingScratch3File:
    def __init__(self,dp:str):
        """
        打包.sb3文件。
        
        :param dp: .sb3文件解包后文件夹位置
        """
        log.debug(f"Packing {dp}...")
        self.p=PathTool(dp,'d')
        fp=['project.json']
        with open(self.p.join((self.p.DIR,'project.json')),'r',encoding='utf-8') as f:
            c=json.load(f)
        for t in c['targets']:
            for i in t['costumes']:
                if i['md5ext'] in os.listdir(self.p.DIR): 
                    fp.append(i['md5ext'])
            for s in t['sounds']:
                if s['md5ext'] in os.listdir(self.p.DIR): 
                    fp.append(s['md5ext'])
        self.outdir=self.p.join((self.p.DIR,'output'))
        os.makedirs(self.outdir,exist_ok=True)
        self.outfile=self.p.join((self.outdir,self.p.NAME+'.sb3'))
        with zipfile.ZipFile(self.outfile,'w') as f:
            for i in fp:
                f.write(self.p.join((self.p.DIR,i)),i)
        log.success(f"Completed packing {repath(dp)} -> {repath(self.outfile)}.")
