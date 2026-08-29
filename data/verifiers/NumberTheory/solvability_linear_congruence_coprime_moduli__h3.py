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

# Top-level setup
# (No specific named objects required for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 4:
            return [False, False, False]
        a, b, m, n = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(a, (int, sympy.Integer)) and \
             isinstance(b, (int, sympy.Integer)) and \
             isinstance(m, (int, sympy.Integer)) and \
             isinstance(n, (int, sympy.Integer))
    except Exception:
        h1 = False

    try:
        h2 = h1 and (int(m) > 0) and (int(n) > 0)
    except Exception:
        h2 = False

    try:
        def has_solution(A, B, M):
            return int(B) % math.gcd(int(A), int(M)) == 0
        
        P = has_solution(a, b, m * n)
        Q = has_solution(a, b, m) and has_solution(a, b, n)
        neg_q = (P != Q)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, m, n are integers",
    "H_2: m > 0 and n > 0",
    "¬Q: ax = b (mod mn) has a solution XOR (ax = b (mod m) and ax = b (mod n) have solutions)"
]

N_HYP = 2
NEG_Q_INDEX = 2