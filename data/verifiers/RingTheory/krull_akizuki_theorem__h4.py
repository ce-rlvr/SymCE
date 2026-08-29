import sympy
from sympy import *
import math
import itertools
import functools

class Ring:
    def __init__(self, name, is_comm, is_Noeth, is_domain, dim):
        self.name = name
        self.is_comm = is_comm
        self.is_Noeth = is_Noeth
        self.is_domain = is_domain
        self.dim = dim
        self.frac = None
        self.super_rings = set()

    def is_subring_of(self, other):
        if self == other:
            return True
        visited = set()
        queue = [self]
        while queue:
            curr = queue.pop(0)
            if curr == other:
                return True
            for sup in curr.super_rings:
                if sup not in visited:
                    visited.add(sup)
                    queue.append(sup)
        return False

    def __repr__(self):
        return self.name

# Fields
QQ = Ring('QQ', True, True, True, 0)
RR = Ring('RR', True, True, True, 0)
CC = Ring('CC', True, True, True, 0)

# Rings of integers
ZZ = Ring('ZZ', True, True, True, 1)

# Polynomial rings
ZZ_x = Ring('ZZ[x]', True, True, True, 2)
QQ_x = Ring('QQ[x]', True, True, True, 1)
RR_x = Ring('RR[x]', True, True, True, 1)
CC_x = Ring('CC[x]', True, True, True, 1)

# Rational function fields
QQ_x_frac = Ring('QQ(x)', True, True, True, 0)
RR_x_frac = Ring('RR(x)', True, True, True, 0)
CC_x_frac = Ring('CC(x)', True, True, True, 0)

# Setup fractions
ZZ.frac = QQ
QQ.frac = QQ
RR.frac = RR
CC.frac = CC

ZZ_x.frac = QQ_x_frac
QQ_x.frac = QQ_x_frac
QQ_x_frac.frac = QQ_x_frac

RR_x.frac = RR_x_frac
RR_x_frac.frac = RR_x_frac

CC_x.frac = CC_x_frac
CC_x_frac.frac = CC_x_frac

# Setup inclusions
ZZ.super_rings.update([QQ, ZZ_x])
QQ.super_rings.update([RR, QQ_x, QQ_x_frac])
RR.super_rings.update([CC, RR_x, RR_x_frac])
CC.super_rings.update([CC_x, CC_x_frac])

ZZ_x.super_rings.update([QQ_x, QQ_x_frac])
QQ_x.super_rings.update([RR_x, QQ_x_frac])
RR_x.super_rings.update([CC_x, RR_x_frac])
CC_x.super_rings.update([CC_x_frac])

QQ_x_frac.super_rings.update([RR_x_frac])
RR_x_frac.super_rings.update([CC_x_frac])

# Additional rings
ZZ_x_y = Ring('ZZ[x,y]', True, True, True, 3)
QQ_x_y = Ring('QQ[x,y]', True, True, True, 2)
QQ_x_y_frac = Ring('QQ(x,y)', True, True, True, 0)

ZZ_x_y.frac = QQ_x_y_frac
QQ_x_y.frac = QQ_x_y_frac
QQ_x_y_frac.frac = QQ_x_y_frac

ZZ_x.super_rings.update([ZZ_x_y])
QQ_x.super_rings.update([QQ_x_y])
QQ_x_frac.super_rings.update([QQ_x_y_frac])

ZZ_x_y.super_rings.update([QQ_x_y, QQ_x_y_frac])
QQ_x_y.super_rings.update([QQ_x_y_frac])

# Non-Noetherian ring
ZZ_poly_inf = Ring('ZZ[x1, x2, ...]', True, False, True, float('inf'))
QQ_poly_inf_frac = Ring('QQ(x1, x2, ...)', True, True, True, 0)
ZZ_poly_inf.frac = QQ_poly_inf_frac
QQ_poly_inf_frac.frac = QQ_poly_inf_frac

ZZ.super_rings.add(ZZ_poly_inf)
ZZ_poly_inf.super_rings.add(QQ_poly_inf_frac)
QQ.super_rings.add(QQ_poly_inf_frac)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            K = witness.get('K')
            L = witness.get('L')
            S = witness.get('S')
        else:
            R, K, L, S = witness
    except Exception:
        return [False] * 5

    # H1: R is a commutative Noetherian integral domain
    try:
        h1 = bool(R.is_comm and R.is_Noeth and R.is_domain)
    except Exception:
        h1 = False

    # H2: The Krull dimension of R is 1
    try:
        h2 = bool(R.dim == 1)
    except Exception:
        h2 = False

    # H3: K is the field of fractions of R
    try:
        h3 = bool(K == R.frac)
    except Exception:
        h3 = False

    # H4: S is a subring of L such that R \subseteq S \subseteq L
    try:
        h4 = bool(R.is_subring_of(S) and S.is_subring_of(L))
    except Exception:
        h4 = False

    # neg_Q: S is not a one-dimensional Noetherian ring
    try:
        neg_q = not (S.dim == 1 and S.is_Noeth)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian integral domain",
    "H_2: The Krull dimension of R is 1",
    "H_3: K is the field of fractions of R",
    "H_4: S is a subring of L such that R \\subseteq S \\subseteq L",
    "¬Q: S is not a one-dimensional Noetherian ring"
]

N_HYP = 4
NEG_Q_INDEX = 4