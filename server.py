import tornado.ioloop
import tornado.web
import tornado.websocket

import threading
from functools import wraps
from tornado.options import define, options, parse_command_line

import datetime
import json
import zope.event
import random


from constants import *
import sim
from exploration import Exploration
from shortest_path import ShortestPath

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


define("port", default=8888, help="run on the given port", type=int)

# we gonna store clients in dictionary..
clients = dict()

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        self.id = self.get_argument("Id")
        self.stream.set_nodelay(True)
        clients[self.id] = {"id": self.id, "object": self}
        tick("INIT")

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

class StartHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, delay):
        self.write("Starting...")
        global started
        global delay_time
        if started:
            return
        started = True
        delay_time = float(delay)

        # test()
        exp = Exploration()
        test(exp)


        # After Exploration is done
        # Shortest_path from CURRENT_POSITION to START
        # Shortest_path from START to GOAL

        # sp = ShortestPath(robot.explored_map, NORTH, [18, 1], [1, 13])
        # sp_list = sp.shortest_path()
        # sp_sequence = sp_list['sequence']
        # sp_sequence.reverse()
        # test_sp(sp_sequence)


app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/ws', WebSocketHandler),
    (r'/start/(.+)', StartHandler)
])

def tick(action):
    for key in clients:
        message = dict()
        message['action'] = action
        message['time'] = str(datetime.datetime.utcnow())
        message['map'] = robot.explored_map
        clients[key]['object'].write_message(json.dumps(message))

def translate(action):
    if action == "W":
        return FORWARD
    elif action == "A":
        return LEFT
    elif action == "D":
        return RIGHT

started = False
delay_time = 0.1 # TODO: How to make this variable? (i.e. controllable from the UI?) --> Find a way to redefine decorator

@delay(delay_time)
def test(exp):
    sensors = robot.get_sensors()
    # choice = random.choice([FORWARD, LEFT, RIGHT])
    # robot.action(choice)
    # print(choice, ': ', robot.direction)
    # test()
    cur = exp.getRealTimeMap()
    robot.action(translate(cur[1]))
    sensors = robot.get_sensors()
    if not cur[2]:
        test(exp)

@delay(delay_time)
def test_sp(sequence):
    if len(sequence) == 0:
        print("DONE")
        return False
    choice = sequence.pop()
    robot.action(choice, 9)
    print(choice, ': ', robot.direction)
    test_sp(sequence)

# every 1 s, call Nelson's exploration function --> get sth to print

if __name__ == '__main__':
    parse_command_line()
    app.listen(options.port)
    robot = sim.Robot()
    old_subscribers = zope.event.subscribers[:]
    del zope.event.subscribers[:]
    zope.event.subscribers.append(tick)
    tornado.ioloop.IOLoop.instance().start()
