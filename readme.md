# The One Program to Rule Them All!
## Dependencies
```
pip install tornado
pip install zope.event
pip install gevent
pip install gevent.event
```
- Raspberry Pi
- Bluetooth (`bluetooth`)
- Arduino (`serial`)

## Running at RPi
```
python server_pi.py
```
and then open browser and navigate to `192.168.5.5:8888`



# Simulator
## Dependencies
```
pip install tornado
pip install zope.event
```

## Running
```
python server.py
```
and then open browser and navigate to `localhost:8888`

## Stopping
Ctrl + Pause/break.

## Definitions
- 0: unexplored
- 1: explored
- 2: obstacle
- 3: robot body
- 4: robot head
- 5: robot center
- 6: start
- 7: goal
- 8: explored path
- 9: optimum path