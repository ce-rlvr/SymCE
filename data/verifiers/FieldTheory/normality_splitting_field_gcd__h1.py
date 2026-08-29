import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z
from sympy import QQ, ZZ, Poly
import math
import itertools
import functools
import z3

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def splits_completely(p, domain):
    try:
        poly = Poly(p, domain=domain)
        if poly.degree() <= 0:
            return True
        _, factors = poly.factor_list()
        return all(f.degree() == 1 for f, _ in factors)
    except Exception:
        return False

def conditions(witness):
    if hasattr(witness, 'h1') and hasattr(witness, 'h2') and hasattr(witness, 'neg_q'):
        try:
            return [bool(witness.h1), bool(witness.h2), bool(witness.neg_q)]
        except Exception:
            pass

    try:
        if isinstance(witness, dict):
            K = witness.get('K')
            L = witness.get('L')
            f = witness.get('f')
            g = witness.get('g')
            d = witness.get('d')
        else:
            K, L, f, g, d = witness
    except Exception:
        return [False, False, False]

    try:
        if hasattr(L, 'mod'):
            L_normal = splits_completely(L.mod, L)
        else:
            L_normal = (L == K)
        
        f_splits = splits_completely(f, L)
        g_splits = splits_completely(g, L)
        h1 = bool(L_normal and f_splits and g_splits)
    except Exception:
        h1 = False

    try:
        f_poly = Poly(f, domain=K)
        g_poly = Poly(g, domain=K)
        actual_gcd_poly = f_poly.gcd(g_poly)
        d_poly = Poly(d, domain=K)
        h2 = bool(d_poly.monic() == actual_gcd_poly.monic())
    except Exception:
        h2 = False

    try:
        d_splits = splits_completely(d, L)
        q = d_splits
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: L is a normal extension of K that contains the splitting fields of both f and g",
    "H_2: d = gcd(f, g) is the greatest common divisor of f and g in the polynomial ring over K",
    "¬Q: The splitting field of d over K is not contained in L or is not a normal extension of K"
]

N_HYP = 2
NEG_Q_INDEX = 2