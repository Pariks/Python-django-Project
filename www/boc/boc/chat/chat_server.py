#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Simplified chat demo for websockets.
Authentication, error handling, etc are left as an exercise for the reader :)
"""

import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import torndb
import os.path
import uuid
import urllib2
import json
from datetime import datetime

from tornado.options import define, options

define("port", default=3000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/chatsocket", ChatSocketHandler),
        ]
        
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
        )

        tornado.web.Application.__init__(self, handlers, **settings)


class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    cache = {'users':[], 'messages':[]}
    cache_size = 10000
    
    if len(cache['messages']) == 0:
        db = torndb.Connection("localhost", "boc", user="root", password='Unfightable7!')
        for db_message in db.query("SELECT * FROM chat_chatmessage LEFT JOIN auth_user on chat_chatmessage.user_id = auth_user.id ORDER BY timestamp"):
            message = {
                "id": str(db_message.id),
                "body": db_message.text,
                "username": db_message.username,
                "timestamp": db_message.timestamp.isoformat()
                }
            
            
            cache['messages'].insert(len(cache['messages']), message)
    
    def check_origin(self, origin):
        return True

    def allow_draft76(self):
        # for iOS 5.0 Safari
        return True

    def open(self):
        user = self.get_user()
        if user:
            self.user = self.get_user()
        ChatSocketHandler.waiters.add(self)

    def on_close(self):
        try:
            self.cache['users'].remove(self.user)
            self.cache['users'].sort()
            self.update_users()
            ChatSocketHandler.waiters.remove(self)
        except:
            ChatSocketHandler.waiters.remove(self)
            
        
    def get_user(self):
        #get session key
        cookies = self.request.headers['Cookie'].split('; ')
        sessionid = None
        for cookie in cookies:
            if "sessionid" in cookie:
                sessionid = cookie.split("=")[1]
        if sessionid:
        #post request to server
            url = self.request.headers["Origin"]+"/chat/auth/"
            req = urllib2.Request(url)
            response = urllib2.urlopen(req, "sessionid="+sessionid)
            result = response.read()
            result = json.loads(result)
            return result['user']
        return None
        
    @classmethod
    def update_message_cache(cls, chat):
        cls.cache['messages'].append(chat)
        if len(cls.cache['messages']) > cls.cache_size:
            cls.cache['messages'] = cls.cache['messages'][cls.cache_size:]
              

    @classmethod
    def send_updates(cls, chat):
        logging.info("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)
    
   
    def update_users(self):
        users = {"type": "users"}
        users['users'] = ChatSocketHandler.cache['users']
        for waiter in self.waiters:
            try:
                waiter.write_message(users)
            except:
                pass
                

    def on_message(self, message):
        logging.info("got message %r", message)
        parsed = tornado.escape.json_decode(message)
        if parsed['type'] == "auth":
            #update users
            if parsed['user'] not in self.cache['users']:
                self.cache['users'].append(parsed['user'])
                self.cache['users'].sort()
            ChatSocketHandler.update_users(self)
            
            #return messages
            chat = {}
            chat["messages"] =  ChatSocketHandler.cache['messages']
            chat["type"] = "auth"
            ChatSocketHandler.send_updates(chat)
            
        elif parsed['type'] == "message":
            #get session key
            user = self.get_user()
            
            message = {
                "id": str(uuid.uuid4()),
                "body": parsed["body"],
                "username": user['username'],
                "timestamp": datetime.now().isoformat()
                }
            
            chat = {"type": 'message', "messages": [message]}

            ChatSocketHandler.update_message_cache(message)
            ChatSocketHandler.send_updates(chat)
            

def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
