import math

ROBOT_DIRECTION_UP = 1
ROBOT_DIRECTION_RIGHT = 2
ROBOT_DIRECTION_DOWN = 3
ROBOT_DIRECTION_LEFT = 4
ROBOT_DIRECTION_NOW = 1
START_X = 0.0
START_Y = 0.0


def check_in_list(my_list, i,j):
	node_x = i
	node_y = j
	for element in my_list:
		if element[0] == node_x and element[1] == node_y:
			return True
	return False

def print_tree_to_file(grid_by_cells,path):
	with open("grid3.txt", "w+") as grid_file:
		i = 0
		for row in (grid_by_cells):
			j = 0
			for cell in row:
				if check_in_list(path,i,j):
					grid_file.write("X")
				else:
					grid_file.write("1") if cell == 1 else grid_file.write("0")
				j = j + 1
			grid_file.write("\n")
			i = i + 1

def readMatrix(path):
    file = open(path, "r")
    matrix = []
    for line in file:
        line_list = []
        for char in line:
            if char != '\n':
                line_list.append(char)
        matrix.append(line_list)
    file.close()
    return matrix


def getLocationIndex(robot_size, world_pos, map_origin):
    return int((world_pos - map_origin) / robot_size)


def DFS(grid, start_x, start_y, world_x, world_y, step_size):
    openSet = set()
    closeSet = set()
    openSet.add((start_x, start_y))
    wentToIndex = {}
    wentToXY = []
    while openSet:
        currentIndex = openSet.pop()
        if currentIndex in closeSet:
            continue
        closeSet.add(currentIndex)
        neighbors = getNeighbors(currentIndex[0], currentIndex[1], grid)
        for neighbor in neighbors:
            if neighbor not in closeSet and neighbor not in openSet:
                if (currentIndex[0], currentIndex[1]) in wentToIndex:
                    wentToIndex[(currentIndex[0], currentIndex[1])].append(neighbor)
                    current_world_x  = 0.35 + ((currentIndex[0] - 0) * step_size)
                    current_world_y  = 0.35 + ((currentIndex[1] - 0) * step_size)
                    neighbor_world_x = 0.35 + ((neighbor[0]     - 0) * step_size)
                    neighbor_world_y = 0.35 + ((neighbor[1]     - 0) * step_size)
                    wentToXY.append((current_world_x, current_world_y, neighbor_world_x, neighbor_world_y))
                else:
                    wentToIndex[(currentIndex[0], currentIndex[1])] = [neighbor]
                    current_world_x  = 0.35 + ((currentIndex[0] - 0) * step_size)
                    current_world_y  = 0.35 + ((currentIndex[1] - 0) * step_size)
                    neighbor_world_x = 0.35 + ((neighbor[0]     - 0) * step_size)
                    neighbor_world_y = 0.35 + ((neighbor[1]     - 0) * step_size)
                    wentToXY.append((current_world_x, current_world_y, neighbor_world_x, neighbor_world_y))
                openSet.add(neighbor)
    return wentToIndex, wentToXY


def getNeighbors(x, y, grid):
    possible_neighbors_list = list()
    if x + 1 < len(grid) and grid[x + 1][y] == '0':
        possible_neighbors_list.append((x + 1, y))
    if x - 1 >= 0 and grid[x - 1][y] == '0':
        possible_neighbors_list.append((x - 1, y))
    if y + 1 < len(grid[0]) and grid[x][y + 1] == '0':
        possible_neighbors_list.append((x, y + 1))
    if y - 1 >= 0 and grid[x][y - 1] == '0':
        possible_neighbors_list.append((x, y - 1))
    return possible_neighbors_list


def getDirectionRelativeToRobot(direction):
    if ROBOT_DIRECTION_NOW == ROBOT_DIRECTION_UP:
        return direction

    elif ROBOT_DIRECTION_NOW == ROBOT_DIRECTION_RIGHT:
        if direction == ROBOT_DIRECTION_RIGHT:
            return ROBOT_DIRECTION_DOWN
        if direction == ROBOT_DIRECTION_UP:
            return ROBOT_DIRECTION_RIGHT
        if direction == ROBOT_DIRECTION_LEFT:
            return ROBOT_DIRECTION_UP
        return ROBOT_DIRECTION_LEFT

    elif ROBOT_DIRECTION_NOW == ROBOT_DIRECTION_DOWN:
        if direction == ROBOT_DIRECTION_RIGHT:
            return ROBOT_DIRECTION_LEFT
        if direction == ROBOT_DIRECTION_UP:
            return ROBOT_DIRECTION_DOWN
        if direction == ROBOT_DIRECTION_LEFT:
            return ROBOT_DIRECTION_RIGHT
        return ROBOT_DIRECTION_UP

    elif ROBOT_DIRECTION_NOW == ROBOT_DIRECTION_LEFT:
        if direction == ROBOT_DIRECTION_RIGHT:
            return ROBOT_DIRECTION_UP
        if direction == ROBOT_DIRECTION_UP:
            return ROBOT_DIRECTION_LEFT
        if direction == ROBOT_DIRECTION_LEFT:
            return ROBOT_DIRECTION_DOWN
        return ROBOT_DIRECTION_RIGHT


def canTurn(direction, walls, current_pos, world_x, world_y):
    real_direction = getDirectionRelativeToRobot(direction)
    print("realllllll")
    print(real_direction)
    if real_direction == ROBOT_DIRECTION_RIGHT:
        next_pos = (current_pos[0], current_pos[1] + 1)
    elif real_direction == ROBOT_DIRECTION_UP:
        next_pos = (current_pos[0] + 1, current_pos[1])
    elif real_direction == ROBOT_DIRECTION_LEFT:
        next_pos = (current_pos[0], current_pos[1] - 1)
    else:
        next_pos = (current_pos[0] - 1, current_pos[1])
    i = 0
    for wall in walls:
        if i == 10:
            break
        i = i + 1
        if isStuckOnWall(wall, current_pos, next_pos, world_x, world_y):
            return False
    return True


def isStuckOnWall(wall, c_pos, n_pos, world_x, world_y):
    step_size = 0.35
    print("world_x")
    print(world_x)
    print("world_y")
    print(world_y)
    print("c_pos")
    print(c_pos)
    print("n_pos")
    print(n_pos)

    current_world_x = world_x + ((c_pos[0] - START_X) * step_size)
    current_world_y = world_y + ((c_pos[1] - START_Y) * step_size)
    neighbor_world_x = world_x + ((n_pos[0] - START_X) * step_size)
    neighbor_world_y = world_y + ((n_pos[1] - START_Y) * step_size)
    print("current_world_x")
    print(current_world_x)
    print("current_world_y")
    print(current_world_y)
    print("neighbor_world_x")
    print(neighbor_world_x)
    print("neighbor_world_y")
    print(neighbor_world_y)
    step_is_vertical = current_world_y == neighbor_world_y
    step_is_horizontal = current_world_x == neighbor_world_x
    wall_is_vertical = wall[1] == wall[3]
    wall_is_horizontal = wall[0] == wall[2]
    if step_is_vertical == wall_is_vertical:
        return False
    if step_is_horizontal == wall_is_horizontal:
        return False
    if step_is_vertical:
        #   Step is vertical and wall is horizontal
        if min(current_world_x, neighbor_world_x) < wall[0] < max(current_world_x, neighbor_world_x):
            if min(wall[1], wall[3]) < current_world_y < max(wall[1], wall[3]):
                return True
    if wall_is_vertical:
        #   Wall is vertical and step is horizontal
        if min(wall[0], wall[2]) < current_world_x < max(wall[0], wall[2]):
            if min(current_world_y, neighbor_world_y) < wall[1] < max(current_world_y, neighbor_world_y):
                return True

    return False


def turn(direction, current_pos):
    if direction == ROBOT_DIRECTION_RIGHT:
        next_pos = (current_pos[0], current_pos[1] + 1)
    elif direction == ROBOT_DIRECTION_UP:
        next_pos = (current_pos[0] + 1, current_pos[1])
    elif direction == ROBOT_DIRECTION_LEFT:
        next_pos = (current_pos[0], current_pos[1] - 1)
    else:
        #   direction == ROBOT_DIRECTION_DOWN
        next_pos = (current_pos[0] - 1, current_pos[1])

    return next_pos


def hamiltonPath(walls, grid, current_pos, world_x, world_y):
    dst_pos = (current_pos[0], current_pos[1])
    path = list()
    path.append((current_pos[0], current_pos[1]))
    canStop = False
    global ROBOT_DIRECTION_NOW
    while current_pos != dst_pos or not canStop:
        if canTurn(ROBOT_DIRECTION_RIGHT, walls, current_pos, world_x, world_y):
            ROBOT_DIRECTION_NOW = getDirectionRelativeToRobot(ROBOT_DIRECTION_RIGHT)
            print("!11111111111111111")
            current_pos = turn(ROBOT_DIRECTION_NOW, current_pos)
        elif canTurn(ROBOT_DIRECTION_UP, walls, current_pos, world_x, world_y):
            ROBOT_DIRECTION_NOW = getDirectionRelativeToRobot(ROBOT_DIRECTION_UP)
            print("!222222222222222222222222")
            current_pos = turn(ROBOT_DIRECTION_NOW, current_pos)
        elif canTurn(ROBOT_DIRECTION_LEFT, walls, current_pos, world_x, world_y):
            ROBOT_DIRECTION_NOW = getDirectionRelativeToRobot(ROBOT_DIRECTION_LEFT)
            current_pos = turn(ROBOT_DIRECTION_NOW, current_pos)
            print("!333333333333333333333")
        path.append(current_pos)
        canStop = True

    return path


def main():
    robotSize = 0.35
    global START_X
    global START_Y
    START_X = 19
    START_Y = 16
    grid_x = 19
    grid_y = 16
    four_grid_x = 9
    four_grid_y = 8
    world_x = 6.900181
    world_y = 5.900000
    map_x = 0.0
    map_y = 0.0

    FourDGrid = readMatrix("d4_grid.txt")
    DGrid = readMatrix("grid.txt")
    _, walls = DFS(FourDGrid, four_grid_x, four_grid_y, world_x, world_y, robotSize * 2)
    circle_path = hamiltonPath(walls, DGrid, (grid_x, grid_y), world_x, world_y)
    print_tree_to_file(DGrid, circle_path)

if __name__ == "__main__":
    print("mainnnnnnnnnnnnnnn")
    main()
