import time


def sudo_solve(sudo):
    def check():
        for r in range(9):
            for c in range(9):
                if sudo[r][c] != 0:
                    b = 3 * (r // 3) + c // 3
                    value = sudo[r][c]
                    if legal_r[r][value] and legal_c[c][value] and legal_b[b][value]:
                        legal_r[r][value] = False
                        legal_c[c][value] = False
                        legal_b[b][value] = False
                    else:
                        return False
        return True

    def fill():
        key = True
        same_number = False
        sign_r, sign_c, sign_b = 0, 0, 0
        sign_number = 0
        while key:
            key = False
            for number in range(1, 10):
                for r in range(9):
                    for c in range(9):
                        b = 3 * (r // 3) + c // 3
                        if sudo[r][c] == 0 and legal_r[r][number] and legal_c[c][number] and legal_b[b][number]:
                            if same_number:
                                same_number = False
                                break
                            sign_r = r
                            sign_c = c
                            sign_b = b
                            same_number = True
                    if same_number:
                        key = True
                        same_number = False
                        sudo[sign_r][sign_c] = number
                        legal_r[sign_r][number] = False
                        legal_c[sign_c][number] = False
                        legal_b[sign_b][number] = False
                    for c in range(9):
                        b = 3 * (c // 3) + r // 3
                        if sudo[c][r] == 0 and legal_r[c][number] and legal_c[r][number] and legal_b[b][number]:
                            if same_number:
                                same_number = False
                                break
                            sign_r = c
                            sign_c = r
                            sign_b = b
                            same_number = True
                    if same_number:
                        key = True
                        same_number = False
                        sudo[sign_r][sign_c] = number
                        legal_r[sign_r][number] = False
                        legal_c[sign_c][number] = False
                        legal_b[sign_b][number] = False

                for blo_r in range(0, 9, 3):
                    for blo_c in range(0, 9, 3):
                        for r in range(blo_r, blo_r + 3):
                            if same_number:
                                for c in range(blo_c, blo_c + 3):
                                    b = 3 * (r // 3) + c // 3
                                    if sudo[r][c] == 0 and \
                                            legal_r[r][number] and legal_c[c][number] and legal_b[b][number]:
                                        if same_number:
                                            same_number = False
                                            break
                                        sign_r = r
                                        sign_c = c
                                        sign_b = b
                                        same_number = True
                        if same_number:
                            key = True
                            same_number = False
                            sudo[sign_r][sign_c] = number
                            legal_r[sign_r][number] = False
                            legal_c[sign_c][number] = False
                            legal_b[sign_b][number] = False
            for r in range(9):
                for c in range(9):
                    if sudo[r][c] == 0:
                        b = 3 * (r // 3) + c // 3
                        for number in range(1, 10):
                            if legal_r[r][number] and legal_c[c][number] and legal_b[b][number]:
                                if same_number:
                                    same_number = False
                                    break
                                sign_number = number
                                same_number = True
                        if same_number:
                            key = True
                            same_number = False
                            sudo[r][c] = sign_number
                            legal_r[r][sign_number] = False
                            legal_c[c][sign_number] = False
                            legal_b[b][sign_number] = False

    def get_cache():
        keys = [[-1, -1, -1]]
        values = [[0, 0, 0]]
        for r in range(9):
            for c in range(9):
                if sudo[r][c] == 0:
                    b = 3 * (r // 3) + c // 3
                    keys.append([r, c, b])
                    values.append([number for number in range(1, 10)
                                   if legal_r[r][number] and legal_c[c][number] and legal_b[b][number]])
        return keys, values

    # ———————————————————循环函数———————————————————
    def solve():
        coordinate = len(cache_keys) - 1
        cache_times = [0 for _ in range(len(cache_keys))]
        while coordinate != 0:
            row, col, blo = cache_keys[coordinate]
            for value in cache_values[coordinate][cache_times[coordinate]:]:
                if legal_r[row][value] and legal_c[col][value] and legal_b[blo][value]:
                    legal_r[row][value] = False
                    legal_c[col][value] = False
                    legal_b[blo][value] = False
                    sudo[row][col] = value
                    cache_times[coordinate] = cache_values[coordinate].index(value) + 1
                    coordinate -= 1
                    break
            else:
                cache_times[coordinate] = 0
                coordinate += 1
                row, col, blo = cache_keys[coordinate]
                number = sudo[row][col]
                legal_r[row][number] = True
                legal_c[col][number] = True
                legal_b[blo][number] = True

    time_start = time.time()
    legal_r = [[True for _ in range(10)] for _ in range(9)]
    legal_c = [[True for _ in range(10)] for _ in range(9)]
    legal_b = [[True for _ in range(10)] for _ in range(9)]
    if not check():
        return False
    fill()
    cache_keys, cache_values = get_cache()
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

    # sudo_demo = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
    #              [0, 0, 0, 0, 0, 3, 0, 8, 5],
    #              [0, 0, 1, 0, 2, 0, 0, 0, 0],
    #              [0, 0, 0, 5, 0, 7, 0, 0, 0],
    #              [0, 0, 4, 0, 0, 0, 1, 0, 0],
    #              [0, 9, 0, 0, 0, 0, 0, 0, 0],
    #              [5, 0, 0, 0, 0, 0, 0, 7, 3],
    #              [0, 0, 2, 0, 1, 0, 0, 0, 0],
    #              [0, 0, 0, 0, 4, 0, 0, 0, 9]]

    # sudo_demo = [[1, 0, 0, 4, 0, 0, 8, 0, 0],
    #              [0, 4, 0, 0, 3, 0, 0, 0, 9],
    #              [0, 0, 9, 0, 0, 6, 0, 5, 0],
    #              [0, 5, 0, 3, 0, 0, 0, 0, 0],
    #              [0, 0, 0, 0, 0, 1, 6, 0, 0],
    #              [0, 0, 0, 0, 7, 0, 0, 0, 2],
    #              [0, 0, 4, 0, 1, 0, 9, 0, 0],
    #              [7, 0, 0, 8, 0, 0, 0, 0, 4],
    #              [0, 2, 0, 0, 0, 4, 0, 8, 0]]

    # sudo_demo = [[0, 0, 0, 0, 0, 3, 0, 1, 7],
    #              [0, 1, 5, 0, 0, 9, 0, 0, 8],
    #              [0, 6, 0, 0, 0, 0, 0, 0, 0],
    #              [1, 0, 0, 0, 0, 7, 0, 0, 0],
    #              [0, 0, 9, 0, 0, 0, 2, 0, 0],
    #              [0, 0, 0, 5, 0, 0, 0, 0, 4],
    #              [0, 0, 0, 0, 0, 0, 0, 2, 0],
    #              [5, 0, 0, 6, 0, 0, 3, 4, 0],
    #              [3, 4, 0, 2, 0, 0, 0, 0, 0]]
    print(sudo_solve(sudo_demo))
