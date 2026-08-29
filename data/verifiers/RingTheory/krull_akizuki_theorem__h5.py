import sympy
from sympy import *
import math
import itertools
import functools

class RingObj:
    def __init__(self, name, comm, noeth, domain, dim, frac):
        self.name = name
        self.is_commutative = comm
        self.is_Noetherian = noeth
        self.is_integral_domain = domain
        self.krull_dimension = dim
        self.field_of_fractions = frac

    def __str__(self):
        return self.name

# Standard rings and fields for the witness namespace
Z = RingObj('Z', True, True, True, 1, 'Q')
Q = RingObj('Q', True, True, True, 0, 'Q')
Q_x = RingObj('Q[x]', True, True, True, 1, 'Q(x)')
Q_x_y = RingObj('Q[x,y]', True, True, True, 2, 'Q(x,y)')
Q_x_y_z = RingObj('Q[x,y,z]', True, True, True, 3, 'Q(x,y,z)')
Q_frac_x = RingObj('Q(x)', True, True, True, 0, 'Q(x)')
Q_i = RingObj('Q(i)', True, True, True, 0, 'Q(i)')
Q_sqrt2 = RingObj('Q(sqrt(2))', True, True, True, 0, 'Q(sqrt(2))')
R_field = RingObj('R', True, True, True, 0, 'R')
C_field = RingObj('C', True, True, True, 0, 'C')

finite_extensions = {
    ('Q', 'Q'): True,
    ('Q', 'Q(i)'): True,
    ('Q', 'Q(sqrt(2))'): True,
    ('Q(x)', 'Q(x)'): True,
    ('R', 'R'): True,
    ('R', 'C'): True,
    ('C', 'C'): True,
}

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R_ring = witness['R']
            K_field = witness['K']
            L_field = witness['L']
            S_ring = witness['S']
        elif isinstance(witness, tuple) and len(witness) == 4:
            R_ring, K_field, L_field, S_ring = witness
        else:
            R_ring = witness.R
            K_field = witness.K
            L_field = witness.L
            S_ring = witness.S
    except Exception:
        return [False, False, False, False, False]

    try:
        h1 = bool(R_ring.is_commutative and R_ring.is_Noetherian and R_ring.is_integral_domain)
    except Exception:
        h1 = False

    try:
        h2 = bool(R_ring.krull_dimension == 1)
    except Exception:
        h2 = False

    try:
        h3 = bool(K_field.name == R_ring.field_of_fractions)
    except Exception:
        h3 = False

    try:
        is_field = bool(L_field.krull_dimension == 0 and L_field.is_integral_domain)
        is_fin_ext = finite_extensions.get((K_field.name, L_field.name), False)
        h4 = is_field and is_fin_ext
    except Exception:
        h4 = False

    try:
        q = bool(S_ring.krull_dimension == 1 and S_ring.is_Noetherian)
    except Exception:
        q = False
    neg_q = not q

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian integral domain",
    "H_2: The Krull dimension of R is 1",
    "H_3: K is the field of fractions of R",
    "H_4: L is a finite algebraic field extension of K",
    "¬Q: S is not a one-dimensional Noetherian ring"
]

N_HYP = 4
NEG_Q_INDEX = 4