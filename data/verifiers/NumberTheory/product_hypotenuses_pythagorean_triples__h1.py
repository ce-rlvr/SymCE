import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools
from sympy.ntheory import factorint

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def is_pos_int(x):
    if isinstance(x, bool):
        return False
    if isinstance(x, int):
        return x > 0
    if isinstance(x, float):
        return x.is_integer() and x > 0
    try:
        if isinstance(x, sympy.Integer):
            return x > 0
        if isinstance(x, sympy.Expr) and x.is_integer and x.is_positive:
            return True
    except Exception:
        pass
    return False

def is_sum_of_two_pos_squares(M):
    factors = factorint(M)
    for p, exp in factors.items():
        if p % 4 == 3 and exp % 2 != 0:
            return False
    is_perfect_square = all(exp % 2 == 0 for exp in factors.values())
    if not is_perfect_square:
        return True
    for p in factors:
        if p % 4 == 1:
            return True
    return False

def conditions(witness):
    c_1 = a_2 = b_2 = c_2 = None
    if isinstance(witness, dict):
        c_1 = witness.get('c_1', None)
        a_2 = witness.get('a_2', None)
        b_2 = witness.get('b_2', None)
        c_2 = witness.get('c_2', None)
    elif isinstance(witness, (tuple, list)):
        if len(witness) == 2 and isinstance(witness[0], (tuple, list)) and isinstance(witness[1], (tuple, list)):
            if len(witness[0]) == 3 and len(witness[1]) == 3:
                _, _, c_1 = witness[0]
                a_2, b_2, c_2 = witness[1]
            else:
                return [False, False]
        elif len(witness) == 4:
            c_1, a_2, b_2, c_2 = witness
        elif len(witness) == 6:
            _, _, c_1, a_2, b_2, c_2 = witness
        elif len(witness) == 3:
            a_2, b_2, c_2 = witness
        else:
            return [False, False]
    else:
        return [False, False]

    # H_1: a_2, b_2, and c_2 are positive integers such that a_2^2 + b_2^2 = c_2^2
    try:
        h1 = is_pos_int(a_2) and is_pos_int(b_2) and is_pos_int(c_2) and (a_2**2 + b_2**2 == c_2**2)
    except Exception:
        h1 = False

    # neg_Q: There do NOT exist positive integers A and B such that A^2 + B^2 = (c_1 c_2)^2
    try:
        if c_1 is None or c_2 is None:
            neg_Q = True
        else:
            prod = c_1 * c_2
            target = prod**2
            
            if isinstance(target, int):
                pass
            elif isinstance(target, float):
                if target.is_integer():
                    target = int(target)
                else:
                    target = -1
            else:
                try:
                    target_int = int(target)
                    if target - target_int == 0:
                        target = target_int
                    else:
                        target = -1
                except Exception:
                    target = -1

            if not isinstance(target, int) or target <= 0:
                neg_Q = True
            else:
                found = is_sum_of_two_pos_squares(target)
                neg_Q = not found
    except Exception:
        neg_Q = True

    return [bool(h1), bool(neg_Q)]

CONDITION_LABELS = [
    "H_1: a_2, b_2, and c_2 are positive integers such that a_2^2 + b_2^2 = c_2^2",
    "¬Q: There do not exist positive integers A and B such that A^2 + B^2 = (c_1 c_2)^2"
]

N_HYP = 1
NEG_Q_INDEX = 1