from random import sample


def generate_sudoku():
    base = 3
    side = base * base

    def pattern(r, c):
        return (base * (r % base) + r // base + c) % side

    def shuffle_list(lst):
        return sample(lst, len(lst))

    rBase = [0, 1, 2]  #rows
    rows = []
    shuffled_groups = shuffle_list(rBase)

    for g in shuffled_groups:
        inside_group = shuffle_list(rBase)
        for r in inside_group:
            rows.append(g * base + r)

    cols = [] #columns
    shuffled_groups = shuffle_list(rBase)

    for g in shuffled_groups:
        inside_group = shuffle_list(rBase)
        for c in inside_group:
            cols.append(g * base + c)

    numbers = shuffle_list([1,2,3,4,5,6,7,8,9])

    board = []
    for r in rows:
        row_list = []
        for c in cols:
            value = numbers[pattern(r, c)]
            row_list.append(value)
        board.append(row_list)

    return board



#remove numbers
def remove_easy(board):
    return remove_numbers(board, 2)

def remove_medium(board):
    return remove_numbers(board, 3)

def remove_hard(board):
    return remove_numbers(board, 4)

def remove_numbers(board, count_per_row):
    new_board = [row[:] for row in board]  
    for r in range(9):
        cols_to_remove = sample(range(9), count_per_row)
        for c in cols_to_remove:
            new_board[r][c] = 0

    return new_board
