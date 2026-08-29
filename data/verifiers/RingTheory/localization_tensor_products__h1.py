import sympy
from sympy import *
import sympy.abc
from sympy.abc import M, N, R, S

def get_bool(witness, *names):
    if isinstance(witness, dict):
        for name in names:
            if name in witness:
                return bool(witness[name])
    else:
        for name in names:
            if hasattr(witness, name):
                return bool(getattr(witness, name))
    return False

def get_neg_bool(witness, *names):
    if isinstance(witness, dict):
        for name in names:
            if name in witness:
                return not bool(witness[name])
    else:
        for name in names:
            if hasattr(witness, name):
                return not bool(getattr(witness, name))
    return False

def conditions(witness) -> list[bool]:
    try:
        h1 = get_bool(witness, 'M_is_R_module', 'is_R_module_M', 'M_module')
    except Exception:
        h1 = False

    try:
        h2 = get_bool(witness, 'N_is_R_module', 'is_R_module_N', 'N_module')
    except Exception:
        h2 = False

    try:
        h3 = get_bool(witness, 'S_is_multiplicatively_closed', 'is_multiplicatively_closed_S', 'S_mult_closed', 'S_is_mult_closed')
    except Exception:
        h3 = False

    try:
        neg_q = get_neg_bool(witness, 'isomorphism_holds', 'is_isomorphic', 'localization_commutes_with_tensor', 'isomorphism')
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: M is an R-module",
    "H_2: N is an R-module",
    "H_3: S is a multiplicatively closed subset of R",
    "¬Q: There is no S^{-1}R-module isomorphism between S^{-1}(M \\otimes_R N) and S^{-1}M \\otimes_{S^{-1}R} S^{-1}N"
]

N_HYP = 3
NEG_Q_INDEX = 3