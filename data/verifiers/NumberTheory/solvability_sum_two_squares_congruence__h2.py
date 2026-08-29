import sympy
import math
import itertools
import functools
from sympy import Rational, Integer
from sympy.abc import x, y, c, p

def conditions(witness):
    """
    Checks whether the given witness satisfies the remaining hypotheses
    and falsifies the conclusion of the conjecture.
    
    The witness can be a tuple (p, c), a dictionary with keys 'p' and 'c',
    or just p (in which case the conclusion is checked for all possible c).
    """
    # Extract p and c from witness
    p_val = None
    c_val = None
    if isinstance(witness, (tuple, list)):
        if len(witness) == 2:
            p_val, c_val = witness
        elif len(witness) == 1:
            p_val = witness[0]
    elif isinstance(witness, dict):
        if 'p' in witness:
            p_val = witness['p']
        if 'c' in witness:
            c_val = witness['c']
    else:
        p_val = witness

    if p_val is None:
        return [False, False]

    # H_1: p is an odd prime
    try:
        p_int = int(p_val)
        h1 = sympy.isprime(p_int) and p_int % 2 != 0
    except Exception:
        h1 = False

    # ¬Q: The conclusion fails
    # Conclusion: There exist integers x and y such that x^2 + y^2 ≡ c (mod p)
    try:
        p_abs = abs(int(p_val))
        if p_abs == 0:
            neg_q = False
        else:
            if c_val is not None:
                c_mod = int(c_val) % p_abs
                # For any prime p, the sum of two squares takes all values mod p.
                if sympy.isprime(p_abs):
                    q = True
                else:
                    squares = set((i**2) % p_abs for i in range(p_abs))
                    q = False
                    for sq in squares:
                        if (c_mod - sq) % p_abs in squares:
                            q = True
                            break
                neg_q = not q
            else:
                # If c is not provided, check if there exists ANY c for which it fails
                if sympy.isprime(p_abs):
                    neg_q = False
                else:
                    squares = set((i**2) % p_abs for i in range(p_abs))
                    possible_sums = set()
                    for sq1 in squares:
                        for sq2 in squares:
                            possible_sums.add((sq1 + sq2) % p_abs)
                    neg_q = len(possible_sums) < p_abs
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime",
    "¬Q: There do not exist integers x and y such that x^2 + y^2 ≡ c (mod p)"
]

N_HYP = 1
NEG_Q_INDEX = 1