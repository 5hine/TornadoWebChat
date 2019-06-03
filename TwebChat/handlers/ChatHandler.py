import logging
from datetime import datetime
import os
import uuid
import tornado.websocket
import tornado.escape


class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    username = ""
    client_id = 0
    cache = []
    cache_size = 200

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        self.client_id = ChatSocketHandler.client_id
        ChatSocketHandler.client_id += 1
        self.username = "游客%d" % self.client_id
        ChatSocketHandler.waiters.add(self)
        chat = {}
        chat.update({
            "id": str(uuid.uuid4()),
            "type": "online",
            # 聊天消息添加用户名ID 昵称、时间
            "client_id": self.client_id,
            "username": self.username,
            "datetime": datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        })
        ChatSocketHandler.send_update(chat)

    def on_close(self):
        ChatSocketHandler.waiters.remove(self)
        chat = {}
        chat.update({
            "id": str(uuid.uuid4()),
            "type": "offline",
            # 聊天消息添加用户名ID 昵称、时间
            "client_id": self.client_id,
            "username": self.username,
            "datetime": datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        })
        ChatSocketHandler.send_update(chat)

    def on_message(self, message):     # message: Union(str, str)
        logging.info("got message %r", message)
        parsed = tornado.escape.json_decode(message)
        self.username = parsed["username"]           #记录用户设置的昵称
        chat = {}
        chat.update({
            "id": str(uuid.uuid4()),
            "body": parsed["body"],
            "type": "message",
            # 聊天消息添加用户名ID 昵称、时间
            "client_id": self.client_id,
            "username": self.username,
            "datetime": datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        })
        chat["html"] = tornado.escape.to_basestring(
                self.render_string("message.html", message=chat))

        ChatSocketHandler.send_update(chat)
        ChatSocketHandler.update_cache(chat)

    @classmethod
    def send_update(cls, chat):
        logging.info("send message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)

    @classmethod
    def update_cache(cls, chat):
        cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]
