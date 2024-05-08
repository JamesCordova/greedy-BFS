import queue
import tkinter as tk

# to keep track of the blocks of maze
class Grid_Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# each block will have its own position and cost of steps taken
class Node:
    def __init__(self, pos: Grid_Position, cost):
        self.pos = pos
        self.cost = cost

    def __lt__(self, other):
        if self.cost < other.cost:
            return True
        else:
            return False

def heuristic_value(curr_node, dest):
    return (abs(curr_node.x - dest.x) + abs(curr_node.y - dest.y))

# GBFS algo for the maze
def gbfs(Grid, dest: Grid_Position, start: Grid_Position):
    # to get neighbours of current node
    adj_cell_x = [-1, 0, 0, 1]
    adj_cell_y = [0, -1, 1, 0]
    m, n = (len(Grid), len(Grid))
    visited_blocks = [[False for i in range(m)]
                      for j in range(n)]
    visited_blocks[start.x][start.y] = True
    q = queue.PriorityQueue()
    sol = Node(start, 0)
    q.put((0, sol))
    cells = 4
    cost = 0
    while q:
        current = q.get()  # Dequeue the front cell
        current_block = current[1]
        current_pos = current_block.pos

        # if goal found than return cost
        if current_pos.x == dest.x and current_pos.y == dest.y:
            print("Algorithm used = GBFS")
            print("No. of moves utilized = ", cost)
            return current_block.cost

        # if current block not in visited than add in visited
        if current_block not in visited_blocks:
            visited_blocks[current_pos.x][current_pos.y] = True
            cost = cost + 1

        x_pos = current_pos.x
        y_pos = current_pos.y

        for i in range(cells):
            if x_pos == len(Grid) - 1 and adj_cell_x[i] == 1:
                x_pos = current_pos.x
                y_pos = current_pos.y + adj_cell_y[i]
                post = Grid_Position(x_pos, y_pos)
            if y_pos == 0 and adj_cell_y[i] == -1:
                x_pos = current_pos.x + adj_cell_x[i]
                y_pos = current_pos.y
                post = Grid_Position(x_pos, y_pos)
            else:
                x_pos = current_pos.x + adj_cell_x[i]
                y_pos = current_pos.y + adj_cell_y[i]
                post = Grid_Position(x_pos, y_pos)
            if x_pos < 20 and y_pos < 20 and x_pos >= 0 and y_pos >= 0:
                if Grid[x_pos][y_pos] == 1:
                    if not visited_blocks[x_pos][y_pos]:
                        h = heuristic_value(post, dest)  # getting heuristic value of the neighbours
                        next_cell = Node(Grid_Position(x_pos, y_pos), current_block.cost + 1)
                        visited_blocks[x_pos][y_pos] = True
                        q.put((h, next_cell))

    return -1

def A_Star(maze, end, start):
    # Create lists for open nodes and closed nodes
    open1 = queue.PriorityQueue()
    closed = [[False for i in range(len(maze))]
              for j in range(len(maze))]
    closed[start.x][start.y] = True

    # using these cell arrays to get neighbours
    adj_cell_x = [-1, 0, 0, 1]
    adj_cell_y = [0, -1, 1, 0]

    # Create a start node and an goal node
    Start = Node(start, 0)
    goal = Node(end, 0)

    # Add the start node
    open1.put((0, Start))
    cost = 0
    cells = 4

    # Loop until the open list is empty
    while open1:

        # Sort the open list to get the node with the lowest cost first
        # no need cuz priority queue
        # Get the node with the lowest cost

        current = open1.get()  # getting least cost node as open1 is a priority queue
        current_node = current[1]  # getting node in cuurent node
        current_pos = current_node.pos

        # Add the current node to the closed list
        if current_node not in closed:
            closed[current_pos.x][current_pos.y] = True
            cost = cost + 1

        # Check if we have reached the goal, return the path (From Current Node to Start Node By Node.parent)
        if current_pos.x == end.x and current_pos.y == end.y:
            print("Algorithm used = A* Algorithm")
            print("No. of moves utilized = ", cost)
            return current_node.cost

        x_pos = current_pos.x
        y_pos = current_pos.y

        # Get neighbours
        for i in range(cells):
            if x_pos == len(maze) - 1 and adj_cell_x[i] == 1:
                x_pos = current_pos.x
                y_pos = current_pos.y + adj_cell_y[i]
                post = Grid_Position(x_pos, y_pos)
            if y_pos == 0 and adj_cell_y[i] == -1:
                x_pos = current_pos.x + adj_cell_x[i]
                y_pos = current_pos.y
                post = Grid_Position(x_pos, y_pos)
            else:
                x_pos = current_pos.x + adj_cell_x[i]
                y_pos = current_pos.y + adj_cell_y[i]
                post = Grid_Position(x_pos, y_pos)
            if x_pos < 20 and y_pos < 20 and x_pos >= 0 and y_pos >= 0:
                if maze[x_pos][y_pos] == 1:
                    if not closed[x_pos][y_pos]:
                        neighbor = Node(Grid_Position(x_pos, y_pos), current_node.cost + 1)
                        h = heuristic_value(neighbor.pos, end)  # get heuristic value of neighbours
                        f = h + neighbor.cost  # getting f by f = h + g
                        closed[x_pos][y_pos] = True  # adding neighbour to closed
                        open1.put((f, neighbor))

    return -1

def draw_maze(canvas, maze, path, cost_label):
    canvas.delete("all")
    cell_size = 30
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            x1 = j * cell_size
            y1 = i * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            if maze[i][j] == 0:
                canvas.create_rectangle(x1, y1, x2, y2, fill="black")
            else:
                canvas.create_rectangle(x1, y1, x2, y2, fill="white")
            if (i, j) in path:
                canvas.create_oval(x1 + cell_size // 4, y1 + cell_size // 4,
                                   x2 - cell_size // 4, y2 - cell_size // 4,
                                   fill="green")

def gbfs_with_gui(Grid, dest, start):
    # to get neighbours of current node
    adj_cell_x = [-1, 0, 0, 1]
    adj_cell_y = [0, -1, 1, 0]
    m, n = (len(Grid), len(Grid))
    visited_blocks = [[False for i in range(m)]
                      for j in range(n)]
    visited_blocks[start.x][start.y] = True
    q = queue.PriorityQueue()
    sol = Node(start, 0)
    q.put((0, sol))
    cells = 4
    cost = 0
    path = []

    root = tk.Tk()
    canvas = tk.Canvas(root, width=600, height=600)
    canvas.pack()

    cost_label = tk.Label(root, text=f"Costo acumulado: 0", font=("Arial", 12))
    cost_label.pack(side="bottom")

    while q:
        current = q.get()  # Dequeue the front cell
        current_block = current[1]
        current_pos = current_block.pos

        # if goal found than return cost
        if current_pos.x == dest.x and current_pos.y == dest.y:
            print("Algorithm used = GBFS")
            print(f"No. of moves utilized = {cost}")
            print(f"Path cost = {current_block.cost}")
            result_label = tk.Label(root, text=f"No. of moves utilized = {cost}\nPath cost = {current_block.cost}", font=("Arial", 12))
            result_label.pack(side="top")
            root.mainloop()
            return current_block.cost

        # if current block not in visited than add in visited
        if current_block not in visited_blocks:
            visited_blocks[current_pos.x][current_pos.y] = True
            cost += 1
            path.append((current_pos.x, current_pos.y))

        x_pos = current_pos.x
        y_pos = current_pos.y

        for i in range(cells):
            if x_pos == len(Grid) - 1 and adj_cell_x[i] == 1:
                x_pos = current_pos.x
                y_pos = current_pos.y + adj_cell_y[i]
                post = Grid_Position(x_pos, y_pos)
            if y_pos == 0 and adj_cell_y[i] == -1:
                x_pos = current_pos.x + adj_cell_x[i]
                y_pos = current_pos.y
                post = Grid_Position(x_pos, y_pos)
            else:
                x_pos = current_pos.x + adj_cell_x[i]
                y_pos = current_pos.y + adj_cell_y[i]
                post = Grid_Position(x_pos, y_pos)
            if x_pos < 20 and y_pos < 20 and x_pos >= 0 and y_pos >= 0:
                if Grid[x_pos][y_pos] == 1:
                    if not visited_blocks[x_pos][y_pos]:
                        h = heuristic_value(post, dest)  # getting heuristic value of the neighbours
                        next_cell = Node(Grid_Position(x_pos, y_pos), current_block.cost + 1)
                        visited_blocks[x_pos][y_pos] = True
                        q.put((h, next_cell))

        # Actualizar la interfaz
        cost_label.config(text=f"Costo acumulado: {cost}")
        draw_maze(canvas, Grid, path, cost_label)
        root.update()

    return -1

def main():
    maze =  [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1],
             [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
             [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1],
             [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
             [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1],
             [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
             [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1],
             [0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0],
             [0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1],
             [0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
             [1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
             [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
             [0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    destination = Grid_Position(12, 19)
    starting_position = Grid_Position(14, 0)
    res = 0
    res1 = 0

    print()
    res = gbfs_with_gui(maze, destination, starting_position)
    if res != -1:
        print("Path cost = ", res)
    else:
        print("Path does not exist")

    print()
    res1 = A_Star(maze, destination, starting_position)
    if res1 != -1:
        print("Path cost = ", res1)
    else:
        print("Path does not exist")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()