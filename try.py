import random

def create_L_walls(map_: list[list[int]], N: int, M: int) -> None:
    # Function to check if given coordinates are within map boundaries
    def is_valid(x, y):
        return 0 <= x < N and 0 <= y < M

    # Function to check if a wall can be placed at given coordinates
    def can_place_wall(x, y):
        return is_valid(x, y) and map_[x][y] == 0

    # Function to check if the placement creates a diagonal wall
    def is_diagonal(x, y):
        return is_valid(x-1, y-1) and map_[x-1][y] == 1 and map_[x][y-1] == 1

    # Shuffle the order of cells to place walls randomly
    cells = [(i, j) for i in range(N) for j in range(M)]
    random.shuffle(cells)

    max_walls = (N + M) // 5
    num_walls = 0
    while num_walls < max_walls:
        long_edge_size = random.randint(2, 3)
        short_edge_size = random.randint(1, 2)
        for i, j in cells:
            if long_edge_size == 3:
                if short_edge_size == 1:
                    if can_place_wall(i, j) and can_place_wall(i+1, j) and can_place_wall(i+2, j) and can_place_wall(i+2, j+1) and not is_diagonal(i+2, j+1):
                        map_[i][j] = 1
                        map_[i+1][j] = 1
                        map_[i+2][j] = 1
                        map_[i+2][j+1] = 1
                        break
                elif short_edge_size == 2:
                    if can_place_wall(i, j) and can_place_wall(i+1, j) and can_place_wall(i+2, j) and can_place_wall(i+2, j+1) and can_place_wall(i+2, j+2) and not is_diagonal(i+2, j+2):
                        map_[i][j] = 1
                        map_[i+1][j] = 1
                        map_[i+2][j] = 1
                        map_[i+2][j+1] = 1
                        map_[i+2][j+2] = 1
                        break
            elif long_edge_size == 2:
                if short_edge_size == 1:
                    if can_place_wall(i, j) and can_place_wall(i+1, j) and can_place_wall(i+1, j+1) and not is_diagonal(i+1, j+1):
                        map_[i][j] = 1
                        map_[i+1][j] = 1
                        map_[i+1][j+1] = 1
                        break
                elif short_edge_size == 2:
                    if can_place_wall(i, j) and can_place_wall(i+1, j) and can_place_wall(i+1, j+1) and can_place_wall(i+1, j+2) and not is_diagonal(i+1, j+2):
                        map_[i][j] = 1
                        map_[i+1][j] = 1
                        map_[i+1][j+1] = 1
                        map_[i+1][j+2] = 1
                        break
        num_walls += 1

# Example usage:
N = 10
M = 20
my_map = [[0 for _ in range(M)] for _ in range(N)]
create_L_walls(my_map, N, M)

# Print the map with L-shaped walls
for row in my_map:
    print(row)