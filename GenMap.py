from random import randint


def export_map(map: list[list[int]], file: str) -> None:
    f = open(file, "w")
    for i in range(len(map)):
        for j in range(len(map[0])):
            f.write(str(map[i][j]))
            if j != len(map[0]) - 1:
                f.write(" ")
        if i != len(map) - 1:
            f.write("\n")
    f.close()


def gen_map(N: int, M: int) -> list[list[int]]: # N is row, M is column
    map = [[0 for i in range(M)] for j in range(N)]
    for i in range(N):
        for j in range(M):
            if i == 0 or i == N-1 or j == 0 or j == M-1: # map must be covered by walls
                map[i][j] = 1
    map[N -2][1] = 3 # seeker
    map[1][M - 2] = 2 # hider
    
    type_map = randint(0, 3)
    # 0: discrete walls
    # 1: rectangle walls
    # 2: L-character walls
    # 3: square-triangle walls

    type_map = 0
    if type_map == 0:
        create_discrete_walls(map, N, M)
    # elif type_map == 1:
    #     create_rectangle_walls(map, N, M)
    # elif type_map == 2:
    #     create_L_walls(map, N, M)
    # else:
    #     create_square_triangle_walls(map, N, M)

    return map


def create_discrete_walls(map: list[list[int]], N: int, M: int) -> None:
    num_walls = (N - 2) * (M - 2) // 10 + randint(1,2)
    cnt_walls = 0
    max_continous_walls = 2
    cnt_continous_walls = 0

    while cnt_walls < num_walls:
        x = randint(1, N-2)
        y = randint(1, M-2)

        if map[x][y] == 0:
            # to avoid creating diagonal walls
            if x == 1:
                if map[x+1][y-1] == 1 or map[x+1][y+1] == 1:
                    continue
            elif x == N-2:
                if map[x-1][y-1] == 1 or map[x-1][y+1] == 1:
                    continue
            if y == 1:
                if map[x-1][y+1] == 1 or map[x+1][y+1] == 1:
                    continue
            elif y == M-2:
                if map[x-1][y-1] == 1 or map[x+1][y-1] == 1:
                    continue
            
            if (map[x-1][y] == 1 and x != 1) or (map[x+1][y] == 1 and x != N-2) or (map[x][y-1] == 1 and y != 1) or (map[x][y+1] == 1 and y != M-2):
                if cnt_continous_walls < max_continous_walls:
                    map[x][y] = 1
                    cnt_walls += 1
                    cnt_continous_walls += 1
            else:
                map[x][y] = 1
                cnt_walls += 1

new_map = gen_map(9, 12)
export_map(new_map, "maze1.txt")