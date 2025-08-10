from __STP.mypath import PackingScratch3File,log
from __STP.config import LOGFORMAT

import argparse as ap
import sys

if __name__ == '__main__':
    log.add(sys.stdout,colorize=True,format=LOGFORMAT)
    parser = ap.ArgumentParser(description='Packing scratch 3.0 project directory to sb3 file')
    parser.add_argument('project', type=str, help='path to the scratch 3.0 project directory')
    args=parser.parse_args()
    if args.project:
        try:
            PackingScratch3File(args.project)
        except Exception as e:
            log.error(f"Error while packing {args.project} to sb3 file: {e}")
