"""
This is the recurrent version of the Telephone Keypad Algorithm (TKA).
As it's much faster than the iterative approach I consider it a final answer 
for the technical exercise. 

Possible additional optimizations not implemented below:
    - Using C-Extensions (Cython)
    - Using bitarray package to store coordinates as well
    
Time Complexity:
    Worst: O(2^n)
    Best: Ω(n)
    
Space complexity:
   Θ(k^2 + n) 
"""

from bitarray import bitarray
from math import sqrt, inf


def compute_laziest_path(telephone_number: str) -> tuple:
   
    def _init_coords() -> dict:
        return {'1': (0, 0), '2': (1, 0), '3': (2, 0),
                '4': (0, 1), '5': (1, 1), '6': (2, 1),
                '7': (0, 2), '8': (1, 2), '9': (2, 2),
                '*': (0, 3), '0': (1, 3), '#': (2, 3)}

    _coords: dict = _init_coords()
    _distances: dict = dict()

    def _get_distance(k1: str, k2: str) -> float:
        k = (k1, k2) if k1 < k2 else (k2, k1)
        v = _distances.get(k)
        if not v:
            v = _calc_distance(k1, k2)
            if v != 0: 
                _distances[k] = v
        return v

    def _calc_distance(k1: str, k2: str) -> float:
        if k1 == k2:
            return 0.0
        p1 = _coords[k1]
        p2 = _coords[k2]
        return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    _number_length: int = len(telephone_number)
    _best_score: float = inf
    _best_path: bitarray = None

    def _recursive_search(path: bitarray, left_finger: str, right_finger: str, score: float, pos: int) -> None:
        nonlocal _best_score, _best_path, _number_length

        if pos == _number_length:
            if score < _best_score:
                _best_score = score
                _best_path = path.copy()
            return

        # Try advance the left finger
        new_left_finger = telephone_number[pos]
        
        # Not proceed if two fingers are on the same key (not optimal)
        if new_left_finger != right_finger:
            new_score = score + _get_distance(left_finger, new_left_finger)
            
            if new_score < _best_score:
                path.append(0)
                _recursive_search(path, new_left_finger, right_finger, new_score, pos+1)
                path.pop()

        # Try advance the right finger
        new_right_finger = telephone_number[pos]
        
        # Not proceed if two fingers are on the same key (not optimal)
        if new_right_finger != left_finger:  
            new_score = score + _get_distance(right_finger, new_right_finger)
            
            if new_score < _best_score:
                path.append(1)
                _recursive_search(path, left_finger, new_right_finger, new_score, pos+1)
                path.pop()

    def _get_result() -> tuple:
        left_finger = '*'
        right_finger = '#'

        moves = [(left_finger, right_finger)]
        pos = 0

        for b in _best_path:
            if b == 0:
                left_finger = telephone_number[pos]
            else:
                right_finger = telephone_number[pos]
            moves.append((left_finger, right_finger))
            pos += 1

        return _best_score, moves

    _recursive_search(bitarray(), '*', '#', 0.0, 0)
    return _get_result()
