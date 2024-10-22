import os
from connections import WS
from utils.utils import read_config


import blueprints.users as users
import blueprints.fragments as fragments
users.register_callbacks()
fragments.register_callbacks()


if __name__ == '__main__':
    config = read_config('config.json')
    port = int(os.environ.get('PORT', config['ws_port']))  # get environment variable "PORT" or port from config
    WS.start(thread=True)
    WS.waitThread()
