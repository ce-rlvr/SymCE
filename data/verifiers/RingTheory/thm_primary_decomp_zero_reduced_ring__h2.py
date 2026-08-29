import sympy
from sympy import Symbol, Poly, sqf_list
from sympy.ntheory import factorint
import math
import itertools
import functools

x, y, z = sympy.symbols('x y z')
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z9 = 9
Z12 = 12

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, (list, tuple)) and len(witness) == 1:
            witness = witness[0]
    except Exception:
        pass

    try:
        if isinstance(witness, int) or (hasattr(witness, 'is_integer') and witness.is_integer):
            n = abs(int(witness))
            if n >= 2:
                h1 = True
                factors = factorint(n)
                is_sqf = all(mult == 1 for mult in factors.values())
                neg_q = not is_sqf
                return [h1, neg_q]
    except Exception:
        pass

    try:
        if isinstance(witness, sympy.Expr):
            free_symbols = witness.free_symbols
            if len(free_symbols) >= 1:
                p = Poly(witness, *free_symbols)
                if sum(p.degree_list()) >= 1:
                    h1 = True
                    _, factors = sqf_list(p)
                    is_sqf = all(mult == 1 for _, mult in factors)
                    neg_q = not is_sqf
                    return [h1, neg_q]
    except Exception:
        pass

    return [False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "¬Q: The zero ideal of R does NOT have a primary decomposition consisting entirely of prime ideals"
]

N_HYP = 1
NEG_Q_INDEX = 1