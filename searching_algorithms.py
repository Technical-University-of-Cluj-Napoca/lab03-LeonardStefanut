from utils import *
from collections import deque
from queue import PriorityQueue
from grid import Grid
from spot import Spot

def reconstruct_path(came_from: dict[Spot, Spot], current: Spot, draw: callable) -> None:
 
    while current in came_from:
        current = came_from[current]
        if not current.is_start():
            current.make_path()
        draw()

def bfs(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    """
    Breadth-First Search (BFS) Algorithm.
    Args:
        draw (callable): A function to call to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
    Returns:
        bool: True if a path is found, False otherwise.
    """
    if not start or not end:
        return False

    queue = deque()
    queue.append(start)
    visited = {start}
    came_from: dict[Spot, Spot] = {}

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current = queue.popleft()

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited and not neighbor.is_barrier():
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()
            
    return False

def dfs(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    """
    Depth-First Search (DFS) Algorithm.
    Args:
        draw (callable): A function to call to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
    Returns:
        bool: True if a path is found, False otherwise.
    """
    if not start or not end:
        return False
        
    stack = []
    stack.append(start)
    visited = {start}
    came_from: dict[Spot, Spot] = {}

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current = stack.pop()

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited and not neighbor.is_barrier():
                visited.add(neighbor)
                came_from[neighbor] = current
                stack.append(neighbor)
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()
            
    return False

def h_manhattan_distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    """
    Heuristic function for A* algorithm: uses the Manhattan distance between two points.
    Args:
        p1 (tuple[int, int]): The first point (x1, y1).
        p2 (tuple[int, int]): The second point (x2, y2).
    Returns:
        float: The Manhattan distance between p1 and p2.
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def h_euclidian_distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    """
    Heuristic function for A* algorithm: uses the Euclidian distance between two points.
    Args:
        p1 (tuple[int, int]): The first point (x1, y1).
        p2 (tuple[int, int]): The second point (x2, y2).
    Returns:
        float: The Manhattan distance between p1 and p2.
    """
    from math import sqrt
    x1, y1 = p1
    x2, y2 = p2
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)


def astar(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    """
    A* Pathfinding Algorithm.
    Args:
        draw (callable): A function to call to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
    Returns:
        bool: True if a path is found, False otherwise.
    """
    if not start or not end:
        return False

    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))

    came_from: dict[Spot, Spot] = {}

    g_score: dict[Spot, float] = {spot: float("inf") for row in grid.grid for spot in row}
    g_score[start] = 0

    f_score: dict[Spot, float] = {spot: float("inf") for row in grid.grid for spot in row}
    f_score[start] = h_manhattan_distance(start.get_position(), end.get_position())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current: Spot = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h_manhattan_distance(neighbor.get_position(), end.get_position())
                
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def ucs(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    if not start or not end:
        return False

    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start)) 

    came_from: dict[Spot, Spot] = {}

    g_score: dict[Spot, float] = {spot: float("inf") for row in grid.grid for spot in row}
    g_score[start] = 0

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current: Spot = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((g_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def greedy_search(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    if not start or not end:
        return False

    count = 0
    open_set = PriorityQueue()
    
    h_score = h_manhattan_distance(start.get_position(), end.get_position())
    open_set.put((h_score, count, start)) 

    came_from: dict[Spot, Spot] = {}
    visited = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current: Spot = open_set.get()[2]

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                came_from[neighbor] = current
                visited.add(neighbor)
                h_score = h_manhattan_distance(neighbor.get_position(), end.get_position())
                count += 1
                open_set.put((h_score, count, neighbor))
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def dls(draw: callable, grid: Grid, start: Spot, end: Spot,limit:int) -> bool:
    
    if not start or not end:
        return False
        
    stack = [(start, 0)]
    visited = {start}
    came_from: dict[Spot, Spot] = {}

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current, depth = stack.pop()

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        if depth < limit:
            for neighbor in current.neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    stack.append((neighbor, depth + 1))
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()
            
    return False

def ids(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    if not start or not end:
        return False
    
    max_depth = grid.rows * grid.cols

    for i in range(max_depth):
        for row in grid.grid:
            for spot in row:
                if not spot.is_start() and not spot.is_end() and not spot.is_barrier():
                    spot.reset()

        if dls(draw, grid, start, end, i):
            return True
            
    return False

def search(draw: callable, path: list[Spot], g_score: float, limit: float, end: Spot, visited_nodes: set[Spot]) -> tuple[bool, float]:
    current_node = path[-1]
    f_score = g_score + h_manhattan_distance(current_node.get_position(), end.get_position())

    if f_score > limit:
        return False, f_score

    if current_node == end:
        return True, limit

    min_val = float("inf")

    for neighbor in current_node.neighbors:
        if neighbor not in path:
            path.append(neighbor)
            visited_nodes.add(neighbor)
            
            if not neighbor.is_end():
                neighbor.make_open()
            draw()

            found, new_limit = search(draw, path, g_score + 1, limit, end, visited_nodes)

            if found:
                return True, new_limit

            if new_limit < min_val:
                min_val = new_limit

            path.pop()
            if not neighbor.is_start() and not neighbor.is_end():
                neighbor.make_closed()
            draw()

    return False, min_val

def ida_star(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    if not start or not end:
        return False

    limit = h_manhattan_distance(start.get_position(), end.get_position())
    path = [start]
    visited_nodes = {start}

    while True:
        found, new_limit = search(draw, path, 0, limit, end, visited_nodes)

        if found:
            for node in path:
                if not node.is_start() and not node.is_end():
                    node.make_path()
            end.make_end()
            start.make_start()
            draw()
            return True

        if new_limit == float("inf"):
            return False

        limit = new_limit
        
        for row in grid.grid:
            for spot in row:
                if not spot.is_start() and not spot.is_end() and not spot.is_barrier():
                    spot.reset()
        start.make_start()
        end.make_end()
        draw()
# and the others algorithms...
# ▢ Depth-Limited Search (DLS)
# ▢ Uninformed Cost Search (UCS)
# ▢ Greedy Search
# ▢ Iterative Deepening Search/Iterative Deepening Depth-First Search (IDS/IDDFS)
# ▢ Iterative Deepening A* (IDA)
# Assume that each edge (graph weight) equalss