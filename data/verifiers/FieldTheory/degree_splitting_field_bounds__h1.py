import sympy
from sympy import factorial
from sympy.polys.polytools import Poly

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            n = int(witness.get('n', 0))
            K_deg = int(witness.get('extension_degree', 0))
            h1_ok = (n >= 1)
            h2_ok = (K_deg >= 1)
            if h1_ok and h2_ok:
                n_fact = factorial(n)
                neg_q_ok = (n_fact % K_deg != 0)
            else:
                neg_q_ok = False
        else:
            f = Poly(witness)
            n = f.degree()
            h1_ok = (n >= 1)
            h2_ok = True
            neg_q_ok = False
    except Exception:
        h1_ok = False
        h2_ok = False
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: f is a polynomial of degree n >= 1",
    "H_2: K is the splitting field of f over F",
    "not Q: The degree of the field extension K over F does not divide n!"
]

N_HYP = 2
NEG_Q_INDEX = 2