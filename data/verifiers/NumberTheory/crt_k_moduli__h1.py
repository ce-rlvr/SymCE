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

from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        # Witness can be a tuple of two lists (a, m) or a list of pairs [(a1, m1), ...]
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], (list, tuple)) and isinstance(witness[1], (list, tuple)):
            a, m = witness
        elif isinstance(witness, (list, tuple)) and all(isinstance(x, (list, tuple)) and len(x) == 2 for x in witness):
            a = [x[0] for x in witness]
            m = [x[1] for x in witness]
        else:
            a, m = None, None
            
        if a is None or m is None:
            h1 = False
        elif len(a) != len(m) or len(a) == 0:
            h1 = False
        else:
            h1 = all(type(x) is int for x in a) and all(type(x) is int for x in m)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            M = 1
            for mi in m:
                M *= mi
            
            M_abs = abs(M)
            if M_abs > 100000:
                # Prevent timeout for excessively large moduli
                neg_q = False
            elif M_abs == 0:
                # If M = 0, we are looking for a unique solution in Z
                fixed_x = None
                possible = True
                for ai, mi in zip(a, m):
                    if mi == 0:
                        if fixed_x is None:
                            fixed_x = ai
                        elif fixed_x != ai:
                            possible = False
                if not possible:
                    neg_q = True
                else:
                    is_sol = True
                    for ai, mi in zip(a, m):
                        if mi != 0 and (fixed_x - ai) % mi != 0:
                            is_sol = False
                    neg_q = not is_sol
            else:
                solutions = 0
                for x in range(M_abs):
                    is_sol = True
                    for ai, mi in zip(a, m):
                        if (x - ai) % mi != 0:
                            is_sol = False
                            break
                    if is_sol:
                        solutions += 1
                        if solutions > 1:
                            break
                neg_q = (solutions != 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a_i and m_i are integers for 1 <= i <= k",
    "¬Q: The system does not have a unique solution modulo M"
]

N_HYP = 1
NEG_Q_INDEX = 1