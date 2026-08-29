import math
import itertools
import functools
import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3

def conditions(witness):
    try:
        m, n, A, B = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: m and n are positive integers
    try:
        h1 = isinstance(m, (int, sympy.Integer)) and isinstance(n, (int, sympy.Integer)) and m > 0 and n > 0
    except Exception:
        h1 = False

    # H_2: gcd(m, n) = 1
    try:
        h2 = math.gcd(int(m), int(n)) == 1
    except Exception:
        h2 = False

    # H_3: B is a complete residue system modulo n
    try:
        h3 = False
        if isinstance(B, (list, set, tuple)) and all(isinstance(b, (int, sympy.Integer)) for b in B):
            if len(B) == n:
                residues = set(int(b) % int(n) for b in B)
                if len(residues) == n:
                    h3 = True
    except Exception:
        h3 = False

    # neg_Q: The set {an + bm | a in A, b in B} is not a complete residue system modulo mn
    try:
        neg_q = False
        if isinstance(A, (list, set, tuple)) and all(isinstance(a, (int, sympy.Integer)) for a in A):
            S = set()
            m_int = int(m)
            n_int = int(n)
            for a in A:
                for b in B:
                    S.add((int(a) * n_int + int(b) * m_int) % (m_int * n_int))
            if len(S) != m_int * n_int:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: m and n are positive integers",
    "H_2: gcd(m, n) = 1",
    "H_3: B is a complete residue system modulo n",
    "¬Q: The set {an + bm | a in A, b in B} is not a complete residue system modulo mn"
]

N_HYP = 3
NEG_Q_INDEX = 3