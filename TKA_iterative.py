"""
Below code estimates the laziest way to dial n-digit number on a standard 
push button telephone (with 12 keys) using two fingers.
Assumptions behind:
    - Fingers always start out on the * (left finger) and # (right finger) buttons
    - Effort required to move finger from one button to another is equal to the Euclidean distance between them

The function examines every possible solution in order to find the best possible one.
It return a tuple where:
    - The first element is the smallest Euclidean distance found for a given number
    - The second element is a list of tuples where each tuple represents finger positions after dialng each number digit

The following optimizations were applied in order to remove redundancy and reduce running time:
    - Once the distance between two given buttons is calculated it's stored in the container for further use
    - If distance passed during given iteration is already higher or equal to the previously calculated one
      it moves immediately to the next one. Moreover all other iterations that start from the same finger combination
      are immediately considered not optimal and not even examined
    - If during given iteration two fingers land on the same button, it's immediately considered a non-optimal one.
      As previously, all iterations that start from the same finger combination are considered not optimal and aren't examined.
"""

import numpy as np
from math import sqrt, inf
from itertools import product, permutations


def compute_laziest_path(telephone_number: str) -> tuple:
    """Computes the laziest path of two fingers moving on the telephone keypad"""

    def calculate_distance(p1: tuple, p2: tuple) -> float:
        """Calculates Euclidean distance between two points"""
        return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def get_position_values(keypad: np.array, p1: tuple, p2: tuple) -> tuple:
        """Returns values for the passed coordinates within the 2d numpy array"""
        return (keypad[p1[0]][p1[1]], keypad[p2[0]][p2[1]])

    def get_coordinates(keypad: np.array, value: str) -> tuple:
        """Returns 2d numpy array's coordinates for the passed value"""
        return (np.where(keypad == value)[0][0], np.where(keypad == value)[1][0])

    def is_wrong(container: dict, lookup_val: tuple) -> bool:
        """Check if given permutation is known to be not optimal"""
        for key, values in container.items():
            if lookup_val[:key] in values:
                return True
        return False

    # Initialize the phone keypad as numpy 2d array
    keypad = np.array([
        ['1', '2', '3'],
        ['4', '5', '6'],
        ['7', '8', '9'],
        ['*', '0', '#'],
    ])

    # Total final distance variable initialized to infinity
    total_dist = inf

    # Container for all the previously calculated distances 
    calculated_dists = {}

    # Initial finger positions both as values and coordinates
    initial_values = ('*', '#')
    initial_pos_l = get_coordinates(keypad, initial_values[0])
    initial_pos_r = get_coordinates(keypad, initial_values[1])

    # Container for all the finger positions, necessary for the output
    all_positions = []
    
    # Container for all known to be wrong permutation parts
    wrong_finger_permutations = {}

    # Create an iterable object of all possible finger moves 
    prod = product('LR', repeat=len(telephone_number))

    # Main loop through all the finger moves
    for perm in prod:

        # Check if the currently iterated permutation is known to be wrong
        if is_wrong(wrong_finger_permutations, perm):
            continue

        # Starting finger positions for each run are always the same: * and #
        start_pos_l = initial_pos_l
        start_pos_r = initial_pos_r

        # Variables to hold iteration output
        temp_positions = []
        temp_dist = 0
        # Temporary container for the finger positions
        fingers = []
        # Flag which tracks if the current finger movement is optimal
        optimal = True

        for i in range(len(perm)):

            # Add finger position to the temporary container
            finger = perm[i]
            fingers.append(finger)

            # Digit value checked in this iteration
            value = telephone_number[i]
            # Coordinates of the given digit
            end_pos = get_coordinates(keypad, value)

            # Movement of the left finger
            if finger == 'L':
                # --- Logic assessing if given distance was already calculated or not
                # --- If yes, it grabs the distance from the container instead of calculating it over again
                pos_values = get_position_values(keypad, start_pos_l, end_pos)

                if pos_values in calculated_dists.keys():
                    dist = calculated_dists[pos_values]
                else:
                    dist = calculate_distance(start_pos_l, end_pos) if start_pos_l != start_pos_r else 0
                    if dist != 0:
                        for x in permutations(pos_values):
                            calculated_dists[x] = dist
                            # --- End of distance calculating logic

                # Save the iteration output in the temporary containers
                temp_dist += dist
                start_pos_l = end_pos

            # Movement of the right finger
            elif finger == 'R':
                # --- Logic assessing if given distance was already calculated or not
                # --- If yes, it grabs the distance from the container instead of calculating it over again
                pos_values = get_position_values(keypad, start_pos_r, end_pos)

                if pos_values in calculated_dists.keys():
                    dist = calculated_dists[pos_values]
                else:
                    dist = calculate_distance(start_pos_r, end_pos) if start_pos_l != start_pos_r else 0
                    if dist != 0:
                        for x in permutations(pos_values):
                            calculated_dists[x] = dist
                # --- End of distance calculating logic

                # Save the iteration output in the temporary containers
                temp_dist += dist
                start_pos_r = end_pos

            # If both fingers are on the same button break the loop as such behaviour is 
            # already not the most optimal one
            if start_pos_l == start_pos_r:
                optimal = False
                if i + 1 in wrong_finger_permutations.keys():
                    wrong_finger_permutations[i + 1].append(tuple(fingers))
                else:
                    wrong_finger_permutations[i + 1] = [tuple(fingers)]
                break

            # If the temp distance is already higher than the previously calculated one, break the loop
            if temp_dist >= total_dist:
                optimal = False
                if i + 1 in wrong_finger_permutations.keys():
                    wrong_finger_permutations[i + 1].append(tuple(fingers))
                else:
                    wrong_finger_permutations[i + 1] = [tuple(fingers)]
                break

            # Append the finger positions to the temporary container
            temp_positions.append(get_position_values(keypad, start_pos_l, start_pos_r))

        # If given movement is considered optimal save the output to permanent containers
        if optimal:
            total_dist = temp_dist
            all_positions = temp_positions

    # Insert starting finger positions at the beginning of positions list
    all_positions.insert(0, initial_values)
    out = (total_dist, all_positions)
    return out