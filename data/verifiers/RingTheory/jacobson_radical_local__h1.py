import sympy
from sympy import symbols, Rational, Integer
import math
import itertools
import functools

x, y, z = symbols('x y z')

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_local_ring', False))
        else:
            h1_attr = getattr(witness, 'is_local_ring', False)
            h1 = bool(h1_attr() if callable(h1_attr) else h1_attr)
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            m = witness.get('maximal_ideal')
            j = witness.get('jacobson_radical')
            neg_q = (m != j)
        else:
            m_attr = getattr(witness, 'maximal_ideal', None)
            m = m_attr() if callable(m_attr) else m_attr
            
            j_attr = getattr(witness, 'jacobson_radical', None)
            j = j_attr() if callable(j_attr) else j_attr
            
            neg_q = (m != j)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a local ring with unique maximal ideal m",
    "¬Q: The Jacobson radical of R is not exactly the ideal m"
]

N_HYP = 1
NEG_Q_INDEX = 1