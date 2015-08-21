# Map display on PC
## Dependencies
```
pip install tornado
```

## Running
```
python test2.py
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


## TODO
- Real map
- simulator of sensors
- simlator of map
    - exploration implementation
    - shortest path implementation




get_sensors(LOCATION)
- LOCATION: coordinate of center of robot
- 6 sensors
    + 1: Front left
    + 2: Front mid
    + 3: front right
    + 4: right
    + 5: left
    + 6: left back
- return value example: array of size 6, each cell is an array of 4 values
    + [[1, 1, 1, 1], [1, 2, 0, 0], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]

move_forward()
- FORWARD

rotate(DIRECTION)
- LEFT or RIGHT