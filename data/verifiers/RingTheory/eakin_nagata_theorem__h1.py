import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

class Ring:
    def __init__(self, name, is_noetherian):
        self.name = name
        self.is_noetherian = is_noetherian

    def __repr__(self):
        return self.name

# Standard rings for the witness
ZeroRing = Ring("ZeroRing", True)
Z = Ring("Z", True)
Q = Ring("Q", True)
F2 = Ring("F2", True)
R_poly_inf = Ring("R_poly_inf", False)
R_bool_inf = Ring("R_bool_inf", False)
NonNoetherianRing = Ring("NonNoetherianRing", False)
NoetherianRing = Ring("NoetherianRing", True)

def get_is_noetherian(ring):
    if hasattr(ring, 'is_noetherian'):
        return ring.is_noetherian
    if ring == sympy.S.Zero:
        return True
    if ring in (sympy.QQ, sympy.ZZ):
        return True
    return False

def check_fg_module(S, R):
    if S == ZeroRing or S == sympy.S.Zero:
        return True
    if S == R:
        return True
    if R in (R_poly_inf, NonNoetherianRing) and S in (Q, Z, F2, NoetherianRing, ZeroRing, sympy.QQ, sympy.ZZ, sympy.S.Zero):
        return True
    if R == R_bool_inf and S in (F2, NoetherianRing, ZeroRing, sympy.S.Zero):
        return True
    return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            S = witness.get('S')
        else:
            R, S = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(get_is_noetherian(S))
    except Exception:
        h1 = False
        
    try:
        h2 = bool(check_fg_module(S, R))
    except Exception:
        h2 = False
        
    try:
        neg_q = not bool(get_is_noetherian(R))
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a Noetherian ring",
    "H_2: S is a finitely generated module over R",
    "¬Q: R is not a Noetherian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2