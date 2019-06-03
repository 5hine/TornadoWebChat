import os

from handlers.Mainhandler import MainHandler
from handlers.ChatHandler import ChatSocketHandler

handlers = [
    (r"/", MainHandler),
    (r"/chatsocket", ChatSocketHandler),
]
