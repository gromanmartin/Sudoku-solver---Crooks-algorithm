import numpy as np
import itertools
import collections

example = np.array([
    [2, 9, 5, 7, 0, 0, 8, 6, 0],
    [0, 3, 1, 8, 6, 5, 0, 2, 0],
    [8, 0, 6, 0, 0, 0, 0, 0, 0],
    [0, 0, 7, 0, 5, 0, 0, 0, 6],
    [0, 0, 0, 3, 8, 7, 0, 0, 0],
    [5, 0, 0, 0, 1, 6, 7, 0, 0],
    [0, 0, 0, 5, 0, 0, 1, 0, 9],
    [0, 2, 0, 6, 0, 0, 3, 5, 0],
    [0, 5, 4, 0, 0, 8, 6, 7, 2],
])

def determine_possible_numbers(arr: np.array):
    """Determine all possible numbers, which could be filled in empty spots according to Sudoku rules.

    Args:
        arr (np.array): Array to check.

    Returns:
        [set]: Set of candidate numbers to be filled in the blank spots.
    """
    b = [x for x in range(10)]
    arr = set(arr)
    poss_numbers = (arr ^ set(b))
    return poss_numbers

def generate_candidates(sudoku:np.array, row_number: int, col_number: int):
    """Generate candidate numbers as a intersection among numbers possible to be filled in according to Sudoku rules for rows, columns and squares.

    Args:
        sudoku (np.array): Sudoku to be solved.
        row_number (int): Number of the row.
        col_number (int): Number of the column.

    Returns:
        [set]: Set of generated candidate numbers. Intersected of 3 sets.
    """
    def check_row():
        row_arr = sudoku[row_number]
        row_possible_numbers = determine_possible_numbers(row_arr)
        return row_possible_numbers

    def check_column():
        col_arr = sudoku[:, col_number]
        col_possible_numbers = determine_possible_numbers(col_arr)
        return col_possible_numbers

    def check_square():
        r = int(row_number/3)
        c = int(col_number/3) 
        square_array = np.array([element for row in sudoku[r*3:r*3+3] for element in row[c*3:c*3+3]])
        square_possible_numbers = determine_possible_numbers(square_array)
        return square_possible_numbers

    row_possible_numbers = check_row()
    col_possible_numbers = check_column()
    square_possible_numbers = check_square()
    possible_numbers = row_possible_numbers.intersection(col_possible_numbers, square_possible_numbers)
    return possible_numbers


def assign_candidate_sets_to_cells(sudoku: np.array):
    """Create a list with sets of candidate numbers assigned to corresponding cells.

    Args:
        sudoku (np.array): Sudoku to be solved.

    Returns:
        [list]: List of candidate sets for each cell.
    """
    set_list = [[set() for _ in range(9)] for _ in range(9)]
    for row in range(9):
        for col in range(9):
            if sudoku[row, col] == 0:
                set_list[row][col] = generate_candidates(sudoku, row, col)
    return set_list


def compare_sets(l:list, n: int, *args: set):
    combs = itertools.combinations(l, n)



def find_preemptive_sets(candidate_set_list: list):
    preemptive_set_list_row = []
    def find_in_rows():
        for row in candidate_set_list:
            for a, b in itertools.combinations(row, 2):
                if a == b:
                    preemptive_set_list_row.append(a)
                else:
                    preemptive_set_list_row.append(set())
    find_in_rows()
    return preemptive_set_list_row

    # def find_singleton():
    #     candidates_intersection = row_candidates.intersection(col_candidates, square_candidates)
    #     if len(candidates_intersection) == 0:
    #         print('No solution possible.')
    #     elif len(candidates_intersection) == 1:
    #         sudoku[row_number, col_number] = next(iter(candidates_intersection))
    #     else:
    #         pass
    #     pass


a = assign_candidate_sets_to_cells(example)
print(a[0])