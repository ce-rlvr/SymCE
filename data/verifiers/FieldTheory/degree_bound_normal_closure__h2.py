import math
import sympy
from sympy import abc

x = sympy.Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            K_degree = witness.get('K_degree')
        else:
            n, K_degree = witness
        h1_ok = isinstance(n, int) and n > 0 and isinstance(K_degree, int) and K_degree > 0
    except Exception:
        h1_ok = False

    try:
        neg_q_ok = False
        if h1_ok:
            neg_q_ok = (K_degree % math.factorial(n)) != 0
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: E over F is a finite field extension of degree n",
    "not Q: The degree of K over F does not divide n factorial"
]

N_HYP = 1
NEG_Q_INDEX = 1