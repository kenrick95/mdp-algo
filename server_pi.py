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

import time
import bluetooth
import gevent
import serial
from gevent import socket
from gevent.event import Event

from collections import deque


from algo.constants import *
import algo.real
from algo.exploration import Exploration
from algo.shortest_path import ShortestPath

clients = dict()
started = False
delay_time = 0
evt = Event()

define("port", default=8888, help="run on the given port", type=int)

def delay_call(f, *args, **kwargs):
    evt.wait()
    global delay_time
    t = threading.Timer(delay_time, f, args=args, kwargs=kwargs)
    t.start()

class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
 
    def run(self):
        self._target(*self._args)



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
        self.render("display.html")
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

        exp = Exploration(int(percentage))


        t1 = FuncThread(exploration, exp)
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

def do_alignment(actions):
    global started
    if not started:
        return False
    if len(actions) > 0:
        choice = actions[0]
        actions = actions[1:]
        send_cmd(choice)
        gevent.joinall([
            gevent.spawn(delay_call, do_alignment, actions)
        ])


def exploration(exp):
    global started
    if not started:
        return False
    
    do_alignment(robot.alignment())

    global sensors
    cur = exp.getRealTimeMap(sensors)
    if not cur[1]:
        robot.action(cur[0])
        send_cmd(cur[0])

        print(robot.current)

        # delay_call(exploration, exp)
        gevent.joinall([
            gevent.spawn(delay_call, exploration, exp)
        ])
    else:
        inform("Exploration done!")
        
        inform(robot.descriptor_one())
        inform(robot.descriptor_two())


        sp = ShortestPath(robot.explored_map, robot.direction, robot.current, robot.start)
        sp_list = sp.shortest_path(-1)
        sp_sequence = sp_list['trim_seq']
        sp_sequence.reverse()
        inform(sp_sequence)
        
        # call sp to start
        # delay_call(sp_to_start, sp_sequence)
        gevent.joinall([
            gevent.spawn(sp_to_start, sp_sequence)
        ])

# @delay(delay_time)
def sp_to_start(sequence):
    global started
    if not started:
        return False
    if len(sequence) == 0:
        inform("Gone back to start!")

        sp = ShortestPath(robot.explored_map, robot.direction, robot.current, robot.goal)
        sp_list = sp.shortest_path()
        sp_sequence = sp_list['trim_seq']
        sp_sequence.reverse()
        inform(sp_sequence)
        # delay_call(sp_to_goal, sp_sequence)
        gevent.joinall([
            gevent.spawn(sp_to_goal, sp_sequence)
        ])

        return False
    
    do_alignment(robot.alignment())

    choice = sequence.pop()
    robot.action(choice, -1)
    send_cmd(choice)

    print(choice, ': ', robot.direction)
    # delay_call(sp_to_start, sequence)
    gevent.joinall([
        gevent.spawn(sp_to_start, sp_sequence)
    ])


# @delay(delay_time)
def sp_to_goal(sequence):
    global started
    if not started:
        return False
    if len(sequence) == 0:
        inform("ShortestPath done!")
        started = False
        return False
    

    do_alignment(robot.alignment())

    choice = sequence.pop()
    robot.action(choice, 9)
    send_cmd(choice)
    
    print(choice, ': ', robot.direction)
    # delay_call(sp_to_goal, sequence)
    gevent.joinall([
        gevent.spawn(sp_to_goal, sp_sequence)
    ])


def wifiComm():
    host = "192.168.5.10"
    port = 5143
    wifisoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    wifisoc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
#    wifisoc.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
#    wifisoc.bind((host, port))
#    wifisoc.listen(5)
#    conn, address = wifisoc.accept()
#    return wifisoc, address
    wifisoc.connect((host, port))
    return wifisoc

def btComm():
#    btaddr = "00:E3:B2:A1:8F:65" #note3
    btaddr = "08:60:6E:A5:89:46" #nexus
    port = 4
    btsock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    btsock.connect((btaddr, port))
    print ("Connected BT")
    return btsock

def setSerComm():
    sersock = serial.Serial('/dev/ttyACM0', 9600) # Establish the connection wi$
    return sersock


def btWrite(threadName, delay):
    stop_flag = 0
#    gevent.sleep(delay)
    while stop_flag == 0:
        gevent.sleep(delay)
        #time.sleep(delay)
        if len(btq) > 0:
            msg = btq.popleft()
            btsock.send(msg)
            print ("%s send msg: %s @ %s" %(threadName, msg, time.ctime(time.time())))

def btRead(threadName, delay):
    stop_flag = 0
    while stop_flag == 0:
        gevent.sleep(delay)
#        time.sleep(delay)
        msg = btsock.recv(1024)
        print ("%s received msg: %s @ %s" %(threadName, msg, time.ctime(time.time()))   )
        serialq.append(msg)
       

def serRead(threadName, delay):
    while 1:
        gevent.sleep(delay)
        msg = serial.readline()
        #sockq.append(msg)
        # received "msg" from Arduino
        parse_msg(msg)

        print ("%s received msg: %s @ %s" %(threadName, msg, time.ctime(time.time()))  )

def serWrite(threadName, delay):
    while 1:
        gevent.sleep(delay)
        if len(serialq) > 0:
            msg = serialq.popleft()
            serial.write(msg)
            print ("%s send msg: %s @ %s" %(threadName, msg, time.ctime(time.time())))


def sockRead(threadName, delay):
    while 1:
        gevent.sleep(delay)
        msg  = wifisock.recv(1024)
        print ("%s received msg: %s @ %s" %(threadName, msg, time.ctime(time.time())))
         
def sockWrite(threadName, delay):
    while 1:
        gevent.sleep(delay)
        if len(sockq) > 0:
            msg = sockq.popleft()
            wifisock.send(msg)
            print ("%s send msg: %s @ %s" %(threadName, msg, time.ctime(time.time())))


def writeInput():
    while 1:
        gevent.sleep(1)
        test = raw_input("Enter Command: ")
        btq.append(test)

def send_cmd(cmd):
    serialq.append(cmd)
    evt.clear()

def parse_msg(msg):
    print(msg)
    if (msg == "K"):
        # alignment acknowledgemnet
        None
    else:
        sensorString = msg
        robot.parse_sensors(sensorString)
        robot.update_map()
    evt.set()
    return

if __name__ == '__main__':
    parse_command_line()
    app.listen(options.port)
    robot = algo.real.Robot()
    old_subscribers = zope.event.subscribers[:]
    del zope.event.subscribers[:]
    zope.event.subscribers.append(tick)


    # wifisock = wifiComm() 
    #btsock = btComm()
    #server = Server('', 5143)
    #asyncore.loop(timeout=1)
    serial = setSerComm()

    #btq = deque([])
    #sockq = deque([])
    serialq = deque([])

    try:
    #    thread.start_new_thread(btWrite, ("Thread 1-btWrite", 0.5))
    #    thread.start_new_thread(btRead, ("Thread 2-btRead", 0.5))
    #    thread1 = gevent.spawn(btWrite, "Thread 1-btWrite", 0.5)
    #    thread2 = gevent.spawn(btRead, "Thread 2-btRead", 0.5)
    #    thread3 = gevent.spawn(sockWrite, "Thread 3-sockWrite", 0.5)
    #    thread4 = gevent.spawn(sockRead, "Thread 4-sockRead", 0.5)
        thread3 = gevent.spawn(serWrite, "Thread 5-serWrite", 0.5)
        thread4 = gevent.spawn(serRead, "Thread 6-serRead", 0.5)
    #    thread5 = gevent.spawn(sockWrite, "Thread 3-sockWrite", 0.5)
    #    thread6 = gevent.spawn(sockRead, "Thread 4-sockRead", 0.5) 
    #    thread3 = gevent.spawn(writeInput)
    #    threads = [thread1, thread2, thread3, thread4]
        threads = [thread3, thread4]
        gevent.joinall(threads)
    except:
        print ("Error, cannot create threads.")

    print("Listening to http://localhost:" + str(options.port) + "...")
    tornado.ioloop.IOLoop.instance().start()
