import sympy
from sympy import I, pi, exp, sqrt, Rational, simplify
from sympy.abc import x, y, z
from sympy.polys.domains import ZZ, QQ

def conditions(witness):
    try:
        if isinstance(witness, dict):
            omega = witness.get('omega')
            R = witness.get('R')
        else:
            omega, R = witness
    except Exception:
        return [False, False]

    try:
        # A primitive third root of unity satisfies x^2 + x + 1 = 0
        h1 = bool(simplify(omega**2 + omega + 1) == 0)
    except Exception:
        h1 = False

    try:
        # In SymPy domains, all Euclidean domains are PIDs.
        # If a domain is not a PID (e.g., ZZ[x]), it is not a Euclidean domain.
        if hasattr(R, 'is_PID'):
            neg_q = not bool(R.is_PID)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: omega is a primitive third root of unity",
    "¬Q: R is not a Euclidean domain"
]

N_HYP = 1
NEG_Q_INDEX = 1