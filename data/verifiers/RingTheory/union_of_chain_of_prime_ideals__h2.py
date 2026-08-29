import sympy
from sympy.abc import x
import math
import itertools

# Standard bindings that a witness might use
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6

def _is_ideal(I, n):
    if not I: 
        return False
    if not all(isinstance(e, int) and 0 <= e < n for e in I): 
        return False
    # Check closure under addition
    for a in I:
        for b in I:
            if (a + b) % n not in I: 
                return False
    # Check closure under external multiplication
    for a in I:
        for r in range(n):
            if (r * a) % n not in I: 
                return False
    return True

def _is_prime_ideal(I, n):
    if not _is_ideal(I, n): 
        return False
    # Prime ideal must be proper
    if len(I) == n: 
        return False
    # Check prime condition: ab in I => a in I or b in I
    for a in range(n):
        for b in range(n):
            if (a * b) % n in I:
                if a not in I and b not in I:
                    return False
    return True

def conditions(witness):
    """
    Expects witness to be a tuple: (n, C, U)
    where:
      - n is an integer >= 2 representing the ring Z/nZ
      - C is a list of subsets (lists/sets) of Z/nZ
      - U is a subset (list/set) of Z/nZ
    """
    try:
        n, C, U = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: R is a commutative ring with identity
    try:
        # We restrict n to a reasonable size to ensure fast verification
        h1_ok = isinstance(n, int) and 2 <= n <= 100
    except Exception:
        h1_ok = False

    # H_2: C is totally ordered by set inclusion
    try:
        C_sets = [set(s) for s in C]
        h2_ok = True
        for A in C_sets:
            for B in C_sets:
                if not (A.issubset(B) or B.issubset(A)):
                    h2_ok = False
                    break
            if not h2_ok:
                break
    except Exception:
        h2_ok = False

    # H_3: U is the union of all prime ideals in C
    try:
        prime_ideals_in_C = [set(s) for s in C if _is_prime_ideal(set(s), n)]
        expected_U = set()
        for pi in prime_ideals_in_C:
            expected_U.update(pi)
        
        h3_ok = (set(U) == expected_U)
    except Exception:
        h3_ok = False

    # ¬Q: U is not a prime ideal of R
    try:
        neg_q_ok = not _is_prime_ideal(set(U), n)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: C is totally ordered by set inclusion",
    "H_3: U is the union of all prime ideals in C",
    "¬Q: U is not a prime ideal of R"
]

N_HYP = 3
NEG_Q_INDEX = 3