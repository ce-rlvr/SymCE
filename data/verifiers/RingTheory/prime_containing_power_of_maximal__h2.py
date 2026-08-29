import sympy
import math
from functools import reduce

# Top-level setup
Z = sympy.S.Integers

def get_ideal_gen(I):
    """Helper to extract the generator of an ideal in Z."""
    if isinstance(I, (list, tuple, set)):
        if not I:
            return 0
        return abs(reduce(math.gcd, [int(abs(x)) for x in I]))
    return int(abs(I))

def conditions(witness) -> list[bool]:
    # Parse witness
    try:
        if isinstance(witness, dict):
            R = witness.get('R', 'Z')
            M = witness['M']
            n = witness['n']
            P = witness['P']
        elif len(witness) == 4:
            R, M, n, P = witness
        elif len(witness) == 3:
            M, n, P = witness
            R = 'Z'
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: R is a commutative ring with identity
    try:
        # We restrict verification to the ring of integers Z for simplicity,
        # as it is a commutative ring with identity where a counterexample exists.
        h1 = (R == 'Z' or R == sympy.S.Integers)
    except Exception:
        h1 = False

    # H_2: n is a positive integer
    try:
        h2 = (int(n) == n) and (int(n) > 0)
    except Exception:
        h2 = False

    # H_3: P is a prime ideal of R such that M^n is a subset of P
    try:
        if h1:
            M_val = get_ideal_gen(M)
            P_val = get_ideal_gen(P)
            
            # In Z, an ideal (p) is prime iff p is prime or p == 0
            is_prime_ideal = sympy.isprime(P_val) or P_val == 0
            
            # M^n is a subset of P iff P divides M^n.
            # Since P is a prime ideal and n > 0, P divides M^n iff P divides M.
            if P_val != 0:
                subset = (M_val % P_val == 0)
            else:
                subset = (M_val == 0)
                
            h3 = bool(is_prime_ideal and subset)
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: P is not equal to M
    try:
        if h1:
            M_val = get_ideal_gen(M)
            P_val = get_ideal_gen(P)
            # In Z, ideals are equal iff their non-negative generators are equal
            neg_q = (P_val != M_val)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: n is a positive integer",
    "H_3: P is a prime ideal of R such that M^n is a subset of P",
    "¬Q: P is not equal to M"
]

N_HYP = 3
NEG_Q_INDEX = 3