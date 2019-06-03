
import tornado.ioloop
import tornado.web
import tornado.options
from tornado.options import define, options
from urls import handlers
from config import settings

define("port", default=8874, help="run on the given port", type=int)


class Application(tornado.web.Application):

    def __init__(self):
        super(Application, self).__init__(handlers, **settings)


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
