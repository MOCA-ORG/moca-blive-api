# Ω*
#               ■          ■■■■■  
#               ■         ■■   ■■ 
#               ■        ■■     ■ 
#               ■        ■■       
#     ■■■■■     ■        ■■■      
#    ■■   ■■    ■         ■■■     
#   ■■     ■■   ■          ■■■■   
#   ■■     ■■   ■            ■■■■ 
#   ■■■■■■■■■   ■              ■■■
#   ■■          ■               ■■
#   ■■          ■               ■■
#   ■■     ■    ■        ■■     ■■
#    ■■   ■■    ■   ■■■  ■■■   ■■ 
#     ■■■■■     ■   ■■■    ■■■■■


"""
Copyright (c) 2020.5.28 [el.ideal-ideas]
This software is released under the MIT License.
see LICENSE.txt or following URL.
https://www.el-ideal-ideas.com/MocaSystem/LICENSE/
"""


# -- Imports --------------------------------------------------------------------------

from docopt import docopt
from .moca_utils import print_warning, print_info, print_license
from .moca_core_db import put, get, delete
from shutil import rmtree
from pathlib import Path
from sys import exit
from leveldb import LevelDBError

# -------------------------------------------------------------------------- Imports --

# -- Console --------------------------------------------------------------------------


def console():
    __doc__ = """
    
    Welcome to moca_modules.
    
    Usage:
        moca.py <module> <command> [<values>...]
        moca.py --help | -h
        moca.py --license
        
    Details:
        core-db clear
            Clear moca-core-database. Don't run this command when your system is running.
        core-db put <key: string> <value: string>
            Add a data to moca-core-database. Don't run this command when your system is running.
        core-db get <key: string>
            Get a data from moca-core-database. Don't run this command when your system is running.
        core-db delete <key: string>
            Delete a data from moca-core-database. Don't run this command when your system is running.
    
    """

    args = docopt(__doc__)

    if args['-h'] or args['--help']:
        print(__doc__)
    elif args['--license']:
        print_license()
    elif args['<module>'] == 'core-db':
        if args['<command>'] == 'clear':
            print_warning("This command will clear the moca-core-database."
                          " Don't run this command when your system is running.")
            while True:
                print('continue? [Y/n]', end='')
                res = input()
                if res in ('Y', 'Yes', 'yes', 'y', ' ', ''):
                    rmtree(str(Path(__file__).parent.joinpath('storage').joinpath('core.db')))
                    Path(__file__).parent.joinpath('storage').joinpath('core-tiny-db.json').unlink()
                    print_info("moca-core-database was cleared.")
                    exit(0)
                elif res in ('N', 'No', 'no', 'n'):
                    exit(0)
        elif args['<command>'] == 'put':
            if len(args['<values>']) == 2:
                try:
                    if put(args['<values>'][0].encode(), args['<values>'][1]):
                        print_info("Success!")
                    else:
                        print_warning("Failed...")
                except LevelDBError:
                    print_warning("Resource temporarily unavailable.")
            else:
                print_warning("Arguments number error.")
        elif args['<command>'] == 'get':
            if len(args['<values>']) == 1:
                try:
                    print(get(args['<values>'][0].encode()))
                except LevelDBError:
                    print_warning("Resource temporarily unavailable.")
            else:
                print_warning("Arguments number error.")
        elif args['<command>'] == 'delete':
            if len(args['<values>']) == 1:
                try:
                    print(delete(args['<values>'][0].encode()))
                except LevelDBError:
                    print_warning("Resource temporarily unavailable.")
            else:
                print_warning("Arguments number error.")
        else:
            print_warning("Unknown command.")
    else:
        print_warning("Unknown module.")

# -------------------------------------------------------------------------- Console --
