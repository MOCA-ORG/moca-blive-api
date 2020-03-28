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


# -- Imports --------------------------------------------------------------------------

from pathlib import Path
from aiofiles import open
from moca_core import N

# -------------------------------------------------------------------------- Imports --

# -- Variables --------------------------------------------------------------------------

log_file_path = str(Path(__file__).parent.parent.joinpath('log').joinpath('BliveCommentAPI.log'))

# -------------------------------------------------------------------------- Variables --

# -- Save Log --------------------------------------------------------------------------


async def save_log(log: str) -> None:
    async with open(log_file_path, mode='a', encoding='utf-8') as file:
        await file.write(log)
        await file.write(N)

# -------------------------------------------------------------------------- Save Log --
