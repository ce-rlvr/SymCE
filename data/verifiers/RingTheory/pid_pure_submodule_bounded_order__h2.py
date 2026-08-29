import sympy
from sympy import symbols, Rational, Integer
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup
Z = sympy.S.Integers
Q = sympy.S.Rationals

def get_prop(w, names):
    if isinstance(w, dict):
        for n in names:
            if n in w:
                return bool(w[n])
    for n in names:
        if hasattr(w, n):
            attr = getattr(w, n)
            return bool(attr() if callable(attr) else attr)
    raise Exception(f"Property not found: {names}")

def conditions(witness) -> list[bool]:
    if callable(witness):
        try:
            witness = witness()
        except Exception:
            pass

    h1 = False
    try:
        h1 = get_prop(witness, ['R_is_PID', 'is_PID', 'is_principal_ideal_domain', 'R_is_principal_ideal_domain'])
    except Exception:
        if isinstance(witness, (tuple, list)) and len(witness) >= 1:
            R = witness[0]
            if R == sympy.S.Integers:
                h1 = True
            else:
                try:
                    h1 = get_prop(R, ['is_PID', 'is_principal_ideal_domain'])
                except Exception:
                    pass

    h2 = False
    try:
        h2 = get_prop(witness, ['N_is_pure_submodule', 'is_pure_submodule', 'is_pure', 'N_is_pure', 'N_is_pure_submodule_of_M'])
    except Exception:
        if isinstance(witness, (tuple, list)) and len(witness) >= 3:
            M, N = witness[1], witness[2]
            try:
                h2 = bool(M.is_pure_submodule(N))
            except Exception:
                try:
                    h2 = bool(N.is_pure_submodule(M))
                except Exception:
                    pass

    h3 = False
    try:
        h3 = get_prop(witness, ['r_exists', 'is_bounded', 'N_is_bounded', 'has_bounded_order', 'exists_r_rx_eq_0', 'N_has_bounded_order'])
    except Exception:
        if isinstance(witness, (tuple, list)) and len(witness) >= 3:
            M, N = witness[1], witness[2]
            try:
                h3 = bool(N.is_bounded())
            except Exception:
                try:
                    h3 = bool(M.is_bounded(N))
                except Exception:
                    pass

    q = True
    try:
        q = get_prop(witness, ['N_is_direct_summand', 'is_direct_summand', 'N_is_direct_summand_of_M'])
    except Exception:
        if isinstance(witness, (tuple, list)) and len(witness) >= 3:
            M, N = witness[1], witness[2]
            try:
                q = bool(M.is_direct_summand(N))
            except Exception:
                try:
                    q = bool(N.is_direct_summand(M))
                except Exception:
                    pass

    return [bool(h1), bool(h2), bool(h3), not bool(q)]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: N is a pure submodule of M",
    "H_3: There exists a non-zero element r in R such that r x = 0 for all x in N",
    "¬Q: N is not a direct summand of M"
]

N_HYP = 3
NEG_Q_INDEX = 3