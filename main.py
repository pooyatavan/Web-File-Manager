import logging, eventlet, sys
from eventlet import wsgi

# no cache files for python
sys.dont_write_bytecode = True

from modules.log import LOG
LOG.logo()

from modules.config import Config
from modules.strings import Console
from modules.tools import network
from modules.flask import app, FlaskAPP

if __name__ == '__main__':
    try:
        FlaskAPP()
    except:
        LOG.error(Console.ServerError.value)
    else:
        LOG.info(Console.NetworkInfo.value.format(ip=network()))
        LOG.info(Console.ServerRunning.value.format(ip=network(), port=80))
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    logging.getLogger("waitress.queue").setLevel(logging.ERROR)
    wsgi.server(eventlet.listen((network(), int(Config.read()['core']['port']))), app, log_output=False)