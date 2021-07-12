import numpy as np
import itertools
import collections

example = np.array([
    [0, 0, 1, 9, 0, 0, 0, 0, 8],
    [6, 0, 0, 0, 8, 5, 0, 3, 0],
    [0, 0, 7, 0, 6, 0, 1, 0, 0],
    [0, 3, 4, 0, 9, 0, 0, 0, 0],
    [0, 0, 0, 5, 0, 4, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 4, 2, 0],
    [0, 0, 5, 0, 7, 0, 9, 0, 0],
    [0, 1, 0, 8, 4, 0, 0, 0, 7],
    [7, 0, 0, 0, 0, 9, 2, 0, 0]
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


def find_preemptive_set(list_with_candidate_sets: list):
    """The idea of this function is to receive a list representing a row/col/square with the goal to find preemptive set in this list.

    Args:
        list_with_candidate_sets (list): List representing row/col/square.

    Returns:
        [set]: Preemptive set.
    """
    cands_w_eliminated_empty = [item for item in list_with_candidate_sets if len(item) > 0]
    for possible_pset in cands_w_eliminated_empty:
        number_of_cells = 0
        number_of_cells_needed = len(possible_pset)
        for other_set in cands_w_eliminated_empty:
            if possible_pset.issuperset(other_set): # NOTE: every set is superset of itself
                number_of_cells += 1
        if number_of_cells == number_of_cells_needed:
            print('Preemptive set found {}'.format(possible_pset))
            return possible_pset



def main():
    """
    Description of the algorithm:
        1. Assign candidate sets to every cell in the Sudoku puzzle.
        2. Check for singletons in the candidate sets
        3. 
            a) Fill in every singleton found, then go back to 1, if Sudoku is not complete yet.
            b) Fill in every singleton found, then end, if Sudoku is completed.
            c) No singleton was found, then procceed to 4.
        4. Try to find preemptive set:
            a) Preemptive set found, then procceed to 5.
            b) Preemptive set not found, then procceed to 6.
        5. Apply Occupancy theorem, then go back to 2.
        TODO:
        6. Random choice of number in the candidate set.
        
    """