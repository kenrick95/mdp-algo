import tornado.ioloop
import tornado.web
import tornado.websocket

import threading
from functools import wraps

def delay(delay=0.):
    """
    Decorator delaying the execution of a function for a while.
    """
    def wrap(f):
        @wraps(f)
        def delayed(*args, **kwargs):
            timer = threading.Timer(delay, f, args=args, kwargs=kwargs)
            timer.start()
        return delayed
    return wrap

from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)

# we gonna store clients in dictionary..
clients = dict()

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        self.id = self.get_argument("Id")
        self.stream.set_nodelay(True)
        clients[self.id] = {"id": self.id, "object": self}

    def on_message(self, message):        
        """
        when we receive some message we want some message handler..
        for this example i will just print message to console
        """
        print ("Client " + str(self.id) + " received a message : " + str(message))
        for key in clients:
            if (clients[key]['id'] != self.id):
                clients[key]['object'].write_message(message)

    def on_close(self):
        if self.id in clients:
            del clients[self.id]

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        #self.write("This is your response")
        self.render("test.html")
        #we don't need self.finish() because self.render() is fallowed by self.finish() inside tornado
        #self.finish()

app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/ws', WebSocketHandler),
])

@delay(10.0)
def x():
    for key in clients:
        print(key)
        clients[key]['object'].write_message("Something")
    print("---------")
    # x()

x()

if __name__ == '__main__':
    parse_command_line()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
