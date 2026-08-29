import sympy
from sympy import ZZ, QQ, Symbol, S
from sympy.polys.domains.domain import Domain
import math
from sympy.ntheory import factorint

x = Symbol('x')
y = Symbol('y')

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "¬Q: The extended ideal is not equal to its own radical in the polynomial ring"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        R, I = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R is a commutative ring
    try:
        if isinstance(R, Domain):
            h1 = R.is_commutative
        elif R == S.Integers:
            h1 = True
        elif hasattr(R, 'is_commutative'):
            h1 = R.is_commutative
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: I is an ideal of R
    try:
        if not isinstance(I, (list, tuple, set)):
            I_list = [I]
        else:
            I_list = list(I)
            
        h2 = True
        for elem in I_list:
            in_ring = False
            if hasattr(R, 'of_type') and R.of_type(elem):
                in_ring = True
            elif hasattr(R, '__contains__') and elem in R:
                in_ring = True
            elif hasattr(R, 'from_sympy'):
                try:
                    if R.from_sympy(sympy.sympify(elem)) is not None:
                        in_ring = True
                except Exception:
                    pass
            elif R == S.Integers and getattr(sympy.sympify(elem), 'is_integer', False):
                in_ring = True
            elif R == ZZ and isinstance(elem, int):
                in_ring = True
            if not in_ring:
                h2 = False
                break
    except Exception:
        h2 = False

    # ¬Q: The extended ideal is not equal to its own radical in the polynomial ring
    try:
        if not isinstance(I, (list, tuple, set)):
            I_list = [I]
        else:
            I_list = list(I)
            
        if not I_list:
            is_rad = True
        else:
            is_rad = True
            if R == ZZ or getattr(R, 'name', '') == 'ZZ' or R == S.Integers:
                g = abs(int(I_list[0]))
                for val in I_list[1:]:
                    g = math.gcd(g, abs(int(val)))
                if g != 0:
                    factors = factorint(g)
                    is_rad = all(exp == 1 for exp in factors.values())
            else:
                from sympy import gcd, sqf_part, cancel
                g = sympy.sympify(I_list[0])
                for val in I_list[1:]:
                    g = gcd(g, sympy.sympify(val))
                if g != 0:
                    sqf = sqf_part(g)
                    ratio = cancel(g / sqf)
                    is_rad = len(ratio.free_symbols) == 0
        neg_q = not is_rad
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]