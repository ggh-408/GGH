import time


def sudo_solve(sudo):
    def legal(number, row, col):
        for rc in range(9):
            if sudo[row][rc] == number or sudo[rc][col] == number:
                return False

        for bol_r in range(3 * (row // 3), 3 * (row // 3) + 3):
            for blo_c in range(3 * (col // 3), 3 * (col // 3) + 3):
                if sudo[bol_r][blo_c] == number:
                    return False

        return True

    def check():
        for r in range(9):
            for c in range(9):
                if sudo[r][c]:
                    tmp = sudo[r][c]
                    sudo[r][c] = 0
                    if legal(tmp, r, c):
                        sudo[r][c] = tmp
                    else:
                        return False
        return True

    def fill():
        key = True
        flag = False
        same_number = False
        sign_r, sign_c = 0, 0
        sign_number = 0
        while key:
            key = False
            for number in range(1, 10):
                for r in range(9):
                    for c in range(9):
                        if not sudo[r][c] and legal(number, r, c):
                            if same_number:
                                same_number = False
                                break
                            sign_r = r
                            sign_c = c
                            same_number = True
                    if same_number:
                        key = True
                        same_number = False
                        sudo[sign_r][sign_c] = number
                    for c in range(9):
                        if not sudo[c][r] and legal(number, c, r):
                            if same_number:
                                same_number = False
                                break
                            sign_r = c
                            sign_c = r
                            same_number = True
                    if same_number:
                        key = True
                        same_number = False
                        sudo[sign_r][sign_c] = number

                for blo_r in range(0, 9, 3):
                    for blo_c in range(0, 9, 3):
                        for r in range(blo_r, blo_r + 3):
                            for c in range(blo_c, blo_c + 3):
                                if not sudo[r][c] and legal(number, r, c):
                                    if same_number:
                                        same_number = False
                                        flag = True
                                        break
                                    sign_r = r
                                    sign_c = c
                                    same_number = True
                            if flag:
                                flag = False
                                break
                        if same_number:
                            key = True
                            same_number = False
                            sudo[sign_r][sign_c] = number
            for r in range(9):
                for c in range(9):
                    if not sudo[r][c]:
                        for number_only in range(1, 10):
                            if legal(number_only, r, c):
                                if same_number:
                                    same_number = False
                                    break
                                sign_number = number_only
                                same_number = True
                        if same_number:
                            key = True
                            same_number = False
                            sudo[r][c] = sign_number

    def get_cache():
        keys = [(-1, -1, -1)]
        values = [(0, 0, 0)]
        for r in range(9):
            for c in range(9):
                if not sudo[r][c]:
                    keys.append([r, c, 3 * (r // 3) + c // 3])
                    values.append([number for number in range(1, 10) if legal(number, r, c)])
        return keys, values

    # ———————————————————迭代函数———————————————————
    def solve():
        nonlocal coordinate
        if not coordinate:
            return True
        row, col, blo = cache_keys[coordinate]
        for value in cache_values[coordinate]:
            if legal_r[row][value] and legal_c[col][value] and legal_b[blo][value]:
                legal_r[row][value] = False
                legal_c[col][value] = False
                legal_b[blo][value] = False
                coordinate -= 1
                if solve():
                    sudo[row][col] = value
                    return True
                legal_r[row][value] = True
                legal_c[col][value] = True
                legal_b[blo][value] = True
                coordinate += 1
        return False

    if not check():
        return None, 0.0
    time_start = time.time()
    fill()
    cache_keys, cache_values = get_cache()
    coordinate = len(cache_keys) - 1
    legal_r = [[True for _ in range(10)] for _ in range(9)]
    legal_c = [[True for _ in range(10)] for _ in range(9)]
    legal_b = [[True for _ in range(10)] for _ in range(9)]
    solve()
    time_end = time.time()
    return sudo, time_end - time_start


if __name__ == '__main__':
    # ————————————————构建数独————————————————
    sudo_demo = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 3, 6, 0, 0, 0, 0, 0],
                 [0, 7, 0, 0, 9, 0, 2, 0, 0],
                 [0, 5, 0, 0, 0, 7, 0, 0, 0],
                 [0, 0, 0, 0, 4, 5, 7, 0, 0],
                 [0, 0, 0, 1, 0, 0, 0, 3, 0],
                 [0, 0, 1, 0, 0, 0, 0, 6, 8],
                 [0, 0, 8, 5, 0, 0, 0, 1, 0],
                 [0, 9, 0, 0, 0, 0, 4, 0, 0]]
    #
    # sudo_demo = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
    #              [0, 0, 0, 0, 0, 3, 0, 8, 5],
    #              [0, 0, 1, 0, 2, 0, 0, 0, 0],
    #              [0, 0, 0, 5, 0, 7, 0, 0, 0],
    #              [0, 0, 4, 0, 0, 0, 1, 0, 0],
    #              [0, 9, 0, 0, 0, 0, 0, 0, 0],
    #              [5, 0, 0, 0, 0, 0, 0, 7, 3],
    #              [0, 0, 2, 0, 1, 0, 0, 0, 0],
    #              [0, 0, 0, 0, 4, 0, 0, 0, 9]]
    #
    # sudo_demo = [[1, 0, 0, 4, 0, 0, 8, 0, 0],
    #              [0, 4, 0, 0, 3, 0, 0, 0, 9],
    #              [0, 0, 9, 0, 0, 6, 0, 5, 0],
    #              [0, 5, 0, 3, 0, 0, 0, 0, 0],
    #              [0, 0, 0, 0, 0, 1, 6, 0, 0],
    #              [0, 0, 0, 0, 7, 0, 0, 0, 2],
    #              [0, 0, 4, 0, 1, 0, 9, 0, 0],
    #              [7, 0, 0, 8, 0, 0, 0, 0, 4],
    #              [0, 2, 0, 0, 0, 4, 0, 8, 0]]
    print(sudo_solve(sudo_demo))
