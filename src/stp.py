import traceback
import argparse as ap

def main(fp:str='./tests/work1.sb3',args:ap.Namespace=ap.Namespace()):
    if args:
        log.debug(dedent(f'''
    ==========================
     ____    _____   ____  
    / ___|  |_   _| |  _ \ 
    \___ \    | |   | |_) |
     ___) |   | |   |  __/ 
    |____/    |_|   |_|    
    ==========================
    Scratch-To-Pygame({USERSET['info']['version']}) is running!
    '''))
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
                if isinstance(j,BlockID):
                    j=j.blocks
                elif isinstance(j,(dict,list,tuple)):
                    j=json.dumps(j,indent=2,ensure_ascii=False)
                log.debug(f'{i}: {j}\n')
        if args.tree_path:
            with open(args.tree_path,'w',encoding='utf-8') as f:
                json.dump(codetree,f,indent=4,ensure_ascii=False)
            log.debug(f'The code tree was saved in {args.tree_path}')
        if args.run:
            for i in codetree['requirements']:
                if not installed(i):
                    log.debug(f'Installing {i}...')
                    os.system(f'{sys.executable} -m pip install {i}')
                log.success(f'Package {i} installed successfully.')
            log.debug('Trying to run the output file...')
            if os.system(f'python {parser.outpyfile}'):
                log.error('There is something wrong above.')
            else:
                log.success('The file has no wrong.')
        if args.save_log:
            log.debug(f'The log was written in {repath(LOGPATH)}')

if __name__=='__main__':
    from __STP.mypath import PathTool,repath,LOGDIR,LOGPATH
    from __STP.core import log,UnPackingScratch3File,CodeParser
    from __STP.config import os,sys,LOGFORMAT,USERSET,dedent,json,time
    from util import BlockID,installed

    log.add(sys.stdout,colorize=True,format=LOGFORMAT)
    parser=ap.ArgumentParser(description="The command list of Scratch-To-Pygame")
    parser.add_argument('--remove-log','-rmlog',dest='logcount',required=False, default=None,type=int,help="Remove the previous <logcount> log file(s).")
    parser.add_argument('-c','--convert',dest='file_path',default=None,type=str,help="Your .sb3 file's name or path.")
    parser.add_argument('--run','-r',dest="run",action="store_true",default=False,help="Run and check the output file.")
    parser.add_argument('--no-log','-nl',dest="no_log",action="store_true",default=False,help="Do not show the log.")
    parser.add_argument('--save-log','-sl',dest="save_log",action="store_true",default=False,help="Save the log to a file.")
    parser.add_argument('-t','--tree',dest="tree",action="store_true",default=False,help="Show the code tree.")
    parser.add_argument('-st','--save-tree',dest="tree_path",help="Save the code tree to a file.")
    args=parser.parse_args()
    if args.save_log:
        log.add(LOGPATH,format=LOGFORMAT)
    if args.logcount is not None:PathTool().rmlog(repath(LOGDIR),args.logcount)
    fp=args.file_path
    if fp:
        if args.no_log:
            log.remove()
        try:
            main(fp,args)
        except SystemExit as e:
            if int(str(e)) != 0: #防止因SystemExit: 0导致的误报错
                log.error(f'SystemExit: {e}')
        except BaseException:
            exc=traceback.format_exc()
            log.error('\n'+exc)