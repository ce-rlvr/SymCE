import sympy
from sympy import Poly
from sympy.abc import x

def conditions(witness):
    try:
        h1_ok = isinstance(witness, Poly) and bool(witness.domain.is_Field)
    except Exception:
        h1_ok = False

    try:
        h2_ok = isinstance(witness, Poly) and bool(witness.is_univariate) and witness.LC() == 1
    except Exception:
        h2_ok = False

    try:
        if not isinstance(witness, Poly) or not witness.is_univariate:
            neg_q_ok = False
        else:
            f_prime = witness.diff(witness.gens[0])
            g = witness.gcd(f_prime)
            neg_q_ok = bool(g.degree() > 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: F is a field", "H_2: f is a monic polynomial over F", "not Q: f is not separable over F"]
N_HYP = 2
NEG_Q_INDEX = 2