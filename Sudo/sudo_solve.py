import time


def sudo(sudo_sudo):
    def find_empty():
        for _ in range(9):
            if 0 in sudo_sudo[_]:
                return _, sudo_sudo[_].index(0)

    def allowed_values_isvalid(num, row, col):
        if num in sudo_sudo[row]:
            return False
        for _ in range(9):
            if num == sudo_sudo[_][col]:
                return False

        row_block = 3 * (row // 3)
        col_block = 3 * (col // 3)
        for j in range(row_block, row_block + 3):
            if num in sudo_sudo[j][col_block:col_block + 3]:
                return False

        return True

    def allowed_values(row, col):
        numbers_list = list()

        for number in range(1, 10):
            if allowed_values_isvalid(number, row, col):
                numbers_list.append(number)
        return numbers_list

    def check():
        for y_check in range(9):
            for x_check in range(9):
                t = sudo_sudo[y_check][x_check]
                if t:
                    sudo_sudo[y_check][x_check] = 0
                    if t in allowed_values(y_check, x_check):
                        sudo_sudo[y_check][x_check] = t
                    else:
                        return False
        return True

    def get_cache():
        cache_get = {}
        for y_cache in range(9):
            for x_cache in range(9):
                if not sudo_sudo[y_cache][x_cache]:
                    cache_get[(y_cache, x_cache)] = allowed_values(y_cache, x_cache)
        return cache_get

    def is_valid(num, row, col):
        if num in sudo_sudo[row]:
            return False
        row_block = 3 * (row // 3)
        col_block = 3 * (col // 3)

        for isvalid_i in range(row_block):
            if num == sudo_sudo[isvalid_i][col]:
                return False
        for isvalid_j in range(row_block, row):
            if num in sudo_sudo[isvalid_j][col_block:col_block + 3]:
                return False

        return True

    def fill():
        key = True
        same_number = False
        sign_r, sign_c = 0, 0
        sign_number = 0
        while key:
            key = False
            for number in range(1, 10):
                for r in range(9):
                    for c in range(9):
                        if not sudo_sudo[r][c] and allowed_values_isvalid(number, r, c):
                            if same_number:
                                same_number = False
                                break
                            sign_r = r
                            sign_c = c
                            same_number = True
                    if same_number:
                        key = True
                        same_number = False
                        sudo_sudo[sign_r][sign_c] = number
                    for j in range(9):
                        if not sudo_sudo[j][r] and allowed_values_isvalid(number, j, r):
                            if same_number:
                                same_number = False
                                break
                            sign_r = j
                            sign_c = r
                            same_number = True
                    if same_number:
                        key = True
                        same_number = False
                        sudo_sudo[sign_r][sign_c] = number

                for r in range(0, 9, 3):
                    for c in range(0, 9, 3):
                        for y in range(r, r + 3):
                            if not sudo_sudo[r][c] and allowed_values_isvalid(number, r, c):
                                if same_number:
                                    same_number = False
                                    break
                                sign_r = y
                                sign_c = c
                                same_number = True
                            if not sudo_sudo[r][c + 1] and allowed_values_isvalid(number, r, c + 1):
                                if same_number:
                                    same_number = False
                                    break
                                sign_r = y
                                sign_c = c + 1
                                same_number = True
                            if not sudo_sudo[r][c + 2] and allowed_values_isvalid(number, r, c + 2):
                                if same_number:
                                    same_number = False
                                    break
                                sign_r = y
                                sign_c = c + 2
                                same_number = True
                        if same_number:
                            key = True
                            same_number = False
                            sudo_sudo[sign_r][sign_c] = number
            for r in range(9):
                for c in range(9):
                    if not sudo_sudo[r][c]:
                        for number_only in range(1, 10):
                            if allowed_values_isvalid(number_only, r, c):
                                if same_number:
                                    sign_number = number_only
                                    same_number = False
                                    break
                                same_number = True
                        if same_number:
                            key = True
                            same_number = False
                            sudo_sudo[r][c] = sign_number

    # ————————————————迭代函数———————————————————————
    def solve():
        blank = find_empty()
        if not blank:
            return True
        else:
            row, col = blank

        for i in cache[(row, col)]:
            if is_valid(i, row, col):
                sudo_sudo[row][col] = i

                if solve():
                    return True
                sudo_sudo[row][col] = 0
        return False

    if not check():
        return False
    time_start = time.time()
    cache = get_cache()
    fill()
    solve()
    time_end = time.time()
    return sudo_sudo, time_end - time_start


# ————————————————构建数独————————————————
"""
sudo = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 6, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 9, 0, 2, 0, 0],
        [0, 5, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 4, 5, 7, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 3, 0],
        [0, 0, 1, 0, 0, 0, 0, 6, 8],
        [0, 0, 8, 5, 0, 0, 0, 1, 0],
        [0, 9, 0, 0, 0, 0, 4, 0, 0]]
sudo = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 8, 5],
        [0, 0, 1, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 5, 0, 7, 0, 0, 0],
        [0, 0, 4, 0, 0, 0, 1, 0, 0],
        [0, 9, 0, 0, 0, 0, 0, 0, 0],
        [5, 0, 0, 0, 0, 0, 0, 7, 3],
        [0, 0, 2, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 9]]
"""
