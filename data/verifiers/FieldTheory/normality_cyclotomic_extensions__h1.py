import sympy
from sympy import I, pi, exp, simplify, S
from sympy.abc import x, y, z
import math

# Top-level setup
QQ = sympy.QQ
ZZ = sympy.ZZ
RR = sympy.RR
CC = sympy.CC

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            zeta_n = witness.get('zeta_n')
            F = witness.get('F')
            K = witness.get('K')
        elif isinstance(witness, (tuple, list)) and len(witness) == 4:
            n, zeta_n, F, K = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: n is a positive integer
    try:
        h1 = bool(isinstance(n, (int, sympy.Integer)) and n > 0)
    except Exception:
        h1 = False

    # H2: zeta_n is a primitive n-th root of unity in some algebraic extension of F
    try:
        val = zeta_n**n
        if hasattr(val, 'simplify'):
            is_root = (simplify(val - 1) == 0)
        else:
            is_root = (val == 1)
            
        is_primitive = True
        if is_root:
            for k in range(1, int(n)):
                val_k = zeta_n**k
                if hasattr(val_k, 'simplify'):
                    if simplify(val_k - 1) == 0:
                        is_primitive = False
                        break
                else:
                    if val_k == 1:
                        is_primitive = False
                        break
        h2 = bool(is_root and is_primitive)
    except Exception:
        h2 = False

    # H3: K = F(zeta_n)
    try:
        if n == 1:
            h3 = bool(K == F)
        elif hasattr(F, 'algebraic_field') and hasattr(zeta_n, 'is_algebraic') and zeta_n.is_algebraic:
            try:
                expected_K = F.algebraic_field(zeta_n)
                h3 = bool(K == expected_K)
            except Exception:
                h3 = bool(K is not None)
        else:
            h3 = bool(K is not None)
    except Exception:
        h3 = False

    # neg_Q: K is NOT a normal extension of F
    # If F is a field, F(zeta_n) is always a normal extension (it is the splitting field of x^n - 1).
    # The conjecture fails only when F is not a field (e.g., a ring like ZZ).
    try:
        is_F_field = getattr(F, 'is_Field', False)
        if F in (S.Rationals, S.Reals, S.Complexes):
            is_F_field = True
            
        if not is_F_field:
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: zeta_n is a primitive n-th root of unity in some algebraic extension of F",
    "H_3: K = F(zeta_n)",
    "not Q: K is not a normal extension of F"
]

N_HYP = 3
NEG_Q_INDEX = 3