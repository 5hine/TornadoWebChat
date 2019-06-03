import tornado.web
from .ChatHandler import ChatSocketHandler


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html",
                    messages=ChatSocketHandler.cache,
                    clients=ChatSocketHandler.waiters,
                    username="游客%d" % ChatSocketHandler.client_id)
