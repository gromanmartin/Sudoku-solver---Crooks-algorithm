import numpy as np
import itertools
import collections

example = np.array([
    [0, 7, 3, 2, 5, 0, 8, 9, 0],
    [8, 0, 1, 0, 0, 9, 0, 0, 0],
    [9, 0, 0, 8, 0, 0, 0, 4, 0],
    [0, 1, 9, 0, 6, 4, 5, 0 ,8],
    [0, 0, 0, 1, 0, 0, 0, 7, 9],
    [0, 3, 4, 0, 0, 8, 0, 6, 0],
    [0, 6, 8, 4, 2, 0, 0, 1, 0],
    [0, 4, 0, 0, 1, 0, 6, 8, 7],
    [1, 0, 0, 0, 0, 0, 0, 5, 4]
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


def find_preemptive_sets(candidate_set_list: list):
    """Given candidate set list (list of sets either in row, column or square), find the preemptive set. Stop after finding the first one.

    Args:
        candidate_set_list (list): List of sets, representing either row, column or square.

    Returns:
        [set]: Preemptive set.
    """
    preemptive_set = set()
    counter = collections.Counter(frozenset(s) for s in candidate_set_list)
    set_counts = [[set(x), len(set(x)), count] for x, count in zip(counter.keys(), counter.values())]
    for el in set_counts:
        if el[1] == el[2] and el[1] > 1:
            preemptive_set = el[0]
            print('Preemptive set {} found!'.format(preemptive_set))
            break
    return preemptive_set


def apply_occupancy_theorem(list_with_preemptive_set: list, preemptive_set: set):
    """Exclude every number of preemptive set from the other sets in the list with preemptive set. It overwrites the original sudoku.

    Args:
        list_with_preemptive_set (list): List(representing row/col/square) containing a preemptive set.
        preemptive_set (set): Preemptive set generated by find_preemptive_sets().
    """
    for idx, cellset in enumerate(list_with_preemptive_set):
        if cellset != preemptive_set:
            list_with_preemptive_set[idx] = cellset - preemptive_set


def fill_in_singletons(sudoku: np.array, sudoku_with_candidates: list):
    """Find single item sets in the sudoku list with candidates. Fill in the values into appropriate cells.

    Args:
        sudoku (np.array): Sudoku to be solved
        sudoku_with_candidates (list): List of sets with candidate numbers for each sets.
    """
    for row in range(9):
        for col in range(9):
            if len(sudoku_with_candidates[row][col]) == 1:
                sudoku[row, col] = next(iter(sudoku_with_candidates[row][col])) 


def main(sudoku_to_solve: np.array):

    def preemptive_in_row():
        preemptive_set_counter = 0
        for row in range(9):
            # I use the assigned candidate sets to find 1 preemptive set
            preemptive_set = find_preemptive_sets(sudoku_with_candidate_sets[row])
            if len(preemptive_set) == 0:
                preemptive_set_counter += 1
            # Once I find the preemptive set, I want to apply the occupancy theorem
            else:
                apply_occupancy_theorem(sudoku_with_candidate_sets[row], preemptive_set)
        # After I apply the occupancy theorem, I want to fill in all singletons, that could have possibly appeared
        # If I had 0 preemptive sets then return False
        if preemptive_set_counter == 9:
            return False
        else:
            fill_in_singletons(example, sudoku_with_candidate_sets)
            return True

    def preemptive_in_col():
        preemptive_set_counter = 0
        for col in range(9):
            # I use the assigned candidate sets to find 1 preemptive set
            col_list = [item[col] for item in sudoku_with_candidate_sets]
            preemptive_set = find_preemptive_sets(col_list)
            if len(preemptive_set) == 0:
                preemptive_set_counter += 1
            # Once I find the preemptive set, I want to apply the occupancy theorem
            else:
                apply_occupancy_theorem(col_list, preemptive_set)
                for idx, _ in enumerate(sudoku_with_candidate_sets):
                    sudoku_with_candidate_sets[idx][col] = col_list[idx]

        # After I apply the occupancy theorem, I want to fill in all singletons, that could have possibly appeared
        # If I had 0 preemptive sets then return False
        if preemptive_set_counter == 9:
            return False
        else:
            fill_in_singletons(example, sudoku_with_candidate_sets)
            return True

    def preemptive_in_square():
        preemptive_set_counter = 0    
        for row_number in range(9):
            for col_number in range(9):
                r = int(row_number/3)
                c = int(col_number/3) 
                square_array = np.array([element for row in sudoku_with_candidate_sets[r*3:r*3+3] for element in row[c*3:c*3+3]])
                preemptive_set = find_preemptive_sets(square_array)
                if len(preemptive_set) == 0:
                    preemptive_set_counter += 1
                else:
                    apply_occupancy_theorem(square_array, preemptive_set)   
                    for idx, _ in enumerate(sudoku_with_candidate_sets):
                        sudoku_with_candidate_sets[row_number][col_number] = square_array[idx]
        # After I apply the occupancy theorem, I want to fill in all singletons, that could have possibly appeared
        # If I had 0 preemptive sets then return False
        if preemptive_set_counter == 9:
            return False
        else:
            fill_in_singletons(example, sudoku_with_candidate_sets)
            return True

    print(example)
    # First of all, I assign every allowed number to every cell in the sudoku
    sudoku_with_candidate_sets = assign_candidate_sets_to_cells(sudoku_to_solve)
    # Secondly, I have to check if there are any singletons to get some quick filled spots
    fill_in_singletons(example, sudoku_with_candidate_sets)

    # Then, I use the assigned candidate sets to find 1 preemptive set
    # - 1. Check lines
    # - 2. Check columns
    # - 3. Check squares
    preemptive_set_not_empty = True
    while preemptive_set_not_empty:
        # 1. rows
        preemptive_set_not_empty = preemptive_in_row()
        print(example)
        # 2. cols
        # preemptive_set_not_empty = preemptive_in_col()
        # print(example)
        # 3. squares
        # preemptive_set_not_empty = preemptive_in_square()
        # print(example)


if __name__ == "__main__":
    main(example)
# a = assign_candidate_sets_to_cells(example)
# print(a)
# b = find_preemptive_sets(a[1])
# apply_occupancy_theorem(a[1], b)
# print(a[1])