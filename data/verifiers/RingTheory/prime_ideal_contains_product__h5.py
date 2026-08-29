import sympy
import sympy.abc
from sympy import Rational, Integer

# Top-level setup for potential witness expressions
Z = 'Z'
ZZ = 'Z'
Integers = 'Z'

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness.get('R', 'Z')
            P = witness['P']
            I = witness['I']
            J = witness['J']
        elif len(witness) == 4:
            R, P, I, J = witness
        elif len(witness) == 3:
            P, I, J = witness
            R = 'Z'
        else:
            return [False] * 5
    except Exception:
        return [False] * 5

    # Helper to check if the ring is the integers
    try:
        is_Z = R in ('Z', 'ZZ', 'Integers') or str(R) in ('Z', 'ZZ', 'Integers')
    except Exception:
        is_Z = False

    # H1: R is a commutative ring
    try:
        if is_Z:
            h1 = True
        else:
            h1 = getattr(R, 'is_commutative', False)
            if not h1 and hasattr(R, 'domain'):
                h1 = R.domain.is_commutative
    except Exception:
        h1 = False

    # H2: P is a prime ideal of R
    try:
        if is_Z:
            h2 = (int(P) == 0) or sympy.isprime(abs(int(P)))
        else:
            h2 = (P == 0) or sympy.polys.polytools.is_irreducible(P)
    except Exception:
        h2 = False

    # H3: I is an ideal of R
    try:
        if is_Z:
            h3 = isinstance(I, (int, sympy.Integer))
        else:
            h3 = hasattr(I, 'as_poly') or isinstance(I, sympy.Expr)
    except Exception:
        h3 = False

    # H4: J is an ideal of R
    try:
        if is_Z:
            h4 = isinstance(J, (int, sympy.Integer))
        else:
            h4 = hasattr(J, 'as_poly') or isinstance(J, sympy.Expr)
    except Exception:
        h4 = False

    # neg_Q: I is not a subset of P AND J is not a subset of P
    try:
        if is_Z:
            if int(P) == 0:
                I_sub_P = (int(I) == 0)
                J_sub_P = (int(J) == 0)
            else:
                I_sub_P = (int(I) % int(P) == 0)
                J_sub_P = (int(J) % int(P) == 0)
        else:
            if P == 0:
                I_sub_P = (I == 0)
                J_sub_P = (J == 0)
            else:
                I_sub_P = sympy.rem(I, P) == 0
                J_sub_P = sympy.rem(J, P) == 0
        
        neg_q = (not I_sub_P) and (not J_sub_P)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: P is a prime ideal of R",
    "H_3: I is an ideal of R",
    "H_4: J is an ideal of R",
    "¬Q: I is not a subset of P and J is not a subset of P"
]

N_HYP = 4
NEG_Q_INDEX = 4