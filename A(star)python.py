"""
Pathfinding with A* Algorithm

This script implements the A* (A-star) algorithm for finding the shortest path
between two points on a grid. It uses a priority queue (heap) for efficient node management.

Author: [Your Name]
Date: [Current Date]
"""

import heapq  # For priority queue functionality

# Node class to store information about each cell in the grid
class Node:
    def __init__(self, position, g=0, h=0):
        self.position = position  # (x, y) coordinates of the node
        self.g = g  # Cost from start node
        self.h = h  # Heuristic (estimated cost to goal)
        self.f = g + h  # Total cost (g + h)
        self.parent = None  # Reference to the previous node for backtracking the path

    # For priority queue comparison (lower 'f' values get higher priority)
    def __lt__(self, other):
        return self.f < other.f

# Heuristic function using Manhattan distance (best for grid-based movement)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* Algorithm implementation
def a_star(grid, start, end):
    open_list = []  # Priority queue for nodes to explore
    closed_set = set()  # Set for visited nodes

    # Initialize the starting node with zero cost and add it to the open list
    start_node = Node(start, 0, heuristic(start, end))
    heapq.heappush(open_list, start_node)

    # Main loop to explore nodes until the goal is reached or no path exists
    while open_list:
        current_node = heapq.heappop(open_list)  # Node with lowest f value

        # Goal check - path found
        if current_node.position == end:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]  # Return path in correct order

        # Mark the current node as visited
        closed_set.add(current_node.position)

        # Explore neighboring nodes (up, down, left, right)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor_pos = (current_node.position[0] + dx, current_node.position[1] + dy)

            # Boundary and obstacle check
            if (0 <= neighbor_pos[0] < len(grid) and
                0 <= neighbor_pos[1] < len(grid[0]) and
                grid[neighbor_pos[0]][neighbor_pos[1]] == 0 and
                neighbor_pos not in closed_set):

                # Calculate the cost for the neighbor
                g_score = current_node.g + 1
                neighbor_node = Node(neighbor_pos, g_score, heuristic(neighbor_pos, end))
                neighbor_node.parent = current_node  # Track the path

                # Avoid adding duplicate nodes with higher costs
                if any(node.position == neighbor_pos and node.f <= neighbor_node.f for node in open_list):
                    continue

                heapq.heappush(open_list, neighbor_node)

    # If no path is found
    return None

# Example grid (0 = walkable, 1 = obstacle)
grid = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 0, 1, 0]
]

# Define start and end points for pathfinding
def get_valid_coordinates(prompt, grid):
    while True:
        try:
            x, y = map(int, input(prompt).split())
            if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
                if grid[x][y] == 1:
                    print("That position contains an obstacle. Please choose a walkable position.")
                    continue
                return (x, y)
            else:
                print(f"Coordinates must be between (0,0) and ({len(grid)-1},{len(grid[0])-1})")
        except ValueError:
            print("Please enter two numbers separated by a space (e.g., '2 3')")

# Get start and end points from user input
print("\nGrid layout (0 = walkable, 1 = obstacle):")
for row in grid:
    print(row)
print("\nEnter coordinates as 'x y' (separated by space)")

start = get_valid_coordinates("Enter start position: ", grid)
end = get_valid_coordinates("Enter end position: ", grid)
# Execute A* algorithm and display results
path = a_star(grid, start, end)
if path:
    print("Path found:", path)
else:
    print("No path found")
