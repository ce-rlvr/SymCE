import math
import itertools
import functools
import z3
import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys

from sympy import QQ, ZZ, Rational, I, sqrt, Poly, eye, zeros, symbols, CC, RR
from sympy.polys.domains import GF, AlgebraicField
from sympy.abc import x, y, z

S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        C, R = witness
    except Exception:
        return [False, False, False, False]
        
    def get_degree(C, R):
        if C == R:
            return 1
        
        try:
            if hasattr(C, 'order') and hasattr(R, 'order'):
                if C.characteristic == R.characteristic and C.characteristic > 0:
                    c_ord = int(C.order)
                    r_ord = int(R.order)
                    if c_ord > 1 and r_ord > 1:
                        deg = int(round(math.log(c_ord) / math.log(r_ord)))
                        if r_ord ** deg == c_ord:
                            return deg
        except Exception:
            pass

        try:
            if hasattr(C, 'domain') and C.domain == R:
                if hasattr(C, 'mod'):
                    return int(C.mod.degree())
                if hasattr(C, 'ext'):
                    return int(C.ext.minpoly.degree())
        except Exception:
            pass
            
        return None

    try:
        deg = get_degree(C, R)
    except Exception:
        deg = None

    try:
        h1 = getattr(C, 'is_Field', False) and getattr(R, 'is_Field', False) and (deg is not None)
    except Exception:
        h1 = False

    try:
        h2 = h1 and isinstance(deg, int) and deg > 0
    except Exception:
        h2 = False

    try:
        h3 = h1 and (deg > 1)
    except Exception:
        h3 = False

    try:
        neg_q = h1 and (deg != 2)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a subfield of C",
    "H_2: The degree of the field extension is finite",
    "H_3: R is not equal to C",
    "not_Q: The degree of the field extension is not exactly 2"
]

N_HYP = 3
NEG_Q_INDEX = 3