import sympy
from sympy import *
from sympy.abc import x, y, z
from sympy.polys.domains import ZZ, QQ

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: a is coprime to b",
    "H_3: a is coprime to c",
    "¬Q: a is not coprime to the product bc"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            if 'R' in witness:
                R = witness['R']
                a = witness['a']
                b = witness['b']
                c = witness['c']
            else:
                R = ZZ
                a = witness['a']
                b = witness['b']
                c = witness['c']
        elif len(witness) == 4:
            R, a, b, c = witness
        elif len(witness) == 3:
            R = ZZ
            a, b, c = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: R is a unique factorization domain
    try:
        h1 = bool(getattr(R, 'is_UFD', False))
    except Exception:
        h1 = False

    # H_2: a is coprime to b
    try:
        evaluated = False
        if hasattr(R, 'gcd') and hasattr(R, 'is_unit'):
            try:
                g_ab = R.gcd(a, b)
                h2 = bool(R.is_unit(g_ab))
                evaluated = True
            except Exception:
                pass
        if not evaluated:
            g_ab = sympy.gcd(a, b)
            h2 = bool(g_ab == 1 or g_ab == -1)
    except Exception:
        h2 = False

    # H_3: a is coprime to c
    try:
        evaluated = False
        if hasattr(R, 'gcd') and hasattr(R, 'is_unit'):
            try:
                g_ac = R.gcd(a, c)
                h3 = bool(R.is_unit(g_ac))
                evaluated = True
            except Exception:
                pass
        if not evaluated:
            g_ac = sympy.gcd(a, c)
            h3 = bool(g_ac == 1 or g_ac == -1)
    except Exception:
        h3 = False

    # ¬Q: a is not coprime to the product bc
    try:
        evaluated = False
        if hasattr(R, 'gcd') and hasattr(R, 'is_unit'):
            try:
                if hasattr(R, 'mul'):
                    bc = R.mul(b, c)
                else:
                    bc = b * c
                g_abc = R.gcd(a, bc)
                neg_q = not bool(R.is_unit(g_abc))
                evaluated = True
            except Exception:
                pass
        if not evaluated:
            bc = b * c
            g_abc = sympy.gcd(a, bc)
            neg_q = not bool(g_abc == 1 or g_abc == -1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]