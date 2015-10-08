import time
import bluetooth
import gevent
import serial
from gevent import socket

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
    print ("Attempting connection to the nexus")
    btaddr = "08:60:6E:A5:89:46" #nexus
    port = 4
    btsock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    btsock.connect((btaddr, ANY_PORT))
    print ("Connected BT")
    return btsock

def btCommListen():
    print ("Listening for incoming BT")
    btsock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    btsock.bind(("", 4))
    btsock.listen(1) #listen for a device
    client_sock, address = btsock.accept()
    print ("Accepted BT connection from %s" %address)    
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

def establishBT():
    attempts = 0
    btsock = 0
    while attempts < 3:
       try:
           btsock = btComm()
           break
       except:
           attempts += 1
    return btsock

def startThreads():
    while btsock == 0 or btThreads == 0:
       if btsock:
          thread2 = gevent.spawn(btWrite, "BTThread-btWrite", 0.5)
          thread3 = gevent.spawn(btRead, "BTThread-btRead", 0.5)
          threads.append(thread2)
          threads.append(thread3)
          gevent.joinall(threads) 

def start():
    while flag == 0:
      btsock = establishBT()
      if btsock == 0:
        btCommListen()
      if btsock:
        flag = 1
        startThreads()
    gevent.sleep(0.5)



#wifisock = wifiComm() 
#btsock = btComm()
#serial = setSerComm()
 
def main():
  while 1:
    try:     
      #if btsock == 0:
      #   btsock = btCommListen()
      #if btsock:
      #  thread1 = gevent.spawn(btWrite, "Thread 1-btWrite", 0.5)
      #  thread2 = gevent.spawn(btRead, "Thread 2-btRead", 0.5)
      #thread3 = gevent.spawn(serWrite, "Thread 3-serWrite", 0.5)
      #thread4 = gevent.spawn(serRead, "Thread 4-serRead", 0.5)
      #thread5 = gevent.spawn(sockWrite, "Thread 5-sockWrite", 0.5)
      #thread6 = gevent.spawn(sockRead, "Thread 6-sockRead", 0.5) 
      #threads = [thread1, thread2]#, #thread3, thread4, thread5, thread6]
        mainthread = gevent.spawn(start)
        if mainthread:
          gevent.joinall(mainthread)
        main_flag = 1
    except:
        for t in threads:
          t.kill(block=False)
        mainthread.kill(block=False)
        print ("Threads cannot start - disconnected")
        mainthread = gevent.spawn(start) #reconnect
        if mainthread:
          gevent.joinall(mainthread)
        
    
    
btq = deque([])
sockq = deque([])
serialq = deque([])
threads = deque([])
btThreads = 0
flag = 0
main_flag = 0


main()
