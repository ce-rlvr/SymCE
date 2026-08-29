import sympy
from sympy import Rational, Integer
import math
import itertools
import functools

# Top-level setup
# Standard bindings for potential witness expressions
Z2 = 2
Z3 = 3
Z4 = 4
Z6 = 6

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (n, S, I) representing:
      - n: an integer >= 2, defining the commutative ring R = Z/nZ
      - S: a list/set of integers representing the subset S
      - I: a list/set of integers representing the ideal I
    """
    
    # H_1: R is a commutative ring with identity
    try:
        n, S_raw, I_raw = witness
        h1 = isinstance(n, int) and n >= 2
    except Exception:
        h1 = False

    # H_2: S is a multiplicatively closed subset of R
    try:
        n, S_raw, I_raw = witness
        if not (isinstance(n, int) and n >= 2):
            h2 = False
        else:
            S = set(x % n for x in S_raw)
            # A multiplicatively closed set typically contains the identity 1
            h2 = (1 in S)
            for a in S:
                for b in S:
                    if (a * b) % n not in S:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # H_3: I is an ideal of R such that the intersection of I and S is empty
    try:
        n, S_raw, I_raw = witness
        if not (isinstance(n, int) and n >= 2):
            h3 = False
        else:
            S = set(x % n for x in S_raw)
            I = set(x % n for x in I_raw)
            
            is_ideal = True
            if not I:
                is_ideal = False
            else:
                for a in I:
                    for b in I:
                        if (a - b) % n not in I:
                            is_ideal = False
                            break
                    for r in range(n):
                        if (a * r) % n not in I:
                            is_ideal = False
                            break
                    if not is_ideal:
                        break
            
            is_disjoint = I.isdisjoint(S)
            h3 = is_ideal and is_disjoint
    except Exception:
        h3 = False

    # ¬Q: I is not a prime ideal of R
    try:
        n, S_raw, I_raw = witness
        if not (isinstance(n, int) and n >= 2):
            neg_q = False
        else:
            I = set(x % n for x in I_raw)
            
            is_prime = True
            # A prime ideal must be a proper ideal
            if len(I) == n:
                is_prime = False
            else:
                for a in range(n):
                    for b in range(n):
                        if (a * b) % n in I:
                            if a not in I and b not in I:
                                is_prime = False
                                break
                    if not is_prime:
                        break
                        
            neg_q = not is_prime
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: S is a multiplicatively closed subset of R",
    "H_3: I is an ideal of R such that the intersection of I and S is empty",
    "¬Q: I is not a prime ideal of R"
]

N_HYP = 3
NEG_Q_INDEX = 3