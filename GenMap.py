from random import randint


def export_map(map: list[list[int]], file: str) -> None:
    f = open(file, "w")
    N = len(map)
    M = len(map[0])
    f.write(str(N) + " " + str(M) + "\n")
    for i in range(N):
        for j in range(M):
            f.write(str(map[i][j]))
            if j != len(map[0]) - 1:
                f.write(" ")
        if i != len(map) - 1:
            f.write("\n")
    f.close()


def check_diagonal_wall(map: list[list[int]], N: int , M: int, x: int, y: int) -> bool:
    if x == 0:
        if y == 0:
            return map[x+1][y+1] == 1
        elif y == M - 1:
            return map[x+1][y-1] == 1
        else:
            return map[x+1][y-1] == 1 or map[x+1][y+1] == 1
    elif x == N - 1:
        if y == 0:
            return map[x-1][y+1] == 1
        elif y == M - 1:
            return map[x-1][y-1] == 1
        else:
            return map[x-1][y-1] == 1 or map[x-1][y+1] == 1
    else:
        if y == 0:
            return map[x-1][y+1] == 1 or map[x+1][y+1] == 1
        elif y == M - 1:
            return map[x-1][y-1] == 1 or map[x+1][y-1] == 1
        else:
            return map[x-1][y-1] == 1 or map[x-1][y+1] == 1 or map[x+1][y-1] == 1 or map[x+1][y+1] == 1


def gen_map(N: int, M: int) -> list[list[int]]: # N is row, M is column
    map = [[0 for i in range(M)] for j in range(N)]

    map[N -1][0] = 3 # seeker
    map[0][M - 1] = 2 # hider
    
    type_map = randint(0, 3)
    # 0: discrete walls
    # 1: rectangle walls
    # 2: L-shape walls
    # 3: square-triangle walls

    # type_map = 0
    type_map = 0
    if type_map == 0:
        create_discrete_walls(map, N, M)
    # elif type_map == 1:
    #     create_rectangle_walls(map, N, M)
    elif type_map == 2:
        create_L_walls(map, N, M) # CÒN NHIỀU BUGS LẮM ;)
    # else:
    #     create_square_triangle_walls(map, N, M)

    return map


def create_discrete_walls(map: list[list[int]], N: int, M: int) -> None:
    num_walls = N*M // 10 + randint(1,2)
    cnt_walls = 0
    max_continous_walls = (N+M) // 10
    cnt_continous_walls = 0

    while cnt_walls < num_walls:
        x = randint(0, N-1)
        y = randint(0, M-1)

        if map[x][y] == 0:
            # to avoid creating diagonal walls
            if check_diagonal_wall(map, N, M, x, y):
                continue
            
            if (x != 0 and map[x-1][y] == 1 ) or (x != N-1 and map[x+1][y] == 1) or (y != 0 and map[x][y-1] == 1) or (y != M-1 and map[x][y+1] == 1):
                if cnt_continous_walls < max_continous_walls:
                    map[x][y] = 1
                    cnt_walls += 1
                    cnt_continous_walls += 1
            else:
                map[x][y] = 1
                cnt_walls += 1


def create_L_walls(map: list[list[int]], N: int, M: int) -> None: # lỗi chặn đường đi + diagonal walls
    horizontal_axis = N // 2
    vertical_axis = M // 2
    max_walls = 4
    cnt_walls = 0
    is_1st_zone = False
    is_2nd_zone = False
    is_3rd_zone = False
    is_4th_zone = False

    while cnt_walls < max_walls:
        x = randint(2, N-3)
        y = randint(2, M-3)

        if map[x][y] == 0:
            if x < horizontal_axis and y < vertical_axis and is_1st_zone == False: # first zone
                direction = randint(0, 1)
                # 0: cạnh dài chĩa xuống
                if direction == 0:
                    for i in range(x, x + N // 3 + 1):
                        map[i][y] = 1
                    side = randint(0, 1)
                    # 0: cạnh ngắn chĩa trái
                    # 1: cạnh ngắn chĩa phải
                    n = randint(2, 3)
                    if side == 0:
                        for i in range(y-1, y-n, -1):
                            if i < 1:
                                break
                            map[x][i] = 1 
                    else:
                        for i in range(y+1, y+n):
                            if i > M-2:
                                break
                            map[x][i] = 1
                else: # 1: cạnh dài chĩa sang phải
                    for i in range(y, y + M // 3 + 1):
                        map[x][i] = 1
                    side = randint(0, 1)
                    # 0: cạnh ngắn chĩa lên
                    # 1: cạnh ngắn chĩa xuống
                    n = randint(2, 3)
                    if side == 0:
                        for i in range(x-1, x-n, -1):
                            if i < 1:
                                break
                            map[i][y] = 1
                    else:
                        for i in range(x+1, x+n):
                            if i > N-2:
                                break
                            map[i][y] = 1
                cnt_walls += 1
                is_1st_zone = True
            elif x < horizontal_axis and y > vertical_axis and is_2nd_zone == False: # second zone
                direction = randint(0, 1)
                # 0: cạnh dài chĩa xuống
                if direction == 0:
                    for i in range(x, N // 3 + 1):
                        map[i][y] = 1
                    side = randint(0, 1)
                    # 0: cạnh ngắn chĩa trái
                    # 1: cạnh ngắn chĩa phải
                    n = randint(2, 3)
                    if side == 0:
                        for i in range(y-1, y-n, -1):
                            if i < 1:
                                break
                            map[x][i] = 1 
                    else:
                        for i in range(y+1, y+n):
                            if i > M-2:
                                break
                            map[x][i] = 1
                else: # 1: cạnh dài chĩa sang trái
                    for i in range(y, y - M // 3 - 1, -1):
                        map[x][i] = 1
                    side = randint(0, 1)
                    # 0: cạnh ngắn chĩa lên
                    # 1: cạnh ngắn chĩa xuống
                    n = randint(2, 3)
                    if side == 0:
                        for i in range(x-1, x-n, -1):
                            if i < 1:
                                break
                            map[i][y] = 1
                    else:
                        for i in range(x+1, x+n):
                            if i > N-2:
                                break
                            map[i][y] = 1
                cnt_walls += 1
                is_2nd_zone = True
            elif x > horizontal_axis and y < vertical_axis and is_3rd_zone == False: # third zone
                direction = randint(0, 1)
                # 0: cạnh dài chĩa lên
                if direction == 0:
                    for i in range(x, x - N // 3 - 1):
                        map[i][y] = 1
                    side = randint(0, 1)
                    # 0: cạnh ngắn chĩa trái
                    # 1: cạnh ngắn chĩa phải
                    n = randint(2, 3)
                    if side == 0:
                        for i in range(y-1, y-n, -1):
                            if i < 1:
                                break
                            map[x][i] = 1 
                    else:
                        for i in range(y+1, y+n):
                            if i > M-2:
                                break
                            map[x][i] = 1
                else: # 1: cạnh dài chĩa sang phải
                    for i in range(y, y + M // 3 + 1):
                        map[x][i] = 1
                    side = randint(0, 1)
                    # 0: cạnh ngắn chĩa lên
                    # 1: cạnh ngắn chĩa xuống
                    n = randint(2, 3)
                    if side == 0:
                        for i in range(x-1, x-n, -1):
                            if i < 1:
                                break
                            map[i][y] = 1
                    else:
                        for i in range(x+1, x+n):
                            if i > N-2:
                                break
                            map[i][y] = 1
                cnt_walls += 1
                is_3rd_zone = True
            elif x > horizontal_axis and y > vertical_axis and is_4th_zone == False: # fourth zone
                direction = randint(0, 1)
                # 0: cạnh dài chĩa lên
                if direction == 0:
                    for i in range(x, x - N // 3 - 1):
                        map[i][y] = 1
                    side = randint(0, 1)
                    # 0: cạnh ngắn chĩa trái
                    # 1: cạnh ngắn chĩa phải
                    n = randint(2, 3)
                    if side == 0:
                        for i in range(y-1, y-n, -1):
                            if i < 1:
                                break
                            map[x][i] = 1 
                    else:
                        for i in range(y+1, y+n):
                            if i > M-2:
                                break
                            map[x][i] = 1
                else: # 1: cạnh dài chĩa sang trái
                    for i in range(y, y - M // 3 - 1, -1):
                        map[x][i] = 1
                    side = randint(0, 1)
                    # 0: cạnh ngắn chĩa lên
                    # 1: cạnh ngắn chĩa xuống
                    n = randint(2, 3)
                    if side == 0:
                        for i in range(x-1, x-n, -1):
                            if i < 1:
                                break
                            map[i][y] = 1
                    else:
                        for i in range(x+1, x+n):
                            if i > N-2:
                                break
                            map[i][y] = 1
                cnt_walls += 1
                is_4th_zone = True


new_map = gen_map(10, 20)
export_map(new_map, "maze7.txt")