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

class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
 
    def run(self):
        self._target(*self._args)

def delay_call(f, *args, **kwargs):
    global delay_time
    t = threading.Timer(delay_time, f, args=args, kwargs=kwargs)
    t.start()

define("port", default=8888, help="run on the given port", type=int)

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
        #for key in clients:
        #    if (clients[key]['id'] != self.id):
        #        clients[key]['object'].write_message(message)

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
    def get(self, percentage, delay):
        self.write("Starting...")
        global robot

        global started
        global delay_time
        if started:
            return
        started = True
        robot = sim.Robot()

        delay_time = float(delay)

        # test()
        exp = Exploration(int(percentage))
        # test(exp)
        t1 = FuncThread(test, exp)
        t1.start()
        t1.join()
        inform("Exploration started!")
        self.flush()


class StopHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, delay):
        global started
        inform("Exploration stopped!")
        started = False
        self.flush()


app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/ws', WebSocketHandler),
    (r'/start/(.*)/(.*)', StartHandler),
    (r'/stop/(.*)', StopHandler)
])

def tick(action):
    for key in clients:
        message = dict()
        message['type'] = 'map'
        message['action'] = action
        message['time'] = str(datetime.datetime.utcnow())
        message['map'] = robot.explored_map
        clients[key]['object'].write_message(json.dumps(message))


def inform(string):
    print(string)
    for key in clients:
        message = dict()
        message['type'] = 'info'
        message['time'] = str(datetime.datetime.utcnow())
        message['info'] = string
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

def test(exp):
    global started
    if not started:
        return False
    sensors = robot.get_sensors()
    cur = exp.getRealTimeMap(sensors)
    if not cur[2]:
        robot.action(translate(cur[1]))
        print(robot.current)
        sensors = robot.get_sensors()
        delay_call(test, exp)
    else:
        inform("EXPLORATION DONE")
        
        inform(robot.descriptor_one())
        inform(robot.descriptor_two())


        sp = ShortestPath(robot.explored_map, robot.direction, robot.current, robot.start)
        sp_list = sp.shortest_path(-1)
        sp_sequence = sp_list['sequence']
        sp_sequence.reverse()
        inform(sp_sequence)
        
        # call sp to start
        delay_call(test_sp, sp_sequence)

# @delay(delay_time)
def test_sp(sequence):
    global started
    if not started:
        return False
    if len(sequence) == 0:
        inform("GONE BACK TO START")

        sp = ShortestPath(robot.explored_map, robot.direction, robot.current, robot.goal)
        sp_list = sp.shortest_path()
        sp_sequence = sp_list['sequence']
        sp_sequence.reverse()
        inform(sp_sequence)
        delay_call(test_sp_to_goal, sp_sequence)

        return False
    choice = sequence.pop()
    robot.action(choice, -1)
    print(choice, ': ', robot.direction)
    delay_call(test_sp, sequence)


# @delay(delay_time)
def test_sp_to_goal(sequence):
    global started
    if not started:
        return False
    if len(sequence) == 0:
        inform("SHORTEST PATH DONE")
        started = False
        return False
    choice = sequence.pop()
    robot.action(choice, 9)
    print(choice, ': ', robot.direction)
    delay_call(test_sp_to_goal, sequence)

if __name__ == '__main__':
    parse_command_line()
    app.listen(options.port)
    robot = sim.Robot()
    old_subscribers = zope.event.subscribers[:]
    del zope.event.subscribers[:]
    zope.event.subscribers.append(tick)
    tornado.ioloop.IOLoop.instance().start()
