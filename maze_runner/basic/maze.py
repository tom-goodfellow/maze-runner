from typing import Optional, Tuple, List, Dict


def create_maze(width=5, height=5):

    the_maze = []

    for x in range(height):     #cycle through rows (top to bottom)
        rows = []
        for y in range(width):  #cycle through columns (left to right)
            #North
            if x == 0:          #if x coordinate is on the top row..
                north = False   #cant move north
            else:
                north = True    #otherwise can
            #East
            if y == width - 1:  #if y coordinate is at 4 (rightmost column)..
                east = False    #can't move east
            else:
                east = True     #otherwise can
            #South
            if x == height - 1: #if x coordinate is at bottom row..
                south = False   #cant move south
            else:
                south = True    #otherwise can
            #West
            if y == 0:          #if y coordinate is at 0 (at leftmost column)..
                west = False    #cant move west
            else:
                west = True     #otherwise can

            hor = False
            ver = False
                
            cell = {"x": x, "y" : y, "N": north, "E": east, "S": south, "W": west, "x_wall": hor, "y_wall": ver}

            rows.append(cell)
            
        the_maze.append(rows)

    return the_maze

def add_horizontal_wall(the_maze: List[List[Dict]], x_coordinate: int, horizontal_line: int) -> List[List[Dict]]:
    #Example: adding a horizontal wall at (x,y) places it one above the cell
    cell = the_maze[horizontal_line][x_coordinate] 
    cell["x_wall"] = True
    return the_maze

def add_vertical_wall(the_maze: List[List[Dict]], y_coordinate: int, vertical_line: int) -> List[List[Dict]]:
    #Example: adding a vertical wall at (x,y) places a wall to the left of this cell
    cell = the_maze[y_coordinate][vertical_line] 
    cell["y_wall"] = True
    return the_maze

def get_dimensions(the_maze: List[List[Dict]]) -> Tuple[int,int]:
    height = len(the_maze)      
    width = len(the_maze[0])      
    return (width, height)

def get_walls(the_maze: List[List[Dict]], x_coordinate : int, y_coordinate: int) -> Tuple[bool,bool,bool,bool]:
    cell = the_maze[x_coordinate][y_coordinate]

    north = False
    east = False
    south = False
    west = False
    
    if (cell["x_wall"] == True) or (x_coordinate == 0):
         #if a horizontal wall exists or at the north border then there is a wall in north direction
        north = True
         
    if (y_coordinate == 0) or (the_maze[x_coordinate][y_coordinate - 1]["y_wall"] == True):
        #if at left border or there is a vertical wall to the left of player then there is a wall in west direction
        west = True

    if x_coordinate + 1 < len(the_maze):
    #prevents index error when checking row below
        if (the_maze[x_coordinate + 1][y_coordinate]["x_wall"] == True):
        #if there is a wall in the south direction
            south = True
    else:
        #at the bottom row so exterior south wall exists
        south = True

    if y_coordinate + 1 < len(the_maze[0]):
         if (the_maze[x_coordinate][y_coordinate + 1]["y_wall"] == True):
            east = True
    else:
        east = True
        
    return (north,east,south,west)
        
              
