from typing import Optional, Tuple, List, Dict
import maze
import runner
import os
import argparse
import sys
import csv

def main():
    #Description
    #-----------------------------------------------
    parser = argparse.ArgumentParser(description="ECS Maze Runner")
    parser.add_argument('maze', nargs="?", default="maze_file.txt", help='The name of the maze file, e.g., maze1.mz')
    parser.add_argument('--starting', metavar='STARTING', help=' The starting position, e.g., "2, 1"')
    parser.add_argument('--goal', help=' The goal position, e.g., "4, 5"')
    #-----------------------------------------------
    
    args = parser.parse_args()

    maze_size = []
    with open(args.maze, "r") as f:
        for line in f.readlines():
            line = line.rstrip("\n")
            maze_size.append(line)
    
    height = (len(maze_size) - 1) // 2  

    width = (len(maze_size[0]) - 1) // 2

    the_maze = maze.create_maze(width, height)

    #Converting argument into tuple format for starting and goal position
    #--------------------------------------
    if args.starting:
        parts = (args.starting).split(',')
        parts_list = []
        for p in parts:
            parts_list.append(int(p.strip()))
        start = tuple(parts_list)
    else:
        start = None

    if args.goal:
        parts = (args.goal).split(',')
        parts_list = []
        for p in parts:
            parts_list.append(int(p.strip()))
        goal = tuple(parts_list)
    else:
        goal = None
    #--------------------------------------

    #Validation Checks
    #----------------------------------------------------   
    if start == None and goal == None:
        pass
    else:
        if len(start) != 2 or len(goal) != 2:
            #ensures coordinates are in correct format
            raise TypeError("The starting/goal position should be two integer")

        width, height = maze.get_dimensions(the_maze)

        #ensures coordinates are within the maze
        if (start[0] >= height or start[1] >= width) or (start[0] < 0 or start[1] < 0):
            raise ValueError("Invalid starting position coordinates")

        if (goal[0] >= height or goal[1] >= width) or (goal[0] < 0 or goal[1] < 0):
            raise ValueError("Invalid goal position coordinates")
    #----------------------------------------------------   

    #File Error Handling
    #----------------------------------------------------
    try:
        with open(args.maze, "r") as f:
            pass
    except FileNotFoundError:
        print(f"Error: The file at {args.maze} was not found.")
    except Exception as e:
        print(f"An error occured: {e}")

    try:
        maze_reading = maze_reader(the_maze, args.maze)
    except IOError:
        print(f"Error: Cannot read maze file")
        return
    except ValueError:
        print(f"Error: Maze file has invalid characters")
        return
    #----------------------------------------------------
    
    path = shortest_path(maze_reading, starting = start, goal = goal, maze_file = args.maze)
    step = exploration_file(path) 
    file = args.maze
    statistics_file(step,path, file)
    print(path)
    
    

def shortest_path(the_maze: List[List[Dict[str,bool]]], starting: Optional[Tuple[int,int]] = None, goal: Optional[Tuple[int,int]] = None, maze_file: str = "") -> List[Tuple[int,int,str]]:
    if starting is None:
        start_x, start_y = len(the_maze)- 1 , 0
    else:
        start_x, start_y = starting

    #^if no optional starting position is given then set to (0,0)

    the_runner = runner.create_runner(start_x, start_y, "N")
    path = runner.dijkstras_algorithm(the_runner, the_maze, goal, maze_file,starting)
    if path:
        del path[-1]
  
    return path

def maze_reader(the_maze: List[List[Dict[str,bool]]], maze_file: str) -> List[List[Dict[str,bool]]]:

    if not os.path.exists(maze_file):
        raise IOError("Maze file not found")

    #put file into 2d array with each index representing an element
    maze_array = []
    with open(maze_file, "r") as f:
        for line in f.readlines():
            line = line.rstrip("\n")
            maze_array.append(list(line))

   
    maze_height = len(the_maze)  #maze dimensions
    maze_width = len(the_maze[0])

    #Loop through everything but exterior walls
    for rows in range(1, (len(maze_array) - 1)):
        for cols in range(1, (len(maze_array[0]) - 1)):

            element = maze_array[rows][cols]

            if element != "." and element != '#':
                raise ValueError("Invalid character in file")

            if maze_array[rows][cols] == '#' and maze_array[rows-1][cols] == '.':
                #^if element is a wall and element above is clear then its a horizontal wall
                cell_x = rows - 1
                cell_y = cols
                if 0 <= cell_x < maze_height and 0 <= cell_y < maze_width:
                    the_maze = maze.add_horizontal_wall(the_maze, cell_y, cell_x)

    
            if maze_array[rows][cols] == '#' and maze_array[rows][cols-1] == '.':
                #^if element is a wall and element to the left is clear then its a vertical wall between these two cells
                cell_x = rows
                cell_y = cols - 1
                if 0 <= cell_x < maze_height and 0 <= cell_y < maze_width:
                    the_maze = maze.add_vertical_wall(the_maze, cell_y, cell_x)

    return the_maze

def exploration_file(path: List[Tuple[int,int,str]]) -> int:
    with open("exploration.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(['Step','x-coordinate','y-coordinate','Actions'])
        step = 1
        for p in path:
            x,y,action = p
            writer.writerow([step,x,y,action])
            step += 1
            
        return step
    
def statistics_file(step: int ,path: List[Tuple[int,int,str]] ,file: str):
    with open("statistics.txt", "w") as f:
        current_file = str(file)
        score = (step / 4) + len(path)
        f.write(f"{current_file}\n{score}\n{step}\n{path}\n{len(path)}\n")
        
    

if __name__ == "__main__":
    main()
                        
      
