import os

from WebSocket.WebSocket import WebSocket
from storage.Database import Database
from utils.utils import read_config


config = read_config('config.json')
DB = Database(
    host=config['db_host'],
    port=config['db_port'],
    user=config['db_user'],
    password=config['db_password'],
    dbname=config['db_db'],
)
_host = config.get('ws_host', '0.0.0.0')
_port = int(os.environ.get('PORT', config['ws_port']))  # get environment variable "PORT" or port from config
WS = WebSocket(port=_port, host=_host)
