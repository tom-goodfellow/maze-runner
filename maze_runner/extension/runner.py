from typing import Optional, Tuple, List, Dict
import maze
import heapq

def create_runner(x: int = 0, y: int = 0, orientation: str = "N") -> Dict[str, int | str]:
    return {"x": x, "y": y, "orientation": orientation}

def get_x(runner: Dict[str, int | str]) -> int:
    return runner['x']

def get_y(runner: Dict[str, int | str]) -> int:
    return runner['y']

def get_orientation(runner: Dict[str, int | str]) -> str:
    return runner['orientation']

def turn(runner: Dict[str, int | str], direction: str) -> Dict[str, int | str]:
    
    #Turn based on intial orientation and direction passed
    #Example: If runner if facing North and direction passed is Right then the runner will face East.
    
    facing = runner['orientation']
    if facing == "N":
        if direction == "Left":
            runner['orientation'] = "W"
        if direction == "Right":
            runner['orientation'] = "E"
    elif facing == "E":
        if direction == "Left":
            runner['orientation'] = "N"
        if direction == "Right":
            runner['orientation'] = "S"
    elif facing == "S":
        if direction == "Left":
            runner['orientation'] = "E"
        if direction == "Right":
            runner['orientation'] = "W"
    elif facing == "W":
        if direction == "Left":
            runner['orientation'] = "S"
        if direction == "Right":
            runner['orientation'] = "N"
    return runner 

def forward(runner: Dict[str, int | str], the_maze: List[List[Dict[str, bool]]]) -> Dict[str, int | str]:

    #Move foward (on the conditions that there are no walls)
    #Example: Runner is at position (1,0), facing East. Granted there are no walls and the next move won't take the runner out of maze boundaries, the runner will move to (1,1)
    
    facing = runner['orientation']
    x = runner['x']
    y = runner['y']

    north, east, south, west = maze.get_walls(the_maze, x, y) #Get walls as bool values

    if facing == "N" and not north and x - 1 >= 0: #If facing north and north is False (no wall ahead) and moving upward a row will not go above index 0 then:
        x -= 1 #decrement x, move upward (x is row)
    elif facing == "S" and not south and x + 1 < len(the_maze):
        x += 1
    elif facing == "E" and not east and y + 1 < len(the_maze[0]):
        y += 1
    elif facing == "W" and not west and y - 1 >= 0:
        y -= 1

    runner['x'] = x
    runner['y'] = y
    return runner

def sense_walls(runner: Dict[str, int | str], the_maze: List[List[Dict[str, bool]]]) -> Tuple[bool, bool, bool]:
    left  = False
    front = False
    right = False
    
    x_coordinate = get_x(runner)
    y_coordinate = get_y(runner)
    orientation = get_orientation(runner)
    north, east, south, west = maze.get_walls(the_maze, x_coordinate, y_coordinate)

    # Sense Walls Logic
    #--------------------------------------
    if orientation == "N": 
        if west: #West is true under the conditions that there is vertical wall to the left of the player
            left = True #If so, player cant turn left and so a wall has been sensed, left returns as True
        if north:
            front = True
        if east:
            right = True
    elif orientation == "E":
        if north:
            left = True
        if east:
            front = True
        if south:
            right = True
    elif orientation == "S":
        if east:
            left = True
        if south:
            front = True
        if west:
            right = True
    elif orientation == "W":
        if south:
            left = True
        if west:
            front = True
        if north:
            right = True
    #--------------------------------------
            
    return (left, front, right)

def go_straight(runner: Dict[str, int | str], the_maze: List[List[Dict[str, bool]]]) -> Dict[str, int | str]:

    # A function to go straight, raises a Value Error if the path is blocked by a wall

    left, front, right = sense_walls(runner, the_maze)
    if front:
        raise ValueError("Cannot go straight due to wall ahead")
    return forward(runner, the_maze)

def move(runner: Dict[str, int | str], the_maze: List[List[Dict[str, bool]]], visited: set[Tuple[int,int]], maze_file: str) -> Tuple[Dict[str, int | str], str]:

        
   



    
    #Main function used to move, utilises awareness of wall locations and a list that keeps track of previous locations to prevent getting stuck in a loop

    left, front, right = sense_walls(runner, the_maze)
    
    left_move = future_move(runner, "Left", the_maze)
    front_move = future_move(runner, "Forward", the_maze)
    right_move = future_move(runner, "Right", the_maze)
    back_move = future_move(runner, "Back", the_maze)

    #^above variables store future moves of the runner
    #Example: Runner is facing North, right_move assumes runner will move right and so will return coordinates of the result ( (3,4) -> (4,4))


    if not left and left_move not in visited: #if left is False (no wall) and the future left move hasnt been done then...
        runner = turn(runner, "Left") #turn left and move foward
        runner = forward(runner, the_maze)
        return runner, "LF"
    elif not front and front_move not in visited:
        runner = forward(runner, the_maze)
        return runner, "F"
    elif not right and right_move not in visited:
        runner = turn(runner, "Right")
        runner = forward(runner, the_maze)
        return runner, "RF"
    else:  #if every path is blocked, turn back
        runner = turn(runner, "Left")
        runner = turn(runner, "Left")
        runner = forward(runner, the_maze)
        return runner, "B"

def future_move(runner: Dict[str, int | str], direction: str, the_maze: List[List[Dict[str, bool]]]) -> Tuple[int,int]:
    x = get_x(runner)
    y = get_y(runner)
    orientation = get_orientation(runner)

    north, east, south, west = maze.get_walls(the_maze, x, y)

    if orientation == "N": #If runner is facing north
        if direction == "Forward" and not north: #If intended direction to go is foward and there is no wall
            return (x-1, y) #return future move
        elif direction == "Left" and not west:
            return (x, y-1)
        elif direction == "Right" and not east:
            return (x, y+1)
        elif direction == "Back" and not south:
            return (x+1, y)
    elif orientation == "E":
        if direction == "Forward" and not east:
            return (x, y+1)
        elif direction == "Left" and not north:
            return (x-1, y)
        elif direction == "Right" and not south:
            return (x+1, y)
        elif direction == "Back" and not west:
            return (x, y-1)
    elif orientation == "S":
        if direction == "Forward" and not south:
            return (x+1, y)
        elif direction == "Left" and not east:
            return (x, y+1)
        elif direction == "Right" and not west:
            return (x, y-1)
        elif direction == "Back" and not north:
            return (x-1, y)
    elif orientation == "W":
        if direction == "Forward" and not west:
            return (x, y-1)
        elif direction == "Left" and not south:
            return (x+1, y)
        elif direction == "Right" and not north:
            return (x-1, y)
        elif direction == "Back" and not east:
            return (x, y+1)
    return (x, y)

def dijkstras_algorithm(runner: Dict[str, int | str], the_maze: List[List[Dict[str,bool]]], goal: Optional[Tuple[int,int]], maze_file: str, starting: Optional[Tuple[int,int]]) -> List[Tuple[int,int,str]]:
    if goal is None:
        goal_x = 0
        goal_y = len(the_maze[0]) - 1  
        goal = (goal_x, goal_y)

    #^If no optional goal is given then goal is top right corner
        
    maze_array = []

    with open(maze_file, "r") as f:
        for line in f.readlines():
            line = line.rstrip("\n")
            maze_array.append(list(line))

    maze_height = len(the_maze)  #maze dimensions
    maze_width = len(the_maze[0])

    nodes = {}

    #Loop through everything but exterior walls
    for x in range(maze_height):
        for y in range(maze_width):
            north, east, south, west = maze.get_walls(the_maze, x, y)
            neighbours = {}
            
            if not north and x - 1 >= 0: #checks for walls or potential to be out of maze boundaries
                neighbours[(x-1, y)] = 1  #create neighbour node, {node:weight}
            if not east and y + 1 < maze_width:
                neighbours[(x, y+1)] = 1
            if not south and x + 1 < maze_height:
                neighbours[(x+1, y)] = 1
            if not west and y - 1 >= 0:
                neighbours[(x, y-1)] = 1

            nodes[(x, y)] = neighbours

    distances = {node: float('inf') for node in nodes} #set inital distances as infinite
    if starting == None:
        starting_node = (0,0)
    else:
        starting_node = starting
        
    distances[starting_node] = 0
    pq = [(0, starting_node)]
    previous = {}

    #Finding Shortest Path Logic
    #---------------------------------------------
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)

        #if a shorter path has been found then skip
        if current_distance > distances[current_node]:
            continue

        #explore each nodes neighbours
        for neighbour, weight in nodes[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbour]:
                distances[neighbour] = distance
                heapq.heappush(pq, (distance, neighbour))
                previous[neighbour] = current_node

    
    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = previous.get(current)

    path.reverse()

    #Add the action for each path:
    for i in range(len(path)-1):    
        x1,y1 = path[i]     #look at intial path and one after
        x2,y2 = path[i+1]
        if x1 + 1 == x2:    #Decide action based on move of coordinates
            path[i] = (x1,y1,"B")
        elif y1 - 1 == y2:
            path[i] = (x1,y1,"LF")
        elif x1 - 1 == x2:
            path[i] = (x1,y1, "F")
        elif y1 + 1 == y2:
            path[i] = (x1,y1, "RF")
        
   
    return path 
    
    #---------------------------------------------
