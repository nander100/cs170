# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to University of California, Riverside and the authors.
# 
# Authors: Pei Xu (peixu@stanford.edu) and Ioannis Karamouzas (ioannis@cs.ucr.edu)
#


"""
 In this assignment, the task is to implement different search algorithms to find 
 a path from a given start cell to the goal cell in a 2D grid map.

 To complete the assignment, you must finish four functions:
   depth_first_search (line 148), breadth_first_search (line 232), 
   uniform_cost_search (line 280), and astar_search (line 327).

 During the search, a cell is represented using a tuple of its location
 coordinates.
 For example:
   the cell at the left-top corner is (0, 0);
   the cell at the first row and second column is (0, 1);
   the cell at the second row and first column is (1, 0).
 You need put these tuples into the open set or/and closed set properly
 during searching.
"""

# ACTIONS defines how to reach an adjacent cell from a given cell
# Important: please check that a cell within the bounds of the grid
# when try to access it.
ACTIONS = (
    (-1,  0), # go up
    ( 0, -1), # go left
    ( 1,  0), # go down
    ( 0,  1)  # go right
)

from utils.search_app import OrderedSet, Stack, Queue, PriorityQueue
"""
 Four different structures are provided as the containers of the open set
 and closed set.

 OrderedSet is an ordered collections of unique elements.

 Stack is an LIFO container whose `pop()` method always pops out the last
 added element. 

 Queue is an FIFO container whose `pop()` method always pops out the first
 added element.

 PriorityQueue is a key-value container whose `pop()` method always pops out
 the element whose value has the highest priority.

 All of these containers are iterable but not all of them are ordered. Use
 their pop() methods to ensure elements are popped out as expected.


 Common operations of OrderedSet, Stack, Queue, PriorityQueue
   len(s): number of elements in the container s
   x in s: test x for membership in s
   x not in s: text x for non-membership in s
   s.clear(): clear s
   s.remove(x): remove the element x from the set s;
                nothing will be done if x is not in s


 Unique operations of OrderedSet:
   s.add(x): add the element x to the set s;
             nothing will be done if x is already in s
   s.pop(): return and remove the LAST added element in s;
            raise IndexError if s is empty 
   s.pop(last=False): return and remove the FIRST added element in s;
            raise IndexError if s is empty 
 Example:
   s = Set()
   s.add((1,2))    # add a tuple element (1,2) to the set
   s.remove((1,2)) # remove the tuple element (1,2) from the set
   s.add((1,1))
   s.add((2,2))
   s.add((3,3))
   x = s.pop()
   assert(x == (3,3))
   assert((1,1) in s and (2,2) in s)
   assert((3,3) not in s)
   x = s.pop(last=False)
   assert(x == (1,1))
   assert((2,2) in s)
   assert((1,1) not in s)
   

 Unique operations of Stack:
   s.add(x): add the element x to the back of the stack s
   s.pop(): return and remove the LAST added element in the stack s;
            raise IndexError if s is empty
 Example:
   s = Stack()
   s.add((1,1))
   s.add((2,2))
   x = s.pop()
   assert(x == (2,2))
   assert((1,1) in s)
   assert((2,2) not in s)


 Unique operations of Queue:
   s.add(x): add the element x to the back of the queue s
   s.pop(): return and remove the FIRST added element in the queue s;
            raise IndexError if s is empty
 Example:
   s = Queue()
   s.add((1,1))
   s.add((2,2))
   x = s.pop()
   assert(x == (1,1))
   assert((2,2) in s)
   assert((1,1) not in s)


 Unique operations of PriorityQueue:
   PriorityQueue(order="min", f=lambda v: v): build up a priority queue
       using the function f to compute the priority based on the value
       of an element
   s.put(x, v): add the element x with value v to the queue
                update the value of x if x is already in the queue
   s.get(x): get the value of the element x
            raise KeyError if x is not in s
   s.pop(): return and remove the element with highest priority in s;
            raise IndexError if s is empty
            if order is "min", the element with minimum f(v) will be popped;
            if order is "max", the element with maximum f(v) will be popped.
 Example:
   s = PriorityQueue(order="max", f=lambda v: abs(v))
   s.put((1,1), -1)
   s.put((2,2), -20)
   s.put((3,3), 10)
   x, v = s.pop()  # the element with maximum value of abs(v) will be popped
   assert(x == (2,2) and v == -20)
   assert(x not in s)
   assert(x.get((1,1)) == -1)
   assert(x.get((3,3)) == 10)
"""


# use math library if needed
import math

def depth_first_search(grid_size, start, goal, obstacles, costFn, logger):
    """
    DFS algorithm finds the path from the start cell to the
    goal cell in the 2D grid world.

    After expanding a node, to retrieve the cost of a child node at location (x,y), 
    please call costFn((x,y)). 
    
    Parameters
    ----------
    grid_size: tuple, (n_rows, n_cols)
        (number of rows of the grid, number of cols of the grid)
    start: tuple, (row, col)
        location of the start cell;
        row and col are counted from 0, i.e. the 1st row is 0
    goal: tuple, (row, col)
        location of the goal cell
    obstacles: tuple, ((row, col), (row, col), ...)
        locations of obstacles in the grid
        the cells where obstacles are located are not allowed to access 
    costFn: a function that returns the cost of landing to a cell (x,y)
         after taking an action. 
    logger: a logger to visualize the search process.
         Do not do anything to it.

   
    Returns
    -------
    movement along the path from the start to goal cell: list of actions
        The first returned value is the movement list found by the search
        algorithm from the start cell to the end cell.
        The movement list should be a list object composed of actions
        that should move the agent from the start to goal cell along the path
        as found by the algorithm.
        For example, if nodes in the path from the start to end cell are:
            (0, 0) (start) -> (0, 1) -> (1, 1) -> (1, 0) (goal)
        then, the returned movement list should be
            [(0,1), (1,0), (0, -1)]
        which means: move right, down, left.

        Return an EMPTY list if the search algorithm fails finding any
        available path.
        
    closed_set: list of location tuple (row, col)
        The second returned value is the closed set, namely, the cells are expanded during search.   
    """
    n_rows, n_cols = grid_size
    start_row, start_col = start
    goal_row, goal_col = goal

    ##########################################
    # Choose a proper container yourself from
    # OrderedSet, Stack, Queue, PriorityQueue
    # for the open set and closed set.
    open_set = Stack()
    closed_set = OrderedSet()
    ##########################################

    ##########################################
    # Set up visualization logger hook
    # Please do not modify these four lines
    closed_set.logger = logger
    logger.closed_set = closed_set
    open_set.logger = logger
    logger.open_set = open_set
    ##########################################

    parent = [ # the immediate predecessor cell from which to reach a cell
        [None for __ in range(n_cols)] for _ in range(n_rows)
    ]
    actions = [ # the action that the parent took to reach the cell
        [None for __ in range(n_cols)] for _ in range(n_rows)
    ]
   
    movement = []
    # ----------------------------------------
    # finish the code below
    # ----------------------------------------
#############################################################################
    # start is defined in parameters
    open_set.add(start) # add the first node to the stack
    while len(open_set) > 0: # while there are still nodes in the stack
        # pop the last node in the stack
        current = open_set.pop()
        closed_set.add(current)
        # check if the current node is the goal
        if current == goal:
            # reconstruct the path
            while parent[current[0]][current[1]] is not None:
                movement.append(actions[current[0]][current[1]])
                current = parent[current[0]][current[1]]
            movement.reverse()
            return movement, closed_set
        # check all the neighbors of the current node
        for action in ACTIONS:
            # get the neighbor node
            neighbor = (current[0] + action[0], current[1] + action[1])
            # check if the neighbor is within the bounds of the grid
            if neighbor[0] < 0 or neighbor[0] >= n_rows or neighbor[1] < 0 or neighbor[1] >= n_cols:
                continue
            # check if the neighbor is an obstacle
            if neighbor in obstacles:
                continue
            # check if the neighbor is already in the closed set
            if neighbor in closed_set:
                continue
            # check if the neighbor is already in the open set
            if neighbor not in open_set:
                open_set.add(neighbor)
                parent[neighbor[0]][neighbor[1]] = current
                actions[neighbor[0]][neighbor[1]] = action
            # check if the neighbor is already in the open set
#############################################################################
    return movement, closed_set

def breadth_first_search(grid_size, start, goal, obstacles, costFn, logger):
    """
    BFS algorithm finds the path from the start cell to the
    goal cell in the 2D grid world.
    
    After expanding a node, to retrieve the cost of a child node at location (x,y), 
    please call costFn((x,y)). 

    See depth_first_search() for details.
    """
    n_rows, n_cols = grid_size
    start_row, start_col = start
    goal_row, goal_col = goal

    ##########################################
    # Choose a proper container yourself from
    # OrderedSet, Stack, Queue, PriorityQueue
    # for the open set and closed set.
    open_set = Queue()
    closed_set = OrderedSet()
    ##########################################

    ##########################################
    # Set up visualization logger hook
    # Please do not modify these four lines
    closed_set.logger = logger
    logger.closed_set = closed_set
    open_set.logger = logger
    logger.open_set = open_set
    ##########################################

    parent = [ # the immediate predecessor cell from which to reach a cell
        [None for __ in range(n_cols)] for _ in range(n_rows)
    ]
    actions = [ # the action that the parent took to reach the cell
        [None for __ in range(n_cols)] for _ in range(n_rows)
    ]

    movement = []
    # ----------------------------------------
    # finish the code below
    # ----------------------------------------
#############################################################################
    open_set.add(start) # add the first node to the stack
    while len(open_set) > 0: # while there are still nodes in the stack
        # pop the last node in the stack
        current = open_set.pop()
        closed_set.add(current)
        # check if the current node is the goal
        if current == goal:
            # reconstruct the path
            while parent[current[0]][current[1]] is not None:
                movement.append(actions[current[0]][current[1]])
                current = parent[current[0]][current[1]]
            movement.reverse()
            return movement, closed_set
        
        # check all the neighbors of the current node
        for action in ACTIONS:
            neighbor = (current[0] + action[0], current[1] + action[1])
            if neighbor[0] < 0 or neighbor[0] >= n_rows or neighbor[1] < 0 or neighbor[1] >= n_cols: # determine if the neighbor exists as a node in the grid
                continue
            if neighbor in obstacles:
                continue
            if neighbor in closed_set:
                continue

            # new node has been reached, add it to the open set
            if neighbor not in open_set:
                open_set.add(neighbor)
                parent[neighbor[0]][neighbor[1]] = current
                actions[neighbor[0]][neighbor[1]] = action
#############################################################################
    return movement, closed_set

def costFn():
    return 1 # all cells have the same cost


def uniform_cost_search(grid_size, start, goal, obstacles, costFn, logger):
    """
    Uniform-cost search algorithm finds the optimal path from 
    the start cell to the goal cell in the 2D grid world. 
    
    After expanding a node, to retrieve the cost of a child node at location (x,y), 
    please call costFn((x,y)). 

    See depth_first_search() for details.
    """
    n_rows, n_cols = grid_size
    start_row, start_col = start
    goal_row, goal_col = goal

    ##########################################
    # Choose a proper container yourself from
    # OrderedSet, Stack, Queue, PriorityQueue
    # for the open set and closed set.
    open_set = PriorityQueue()
    closed_set = OrderedSet()
    ##########################################

    ##########################################
    # Set up visualization logger hook
    # Please do not modify these four lines
    closed_set.logger = logger
    logger.closed_set = closed_set
    open_set.logger = logger
    logger.open_set = open_set
    ##########################################

    parent = [ # the immediate predecessor cell from which to reach a cell
        [None for __ in range(n_cols)] for _ in range(n_rows)
    ]
    actions = [ # the action that the parent took to reach the cell
        [None for __ in range(n_cols)] for _ in range(n_rows)
    ]

    costs = {} # Dictionary to store the minimum cumulative cost (g_cost) found so far for each cell

    movement = []
    # ----------------------------------------
    # finish the code below
    # ----------------------------------------
#############################################################################
    # initialize the starting node
    costs[start] = 0
    open_set.put(start, 0) # add the first node to the priority queue with cost 0

    while len(open_set) > 0:
        current, current_g_cost = open_set.pop() # pop highest priority node (lowest cost)

        if current in closed_set: # If already in closed set, skip processing
           continue

        closed_set.add(current) # add the current node to the closed set

        if current == goal: #goal node reached
            path_current = goal
            while parent[path_current[0]][path_current[1]] is not None:
                action_taken = actions[path_current[0]][path_current[1]]
                movement.append(action_taken)
                path_current = parent[path_current[0]][path_current[1]]
            movement.reverse()
            return movement, closed_set

        for action in ACTIONS:
            row_change, col_change = action
            neighbor_row, neighbor_col = current[0] + row_change, current[1] + col_change
            neighbor = (neighbor_row, neighbor_col)

            ##check if the neighbor is within the grid bounds
            if not (0 <= neighbor_row < n_rows and 0 <= neighbor_col < n_cols):
                continue

            # check obstacles
            if neighbor in obstacles:
                continue
            
            #check in closed set
            if neighbor in closed_set:
                continue
            
            #calculate function cost
            step_cost = costFn(neighbor)
            new_g_cost = current_g_cost + step_cost

            # 5. Check if this path to the neighbor is better than any previously found path OR if neighbor is new
            existing_g_cost = costs.get(neighbor, float('inf')) # Get current best cost, default infinity

            if new_g_cost < existing_g_cost:
                # Found a better path! Update records.
                costs[neighbor] = new_g_cost # Update the best cost found for neighbor
                parent[neighbor_row][neighbor_col] = current
                actions[neighbor_row][neighbor_col] = action
                open_set.put(neighbor, new_g_cost)

    
    path_current = goal
    while parent[path_current[0]][path_current[1]] is not None:
        action_taken = actions[path_current[0]][path_current[1]]
        movement.append(action_taken)
        path_current = parent[path_current[0]][path_current[1]]
    movement.reverse()
    return movement, closed_set

def astar_search(grid_size, start, goal, obstacles, costFn, logger):
    """
    A* search algorithm finds the optimal path from the start cell to the
    goal cell in the 2D grid world using a heuristic.

    Uses Manhattan distance as the heuristic.

    After expanding a node, to retrieve the cost of landing on a child node at location (x,y),
    please call costFn((x,y)).

    See depth_first_search() for parameter details.
    """
    n_rows, n_cols = grid_size
    start_row, start_col = start
    goal_row, goal_col = goal # Goal coordinates needed for heuristic

    # Use a set for efficient obstacle checking
    obstacle_set = set(obstacles)

    ##########################################
    # Choose a proper container yourself from
    # OrderedSet, Stack, Queue, PriorityQueue
    # for the open set and closed set.
    # A* needs a Priority Queue ordered by f_cost = g_cost + h_cost
    open_set = PriorityQueue()
    closed_set = OrderedSet()
    ##########################################

    ##########################################
    # Set up visualization logger hook
    # Please do not modify these four lines
    closed_set.logger = logger
    logger.closed_set = closed_set
    open_set.logger = logger
    logger.open_set = open_set
    ##########################################

    parent = [ # the immediate predecessor cell from which to reach a cell
        [None for __ in range(n_cols)] for _ in range(n_rows)
    ]
    actions = [ # the action that the parent took to reach the cell
        [None for __ in range(n_cols)] for _ in range(n_rows)
    ]

    # Dictionary to store the minimum cumulative cost (g_cost) found so far for each cell
    g_costs = {}

    movement = []

    # ----------------------------------------
    # Manhattan distance heuristic implementation
    # ----------------------------------------
    def heuristic(row, col):
        """Calculates the Manhattan distance from (row, col) to the goal."""
#############################################################################
        # Manhattan distance: |delta_row| + |delta_col|
        return abs(row - goal_row) + abs(col - goal_col)
#############################################################################

    # --- A* Algorithm Implementation ---

    # Initialize start node: g_cost = 0, calculate h_cost and f_cost
    g_costs[start] = 0
    h_start = heuristic(start_row, start_col)
    f_start = g_costs[start] + h_start


    open_set.put(start, f_start)

    while len(open_set) > 0:
        
        try:
             current, current_f_cost_popped = open_set.pop()
        except IndexError: # Handle empty queue case if pop raises it
             break

        current_g_cost = g_costs.get(current) 
        if current in closed_set:
           continue

        closed_set.add(current)

        if current == goal:
            path_current = goal
            while parent[path_current[0]][path_current[1]] is not None:
                action_taken = actions[path_current[0]][path_current[1]]
                movement.append(action_taken)
                path_current = parent[path_current[0]][path_current[1]]
            movement.reverse() 
            return movement, closed_set

        for action in ACTIONS:
            row_change, col_change = action

            if not isinstance(current, tuple) or len(current) != 2:
                 print(f"ERROR: 'current' is not a valid coordinate tuple. Value: {current}, Type: {type(current)}")
                 return [], closed_set 

            neighbor_row = current[0] + row_change
            neighbor_col = current[1] + col_change
            neighbor = (neighbor_row, neighbor_col)

            if not (0 <= neighbor_row < n_rows and 0 <= neighbor_col < n_cols):
                continue

            if neighbor in obstacle_set:
                continue

            step_cost = costFn(neighbor) # Cost of landing on the neighbor cell
            new_g_cost = current_g_cost + step_cost

            if neighbor in closed_set:
                 continue

            #check if neighbor is better than any previously found path OR if neighbor is new
            existing_g_cost = g_costs.get(neighbor, float('inf')) # Get current best known g_cost

            if new_g_cost < existing_g_cost:
                # update records.
                g_costs[neighbor] = new_g_cost # Update the best g_cost found for neighbor
                parent[neighbor_row][neighbor_col] = current
                actions[neighbor_row][neighbor_col] = action

                # calculate the f_cost = g_cost + h_cost for the priority queue
                h_neighbor = heuristic(neighbor_row, neighbor_col)
                new_f_cost = new_g_cost + h_neighbor
                open_set.put(neighbor, new_f_cost)

    # If the loop finishes without finding the goal, no path exists
    return movement, closed_set

if __name__ == "__main__":
    # make sure actions and cost are defined correctly
    from utils.search_app import App
    assert(ACTIONS == App.ACTIONS)

    import tkinter as tk

    algs = {
        "Breadth-First Search": breadth_first_search,
        "Depth-First Search": depth_first_search,
        "Uniform Cost Search": uniform_cost_search,
        "A* Search": astar_search
    }

    root = tk.Tk()
    App(algs, root)
    root.mainloop()

