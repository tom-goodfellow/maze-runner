# maze-runner
A Python maze runner project implementing maze creation, wall detection, runner movement, exploration, and pathfinding.

The maze runner is a python project that reads a maze from a text file and converts it into a usuable maze structure that it proceeds to navigate through via a reactive wall-rebound exploration algorithm. The extension includes the use of Dijkstra's algorithm for shortest-path calculation

**How To Run**

Open terminal and in the project directory run the following:

python maze_runner.py **maze**

<img width="631" height="278" alt="image" src="https://github.com/user-attachments/assets/ec2fb7b4-891b-4825-98c6-b0d6bb7d5871" />

_To display: python maze_runner.py --help_

Optional arguments including custom starting positions and goal positions are available 

_python maze_runner.py maze1.mz --starting "2, 1" --goal "4, 5"_

The maze uses `(x, y)` coordinates, with `x` representing the horizontal position and `y` representing the vertical position. `(0, 0)` represents the top-left cell.

The maze is internally stored using `maze[y][x]`.

**Movement**

The runner uses a reactive wall-rebound algorithm, checking the walls around its current position and moving through available directions while keeping track of visited positions.

The runner can move North, East, South, or West depending on its current orientation.

**Pathfinding**

The extension includes Dijkstra's algorithm to calculate the shortest path between the starting position and goal.

**Maze & Exploration Files**

The project includes `.mz` maze files which contain the maze layouts used as input.

An `exploration.csv` file is also included, containing information about the exploration such as the maze used, score, number of steps, path, and path length. This can be opened using Excel or other spreadsheet software.

