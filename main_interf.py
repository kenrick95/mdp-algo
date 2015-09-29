import time
import bluetooth
import gevent
import serial
from gevent import socket

#from gevent import monkey, sleep
#monkey.patch_all()

from collections import deque

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
        sockq.append(msg)
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


wifisock = wifiComm() 
btsock = btComm()
#server = Server('', 5143)
#asyncore.loop(timeout=1)
serial = setSerComm()

btq = deque([])
sockq = deque([])
serialq = deque([])

try:
#    thread.start_new_thread(btWrite, ("Thread 1-btWrite", 0.5))
#    thread.start_new_thread(btRead, ("Thread 2-btRead", 0.5))
    thread1 = gevent.spawn(btWrite, "Thread 1-btWrite", 0.5)
    thread2 = gevent.spawn(btRead, "Thread 2-btRead", 0.5)
#    thread3 = gevent.spawn(sockWrite, "Thread 3-sockWrite", 0.5)
#    thread4 = gevent.spawn(sockRead, "Thread 4-sockRead", 0.5)
    thread3 = gevent.spawn(serWrite, "Thread 5-serWrite", 0.5)
    thread4 = gevent.spawn(serRead, "Thread 6-serRead", 0.5)
    thread5 = gevent.spawn(sockWrite, "Thread 3-sockWrite", 0.5)
    thread6 = gevent.spawn(sockRead, "Thread 4-sockRead", 0.5) 
#    thread3 = gevent.spawn(writeInput)
    threads = [thread1, thread2, thread3, thread4, thread5, thread6]
    gevent.joinall(threads)
except:
    print ("Error, cannot create threads.")

#while 1:
#    test = raw_input("Enter Command: ")
#    btq.append(test)
