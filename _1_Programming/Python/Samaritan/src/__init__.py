__version__ = '0.0.1'
from src.common.logger_utils import setup_logging
from common.path_utils import PathUtil
from sys import path as sys_path

path_util = PathUtil()
BASEDIR = path_util.root_path
sys_path.append(BASEDIR)

logger = setup_logging(BASEDIR + '/src/common/logging.json')
