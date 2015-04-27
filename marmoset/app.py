from . import config, webserver

app = webserver.app(config.load())

