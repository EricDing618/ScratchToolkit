import traceback
import argparse as ap
from art import text2art
from __STP.mypath import PathTool,repath,LOGDIR,LOGPATH
from __STP.reg import log,UnPackingScratch3File,CodeParser
from __STP.config import os,sys,LOGFORMAT,USERSET,json,time
from __STP.util import BlockID,installed

class STP:
    def __init__(self):
        log.add(sys.stdout,colorize=True,format=LOGFORMAT)
        self.parser=ap.ArgumentParser(description="The command list of Scratch-To-Pygame")
        self.parser.add_argument('--remove-log','-rmlog',dest='logcount',required=False, default=None,type=int,help="Remove the previous <logcount> log file(s).")
        self.parser.add_argument('-c','--convert',dest='file_path',default=None,type=str,help="Your .sb3 file's name or path.")
        self.parser.add_argument('--run','-r',dest="run",action="store_true",default=False,help="Run and check the output file.")
        self.parser.add_argument('--no-log','-nl',dest="no_log",action="store_true",default=False,help="Do not show the log.")
        self.parser.add_argument('--save-log','-sl',dest="save_log",action="store_true",default=False,help="Save the log to a file.")
        self.parser.add_argument('-t','--tree',dest="tree",action="store_true",default=False,help="Show the code tree.")
        self.parser.add_argument('-st','--save-tree',dest="tree_path",help="Save the code tree to a file.")
        self.args=self.parser.parse_args()

    def _start(self, fp:str='./tests/work1.sb3',args=None,):
        if args:
            log.debug(f'''
    ==========================
    {text2art('STP')}==========================
    Scratch-To-Pygame({USERSET['info']['version']}) is running!
        ''')
            info=UnPackingScratch3File(fp)
            info.convert()
            start=time.time()
            parser=CodeParser(info)
            parser.write_result()
            codetree=parser.code_tree()
            log.success(f"Converted successfully (in {repath(parser.outpyfile)}) .")
            log.success(f"Time used: {time.time()-start}s") #仅为积木转换时间，不包括解压缩及资源格式转换时间，与积木数量有关
            if args.tree:
                log.debug('Showing the code tree...')
                for i,j in codetree.items():
                    j=json.dumps(j,indent=2,ensure_ascii=False)
                    log.debug(f'{i}: {j}\n')
            if args.tree_path:
                with open(args.tree_path,'w',encoding='utf-8') as f:
                    json.dump(codetree,f,indent=4,ensure_ascii=False)
                log.debug(f'The code tree was saved in {args.tree_path}')
            if args.run:
                for i in codetree['requirements']:
                    error=False
                    if not installed(i):
                        log.debug(f'Installing {i}...')
                        if os.system(f'{sys.executable} -m pip install {i}'):
                            error=True
                    if not error:
                        log.success(f'Package/module {i} installed successfully.')
                    else:
                        log.error(f'Failed to install {i}.')
                log.debug('Trying to run the output file...')
                if os.system(f'python {parser.outpyfile}'):
                    log.error('There is something wrong above.')
                else:
                    log.success('The file has no wrong.')
            if args.save_log:
                log.debug(f'The log was written in {repath(LOGPATH)}')

    def parse(self):
        if self.args.save_log:
            log.add(LOGPATH,format=LOGFORMAT)
        if self.args.logcount is not None:PathTool().rmlog(repath(LOGDIR),self.args.logcount)
        fp=self.args.file_path
        if fp:
            if self.args.no_log:
                log.remove()
            try:
                self._start(fp,self.args)
            except SystemExit as e:
                if int(str(e)) != 0: #防止因SystemExit: 0导致的误报错
                    log.error(f'SystemExit: {e}')
            except BaseException:
                exc=traceback.format_exc()
                log.error('\n'+exc)

if __name__=='__main__':
    stp = STP()
    stp.parse()