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
Copyright (c) 2020.1.17 [el.ideal-ideas]
This software is released under the MIT License.
see LICENSE.txt or following URL.
https://www.el-ideal-ideas.com/MocaLog/LICENSE/
"""


# -- Imports --------------------------------------------------------------------------

from sanic.log import logger, LOGGING_CONFIG_DEFAULTS
from .. import core

# -------------------------------------------------------------------------- Imports --

# -- Setup Logging --------------------------------------------------------------------------


def setup_logging(log_level: int) -> None:
    """
    Setup logging for sanic application.
    This function must be called before instantiate the Sanic.
    """
    logger.setLevel(log_level)
    LOGGING_CONFIG_DEFAULTS['handlers']['root_file'] = {
        'class': 'logging.FileHandler',
        'formatter': 'generic',
        'filename': str(core.LOG_DIR.joinpath('sanic_root.log'))
    }
    LOGGING_CONFIG_DEFAULTS['handlers']['error_file'] = {
        'class': 'logging.FileHandler',
        'formatter': 'generic',
        'filename': str(core.LOG_DIR.joinpath('sanic_error.log'))
    }
    LOGGING_CONFIG_DEFAULTS['handlers']['access_file'] = {
        'class': 'logging.FileHandler',
        'formatter': 'access',
        'filename': str(core.LOG_DIR.joinpath('sanic_access.log'))
    }
    LOGGING_CONFIG_DEFAULTS['loggers']['sanic.root']['handlers'][0] = 'root_file'
    LOGGING_CONFIG_DEFAULTS['loggers']['sanic.error']['handlers'][0] = 'error_file'
    LOGGING_CONFIG_DEFAULTS['loggers']['sanic.access']['handlers'][0] = 'access_file'

# -------------------------------------------------------------------------- Setup Logging --
