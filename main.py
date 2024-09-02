import logging, eventlet, sys, os
from eventlet import wsgi

# no cache files for python
sys.dont_write_bytecode = True

from modules.log import LOG
from modules.config import Config
from modules.strings import Console
from modules.tools import network
from modules.flask import app, FlaskAPP
from modules.thread import thread
from modules.image import Scan

if __name__ == '__main__':
    try:
        UPLOAD_FOLDER = os.path.join(os.getcwd(), 'dir')
        if not os.path.exists(UPLOAD_FOLDER):
            LOG.error(Console.DirFolder.value)
            #os.makedirs(UPLOAD_FOLDER)
        else:
            thread(Scan())
            FlaskAPP()
            LOG.info(Console.NetworkInfo.value.format(ip=network()))
            LOG.info(Console.ServerRunning.value.format(ip=network(), port=80))
    except:
        LOG.error(Console.ServerError.value)

    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    logging.getLogger("waitress.queue").setLevel(logging.ERROR)
    wsgi.server(eventlet.listen((network(), int(Config.read()['core']['port']))), app, log_output=False)