import math
import itertools
import functools
import sympy
from sympy.abc import x, y, z

# Top-level setup for common finite rings Z_n
# If a witness expression references Z6, it will evaluate to the integer 6,
# representing the ring Z/6Z.
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z7 = 7
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample to the conjecture:
    "In any ring R, if p is a non-zero, non-unit prime element, then p is irreducible."
    
    The witness is expected to be a tuple (n, p) representing the ring Z/nZ and the element p.
    """
    try:
        if isinstance(witness, str):
            witness = witness.replace('(', '').replace(')', '').split(',')
        n, p = witness
        n = int(n)
        p = int(p)
        if n <= 1:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    # H_1: p is a non-zero element of R
    try:
        h1 = (p % n) != 0
    except Exception:
        h1 = False
        
    # H_2: p is not a unit in R
    try:
        h2 = math.gcd(p % n, n) != 1
    except Exception:
        h2 = False
        
    # H_3: p is a prime element of R
    # Definition: non-zero, non-unit, and if p | ab then p | a or p | b
    try:
        if (p % n) == 0 or math.gcd(p % n, n) == 1:
            h3 = False
        else:
            h3 = True
            multiples_of_p = set((p * k) % n for k in range(n))
            for a in range(n):
                for b in range(n):
                    if (a * b) % n in multiples_of_p:
                        if (a % n) not in multiples_of_p and (b % n) not in multiples_of_p:
                            h3 = False
                            break
                if not h3:
                    break
    except Exception:
        h3 = False
        
    # ¬Q: p is NOT an irreducible element of R
    # Definition of irreducible: non-zero, non-unit, and if p = ab then a is a unit or b is a unit
    # Negation: p is 0, or p is a unit, or there exist a, b such that p = ab and neither is a unit
    try:
        if (p % n) == 0 or math.gcd(p % n, n) == 1:
            neg_q = True
        else:
            neg_q = False
            p_mod = p % n
            for a in range(n):
                for b in range(n):
                    if (a * b) % n == p_mod:
                        if math.gcd(a, n) != 1 and math.gcd(b, n) != 1:
                            neg_q = True
                            break
                if neg_q:
                    break
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is a non-zero element of R",
    "H_2: p is not a unit in R",
    "H_3: p is a prime element of R",
    "¬Q: p is not an irreducible element of R"
]

N_HYP = 3
NEG_Q_INDEX = 3