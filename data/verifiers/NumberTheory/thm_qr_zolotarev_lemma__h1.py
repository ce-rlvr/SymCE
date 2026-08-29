import math
import sympy
from sympy.combinatorics import Permutation
from sympy.ntheory import legendre_symbol

# Top-level setup
# No specific named bindings are required for this number theory conjecture.

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False, False]
        a, p = witness
    except Exception:
        return [False, False, False]
        
    try:
        if isinstance(a, int):
            h1 = True
        elif hasattr(a, 'is_integer'):
            h1 = bool(a.is_integer() if callable(a.is_integer) else a.is_integer)
        else:
            h1 = False
    except Exception:
        h1 = False
        
    try:
        h2 = False
        p_is_int = False
        if isinstance(p, int):
            p_is_int = True
        elif hasattr(p, 'is_integer'):
            p_is_int = bool(p.is_integer() if callable(p.is_integer) else p.is_integer)
            
        if p_is_int and math.gcd(int(a), int(p)) == 1:
            h2 = True
    except Exception:
        h2 = False
        
    try:
        a_int = int(a)
        p_int = int(p)
        if p_int < 2:
            # The permutation of {1, ..., p-1} is ill-defined or empty for p < 2
            neg_q = True
        else:
            perm = [(a_int * x) % p_int for x in range(1, p_int)]
            if sorted(perm) != list(range(1, p_int)):
                # Multiplication by a mod p does not permute {1, ..., p-1}
                neg_q = True
            else:
                # Convert to 0-indexed permutation for sympy
                p_obj = Permutation([val - 1 for val in perm])
                sign = p_obj.signature()
                
                try:
                    # legendre_symbol raises ValueError if p is not an odd prime
                    leg = legendre_symbol(a_int, p_int)
                    neg_q = (leg != sign)
                except Exception:
                    # If Legendre symbol is undefined, the conclusion fails
                    neg_q = True
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a is an integer",
    "H_2: a and p are coprime",
    "¬Q: The Legendre symbol (a/p) does not equal the sign of the permutation of {1, 2, ..., p-1} given by multiplication by a modulo p"
]

N_HYP = 2
NEG_Q_INDEX = 2