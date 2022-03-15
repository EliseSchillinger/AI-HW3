import sys
import copy
from collections import deque
import time

class pengu: # class for attributes of pengu
    def __init__(pengu, score, death, location, can_move, game_grid, move_tracker,valid_move) -> None:
        """ pengu class creation """

        pengu.score = score
        pengu.death = death
        pengu.location = location
        pengu.can_move = can_move
        pengu.move_tracker = move_tracker
        pengu.game_grid = game_grid
        pengu.valid_move = valid_move

    def pengu_start():
        """ initialized upon object creation """

        pengu.score = 0
        pengu.death, pengu.can_move, pengu.valid_move = False, True, True
        pengu.location, pengu.game_grid, pengu.visited = [], [], []
        pengu.move_tracker = ''

    def move_restart():
        """ reset for the beginning of every path test """

        pengu.score = 0
        pengu.death, pengu.can_move, pengu.valid_move = False, True, True

def get_input(rows, columns, initial_game_grid):
    """ reads through the input file to create the grid for the game """

    with open("test-input.txt", 'r') as input_file:
        rows, columns = [int(x) for x in next(input_file).split()]  # reads rows and columns from the first line
        initial_game_grid = []
        for line in input_file:  # read rest of lines and add symbols to game grid 2D list
            initial_game_grid.append([char for char in line.strip()])
        return rows, columns, initial_game_grid

def starting_game_info(rows, columns, initial_game_grid, pengu, num_of_fish, initial_location):
    """ determines pengu's initial location and the total number of fish on the board """

    for x in range(0, rows-1): # iterates through the game_grid array using rows & columns
        for y in range(0, columns-1):
            if initial_game_grid[x][y] == "P": # finds initial pengu location
                pengu.location = [x, y]
                initial_location = [x,y]


            if initial_game_grid[x][y] == "*": 
                num_of_fish += 1

    return pengu, num_of_fish, initial_location

def movement_choice(pengu, pengu_move):
    """ implements pengu's movement choice
        8 different directions according to keypad number.
        coordinates according to matrix, not xy coordinate system """

    next_location = pengu.location[:]
    
    if pengu_move == 1: # southwest
        next_location[0] = next_location[0]+1
        next_location[1] = next_location[1]-1
    elif pengu_move == 2: # south
        next_location[0] = next_location[0]+1
    elif pengu_move == 3: # southeast
        next_location[0] = next_location[0]+1
        next_location[1] = next_location[1]+1
    elif pengu_move == 4: # west
        next_location[1] = next_location[1]-1
    elif pengu_move == 6: # east
        next_location[1] = next_location[1]+1
    elif pengu_move == 7: # northwest
        next_location[0] = next_location[0]-1
        next_location[1] = next_location[1]-1
    elif pengu_move == 8: # north
        next_location[0] = next_location[0]-1
    elif pengu_move == 9: # northeast
        next_location[0] = next_location[0]-1
        next_location[1] = next_location[1]+1
    elif pengu_move == 0:
        return
    # prevents pengu from going outside walls
    if next_location[0] < 0:
        next_location[0] = 0
    if next_location[1] < 0:
        next_location[1] = 0

    return next_location

def movement_check_function(pengu, path):
    """ determines if pengu can move, updates symbols and score accordingly """

    # reset before the start of next path tested just in case
    pengu.valid_move = True

    next_location = movement_choice(pengu, path)

    if pengu.game_grid[next_location[0]][next_location[1]] == '#': # Wall
        pengu.can_move = False
        pengu.valid_move = False
        return pengu
    elif pengu.game_grid[next_location[0]][next_location[1]] == '*': # Fish
        pengu.score += 1
        pengu.game_grid[next_location[0]][next_location[1]] = ' ' 
    elif pengu.game_grid[next_location[0]][next_location[1]] == ' ': # Ice
        pass
    elif pengu.game_grid[next_location[0]][next_location[1]] == '0': # Snow Block
        pengu.can_move = False
    elif pengu.game_grid[next_location[0]][next_location[1]] == 'S': # Shark: pengu dies and is replaced with 'X'
        # pengu.game_grid[next_location[0]][next_location[1]] = 'X'
        pengu.can_move = False
        pengu.valid_move = False
        pengu.death = True
        return pengu
    elif pengu.game_grid[next_location[0]][next_location[1]] == 'U': # Bear: pengu dies and is replaced with 'X'
        # pengu.game_grid[next_location[0]][next_location[1]] = 'X'
        pengu.can_move = False
        pengu.valid_move = False
        pengu.death = True
        return pengu
    pengu.location = next_location[:]

    return pengu

def valid_move(pengu, current_test_location):
    """ determines whether pengu's move was actually valid
        for ex. pengu doesn't actually move bc his direction is directly towards a wall
        vs. can_move becoming false after actual movement in the grid
    """

    if pengu.location != current_test_location and (pengu.can_move == False and pengu.valid_move == False and pengu.death == False):
        return True
    elif pengu.valid_move == True:
        return True
    elif pengu.valid_move == False:
        return False

def copy_game_grid(initial_game_grid):
    """ copies the initial gameboard to pengu's current board"""

    temp_grid = []
    for i in range(len(initial_game_grid)):
        temp_grid.append(initial_game_grid[i][:])
    return temp_grid

def write_output(pengu):
    """ opens up file for output and writes the updated game map to that file """

    original_stdout = sys.stdout

    with open("output.txt", "w") as output_file: # file open while writing output then closed at end
        pengu.game_grid[pengu.location[0]][pengu.location[1]] = 'P'
        output_file.write(pengu.move_tracker + "\n")
        output_file.write(str(pengu.score) + "\n")
        sys.stdout = output_file  # alters the standard output to write directly to file
        for rows in pengu.game_grid:
            print(str(rows).strip("'[']").replace("', '", ''))
        sys.stdout = original_stdout
    return

def bounded_dfs(initial_game_grid, initial_location, current_test_location, path, goal, depth_limit, pengu_obj, frontier):
    """returns depth limited path"""

    limit_hit = False
    frontier.append(path)
 
    while frontier: # as long as the frontier stack isn't empty, test algorithm
        path = frontier.pop()
        # reset every iteration: 
        pengu_obj.location = copy.copy(initial_location)
        pengu_obj.game_grid = copy_game_grid(initial_game_grid) 
        pengu_obj.move_restart()

        # clear the 'P' from pengu's initial location
        pengu_obj.game_grid[pengu_obj.location[0]][pengu_obj.location[1]] = ' '

        # if path is the length of the depth limit, execute entire path and check for goal
        if len(path) == depth_limit:
            for move in path:
                pengu_obj.can_move = True
                while pengu_obj.can_move:
                    pengu_obj = movement_check_function(pengu_obj, move)
           
            if pengu_obj.score == goal:
                return path
            else:
                limit_hit = True

        else:
            for move in path: # do entire movement path up until next moves necessary
                pengu_obj.can_move = True
                while pengu_obj.can_move:
                    pengu_obj = movement_check_function(pengu_obj, move)

            # temporary location variable for pengu after the path is gone through above
            current_test_location = pengu_obj.location[:]
            
            for move in range(1,10): # test all keypad moves excluding 5
                if move == 5:
                    continue
                # pengu starts from the path tested in previous segment of the loop. resets necessary attributes for path testing
                pengu_obj.location = current_test_location[:]
                pengu_obj.move_restart()

                test_move = [] # holds currently tested move instead of entire path

                test_move.append(move)
                while pengu_obj.can_move:
                    pengu_obj = movement_check_function(pengu_obj, move)
    
                if valid_move(pengu_obj, current_test_location): # add to the frontier
                    path.append(test_move[0])
                    frontier.append(path[:])
                    path = path[:-1] # remove from path afterwards in order to check next valid move
                else: # otherwise ignore
                    continue
    return limit_hit

def main_id_dfs():
    """ - main function for ID-DFS: initializes all necessary variables
        - runs ID-DFS loop and calls the bounded DFS function """

    # initilization
    pengu_obj = pengu
    pengu_obj.pengu_start()
    num_of_fish, rows, columns = 0, 0, 0
    initial_location, initial_game_grid, current_test_location, path = [], [], [], []

    # HW 3 specific variables
    frontier = deque([])
    goal = 16
    result = True
    max_depth = 12

    # getting information necessary for all lists and variables
    rows, columns, initial_game_grid = get_input(rows, columns, initial_game_grid)
    pengu_obj, num_of_fish, initial_location = starting_game_info(rows, columns, initial_game_grid, pengu_obj, num_of_fish, initial_location)
    pengu_obj.game_grid = copy_game_grid(initial_game_grid)

    # ID-DFS
    depth = 0
    while(result):
        result = bounded_dfs(initial_game_grid, initial_location, current_test_location, path, goal, depth, pengu_obj, frontier)
        if pengu_obj.score == goal:
            pengu_obj.move_tracker = str(result)
            write_output(pengu_obj)
            return
        depth = depth + 1
        path = [] #ensure path is cleared for next iteration

# run primary function, determine time taken to execute
start_time= time.time()
main_id_dfs()
print("---------- %s seconds ---------" % (time.time()- start_time))

