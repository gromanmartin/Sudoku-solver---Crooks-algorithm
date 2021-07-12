from sudokusolver import find_preemptive_sets
import numpy as np
import itertools
import collections

example = np.array([
    [0, 3, 9, 5, 0, 0, 0, 0, 0],
    [0, 0, 1, 8, 0, 9, 0, 7, 0],
    [0, 0, 0, 0, 1, 0, 9, 0, 4],
    [1, 0, 0, 4, 0, 0, 0, 0, 3],
    [0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 7, 0, 0, 0, 8, 6, 0], 
    [0, 0, 6, 7, 0, 8, 2, 0, 0], 
    [0, 1, 0, 0, 9, 0, 0, 0, 5],
    [0, 0, 0, 0, 0, 1, 0, 0, 8]
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
        [set]: Preemptive set. Returns first pset it founds.
    """
    for possible_pset in list_with_candidate_sets:
        indexes = []
        number_of_cells = 0
        number_of_cells_needed = len(possible_pset)
        max_number_of_cells = max([len(x) for x in list_with_candidate_sets])
        for idx, other_set in enumerate(list_with_candidate_sets):
            if len(possible_pset) > 1 and len(other_set) > 0:
                if possible_pset.issuperset(other_set):
                    number_of_cells += 1
                    indexes.append(idx)
        # We dont want empty sets, 1 element sets and sets containing every possible number
        if number_of_cells == number_of_cells_needed and number_of_cells > 1 and number_of_cells < max_number_of_cells:
            print('Preemptive set found {} with index {}'.format(possible_pset, indexes))
            return possible_pset, indexes
    print('Preemptive set not found')
    return None, None


def update_cand_sets_w_occ_theorem(list_of_lists_with_candidate_sets: list):
    def scan_rows():
        """
        Checks every row in Sudoku and tries to find preemptive set. If found applies the occupancy theorem.
        """
        print('Scanning rows...')
        for row in list_of_lists_with_candidate_sets:
            pset, pst_indexes = find_preemptive_set(row)
            if pset != None and pst_indexes != None:
                row = apply_occupancy_theorem(row, pst_indexes, pset)
                for idx in range(9):
                    list_of_lists_with_candidate_sets[row][idx] = row[idx]

    def scan_cols():
        """
        Checks every column in Sudoku and tries to find preemptive set. If found applies the occupancy theorem.
        """
        for col in range(9):
            col_list = [item[col] for item in list_of_lists_with_candidate_sets]
            pset, pst_indexes = find_preemptive_set(col_list)
            if pset != None and pst_indexes != None:
                col_list = apply_occupancy_theorem(col_list, pst_indexes, pset)
                
        pass

    def scan_squares():
        """
        Checks every square in Sudoku and tries to find preemptive set. If found applies the occupancy theorem.
        """
        print('Scanning squares...')
        for r in range(3):
            for c in range(3):
                square_list = [element for row in list_of_lists_with_candidate_sets[r*3:r*3+3] for element in row[c*3:c*3+3]]
                pset, pst_indexes = find_preemptive_set(square_list)
                if pset != None and pst_indexes != None:
                    square_list = apply_occupancy_theorem(square_list, pst_indexes, pset)
                    idx = 0 # index used to select elements from square_list
                    for row in range(r*3, r*3+3):
                        for col in range(c*3, c*3+3):
                            list_of_lists_with_candidate_sets[row][col] = square_list[idx]
                            idx += 1
    scan_rows()
    scan_cols()
    scan_squares()
    return list_of_lists_with_candidate_sets


def apply_occupancy_theorem(list_of_cand_sets: list, indexes_of_preemptive_set: list, preemptive_set: set):
    """Applies the occupancy theorem to the selected list

    Args:
        list_of_cand_sets (list): List of candidates sets for the OT to be applied to.
        indexes_of_preemptive_set (list): Indexes of cells, which contain subsets of preemptive set.
        preemptive_set (set): The preemptive set.

    Returns:
        [list]: Returns the same list, but with applied theorem. Some of the numbers will be deleted from sets not included in preemptive set.
    """
    for idx, item in enumerate(list_of_cand_sets):
        if idx not in indexes_of_preemptive_set:
            list_of_cand_sets[idx] = set(item) - preemptive_set
    return list_of_cand_sets




def main():
    """
    Description of the algorithm:
        1. Assign candidate sets to every cell in the Sudoku puzzle.
        2. Check for singletons in the candidate sets
        3. Try to find singleton:
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
    cands = assign_candidate_sets_to_cells(example)
    print(cands)
    cands2 = update_cand_sets_w_occ_theorem(cands)
    print(cands)

if __name__ == '__main__':
    main()